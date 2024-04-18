def check_anonymous_list_fields(self, response):
    fields_to_remove = [
        "is_favorite",
        "like_count",
        "dislike_count",
    ]
    list_fields = [field for field in self.list_fields if field not in fields_to_remove]
    required_fields = list_fields + self.base_fields
    for result in response.data["results"]:
        for field in required_fields:
            self.assertIn(
                field,
                result,
                f"Это поле '{field}' в листе должно быть",
            )
