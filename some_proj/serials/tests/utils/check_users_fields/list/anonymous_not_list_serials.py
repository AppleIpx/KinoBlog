def check_anonymous_not_list_fields(self, response):
    retrieve_fields = [*self.retrieve_fields, "is_favorite", "like_count", "dislike_count"]
    for result in response.data["results"]:
        for field in retrieve_fields:
            self.assertNotIn(
                field,
                result,
                f"Этого поля '{field}' в листе не должно быть",
            )
