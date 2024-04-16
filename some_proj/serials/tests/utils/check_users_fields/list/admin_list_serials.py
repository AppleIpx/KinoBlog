def check_admin_list_fields(self, response):
    required_fields = [*self.list_fields, "data_added", *self.base_fields]
    for result in response.data["results"]:
        for field in required_fields:
            self.assertIn(
                field,
                result,
                f"Это поле '{field}' в листе должно быть",
            )
