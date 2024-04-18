def check_anonymous_retrieve_fields(self, response):
    fields_to_remove = [
        "is_watched",
        "is_see_late",
        "is_favorite",
        "like_count",
        "dislike_count",
    ]
    required_fields = self.list_fields + self.base_fields + self.retrieve_fields
    required_anonymous_fields = [field for field in required_fields if field not in fields_to_remove]
    result = response.data
    for field in required_anonymous_fields:
        self.assertIn(
            field,
            result,
            f"Это поле '{field}' должно быть в детальном просмотре",
        )
