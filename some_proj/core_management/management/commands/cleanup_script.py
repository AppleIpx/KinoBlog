import json
import logging
from datetime import date
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import pytz
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models
from django.db import transaction
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from wagtail.fields import StreamField

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Django management command to clean up outdated data from a specified model.
    The command supports creating backups before deleting outdated records.
    """

    help = "Clean up outdated data from a specified model."

    def add_arguments(self, parser):
        """
        Define arguments for the command.

        Args:
            parser: The argument parser instance.
        """

        parser.add_argument("model_name", type=str, help="Model name in the format app_label.ModelName")
        parser.add_argument("date_field", type=str, help="Field name to check date for deletion")
        parser.add_argument("expiry_days", type=int, help="Number of days after which data is considered outdated")

    def _filling_data(self, **options):
        """
        Extract necessary data from the provided options.

        Args:
            options: A dictionary of options passed to the command.

        Returns:
            Tuple containing model name, date field, and expiry days.
        """
        return (
            options["model_name"],
            options["date_field"],
            options["expiry_days"],
        )

    def _find_outdated_records(self, model, date_field, threshold_date):
        """
        Find records in the model that are outdated based on the threshold date.

        Args:
            model: The Django model to query.
            date_field: The field used to determine if a record is outdated.
            threshold_date: The date used as the threshold for finding outdated records.

        Returns:
            QuerySet of outdated records.
        """
        return model.objects.filter(**{f"{date_field}__lt": threshold_date})

    def _default_json_serializer(self, obj):
        """
        Default JSON serializer for handling non-serializable objects like datetime.

        Args:
            obj: The object to serialize.

        Returns:
            Serialized value of the object.

        Raises:
            TypeError: If the object type is not serializable.
        """
        if isinstance(obj, date | datetime):
            return obj.isoformat()
        msg = f"Type {type(obj)} is not serializable"
        raise TypeError(msg)

    def _create_dir(self, model_name: str) -> Path:
        """
        Create a directory for backup files.

        Args:
            model_name: Name of the model to create a backup directory for.

        Returns:
            Path to the newly created backup file.
        """
        backup_dir = Path.cwd() / "backups" / model_name
        backup_dir.mkdir(parents=True, exist_ok=True)

        tz = pytz.UTC
        current_time = datetime.now(tz).strftime("%Y%m%d_%H%M%S")

        return backup_dir / f"backup_{model_name}_{current_time}.json"

    def _create_backup(self, model, model_name):
        """
        Create a backup of all records in the model.

        Args:
            model: The Django model whose records will be backed up.
            model_name: Name of the model for the backup file.

        Raises:
            Exception: If there is an error during the backup process.
        """
        backup_filename = self._create_dir(model_name)
        try:
            all_records = list(model.objects.all().values())
            with backup_filename.open("w") as backup_file:
                json.dump(all_records, backup_file, default=self._default_json_serializer)
            msg = f"Backup created: {backup_filename}"
            logger.info(msg)
        except Exception:
            error_msg = "Error creating backup:"
            logger.exception(error_msg)
            self.stdout.write(self.style.ERROR("Failed to create backup."))
            raise

    def _create_backup_with_serializer(self, model, model_name, user_serializer):
        """
        Create a backup of all records in the model using the provided serializer.

        Args:
            model: The Django model whose records will be backed up.
            model_name: Name of the model for the backup file.
            user_serializer: The serializer class to use for serializing model instances.

        Raises:
            Exception: If there is an error during the backup process.
        """
        backup_filename = self._create_dir(model_name)
        try:
            all_records = list(model.objects.all())
            serializer = user_serializer(all_records, many=True)
            with backup_filename.open("w") as backup_file:
                json.dump(serializer.data, backup_file)
        except Exception:
            error_msg = "Error creating backup with serializer:"
            logger.exception(error_msg)
            self.stdout.write(self.style.ERROR("Failed to create backup with serializer."))
            raise

    def _delete_outdated_records(self, outdated_records):
        """
        Delete the outdated records from the database.

        Args:
            outdated_records: QuerySet of records to delete.

        Raises:
            Exception: If there is an error during the deletion process.
        """
        try:
            with transaction.atomic():
                deleted_count = outdated_records.delete()
                if deleted_count is not None:
                    msg = f"Deleted {deleted_count} outdated records"
                    logger.info(msg)
        except Exception:
            logger.exception("Error deleting outdated records")
            self.stdout.write(self.style.ERROR("Failed to delete outdated records."))
            raise

    def _find_serializer(self):
        """
        Prompts the user to input the full name of a serializer and attempts to import it.

        Returns:
            The serializer class if found, None otherwise.

        Raises:
            Exception: If there is an error during the import process.
        """
        msg = "Non-serializable data was detected in the passed model; a serializer is required."
        self.stdout.write(self.style.WARNING(msg))
        user_input_serializer = input(
            "Enter the full name of the serializer (exmp: root_dir.app_name.serializers.SerializerName): ",
        )
        try:
            module_name, serializer_name = user_input_serializer.rsplit(".", 1)
            serializer_module = __import__(module_name, fromlist=[serializer_name])
            return getattr(serializer_module, serializer_name)
        except (ImportError, AttributeError) as e:
            self.stdout.write(self.style.ERROR(f"Failed to find serializer: {e}"))
            return None

    def _check_difficulty_model(self, model):
        """
        Checks whether the given model contains fields that are considered difficult to serialize.

        Args:
            model: The Django model to check for difficult fields.

        Returns:
            bool: True if the model has difficult fields, False otherwise.
        """
        difficult_fields = (
            models.ForeignKey,
            models.ManyToManyField,
            models.OneToOneField,
            models.JSONField,
            models.FileField,
            models.ImageField,
            models.TextField,
            models.BinaryField,
            models.DurationField,
            models.DecimalField,
            ParentalManyToManyField,
            ParentalKey,
            StreamField,
        )
        return any(isinstance(field, difficult_fields) for field in model._meta.get_fields())  # noqa: SLF001

    def _get_model(self, model_name):
        """
        Get the Django model class based on the model name.

        Args:
            model_name: The model name in the format app_label.ModelName.

        Returns:
            The Django model class.
        """
        return apps.get_model(*model_name.split("."))

    def handle(self, *args, **options):
        """
        Main entry point for the command. Handles backup and deletion of outdated records.

        Args:
            *args: Positional arguments.
            **options: Keyword arguments containing model_name, date_field, and expiry_days.
        """
        model_name, date_field, expiry_days = self._filling_data(**options)

        model = self._get_model(model_name)
        threshold_date = timezone.now() - timedelta(days=expiry_days)

        outdated_records = self._find_outdated_records(model, date_field, threshold_date)

        if not outdated_records.exists():
            msg = "No outdated records found."
            logger.info(msg)
            self.stdout.write(self.style.SUCCESS("No outdated records found."))
            return

        if self._check_difficulty_model(model):
            user_serializer = self._find_serializer()
            self._create_backup_with_serializer(model, model_name, user_serializer)
        else:
            self._create_backup(model, model_name)

        self._delete_outdated_records(outdated_records)
        self.stdout.write(self.style.SUCCESS("Backup completed successfully, outdated data deleted."))
