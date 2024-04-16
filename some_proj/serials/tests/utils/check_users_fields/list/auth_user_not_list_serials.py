def check_auth_user_not_list_fields(self, response):
    retrieve_fields = [*self.retrieve_fields, "data_added"]
    for result in response.data["results"]:
        for field in retrieve_fields:
            self.assertNotIn(
                field,
                result,
                f"Этого поля '{field}' в листе не должно быть",
            )
