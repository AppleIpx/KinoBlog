class DeleteHttpInUrlMixin:
    def delete_http_in_url(self, url):
        return url.replace("https://", "", 1)
