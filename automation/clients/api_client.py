import requests


class APIClient:

    def __init__(self, base_url, token=None, timeout=10):

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json"
        })

        if token:
            self.set_token(token)

    def set_token(self, token):

        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def clear_token(self):

        self.session.headers.pop(
            "Authorization",
            None
        )

    def get(self, endpoint, **kwargs):

        return self.session.get(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout,
            **kwargs
        )

    def post(self, endpoint, **kwargs):

        return self.session.post(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout,
            **kwargs
        )

    def put(self, endpoint, **kwargs):

        return self.session.put(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout,
            **kwargs
        )

    def delete(self, endpoint, **kwargs):

        return self.session.delete(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout,
            **kwargs
        )