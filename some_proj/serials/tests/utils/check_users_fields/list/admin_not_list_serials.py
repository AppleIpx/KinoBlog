def check_admin_not_list_fields(self, response):
    for result in response.data["results"]:
        for field in self.retrieve_fields:
            self.assertNotIn(
                field,
                result,
                f"Этого поля '{field}' в листе не должно быть",
            )
