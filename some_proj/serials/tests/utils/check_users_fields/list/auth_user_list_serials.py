def check_auth_user_list_fields(self, response):
    required_fields = self.list_fields + self.base_fields
    for result in response.data["results"]:
        for field in required_fields:
            self.assertIn(
                field,
                result,
                f"Это поле '{field}' в листе должно быть",
            )
