def check_admin_retrieve_fields(self, response):
    required_fields = self.list_fields + self.base_fields + self.retrieve_fields + ["data_added"]
    result = response.data
    for field in required_fields:
        self.assertIn(
            field,
            result,
            f"Это поле '{field}' должно быть в детальном просмотре",
        )
