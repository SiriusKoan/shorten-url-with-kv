import json
import requests


class KV:
    def init_app(self, app) -> None:
        self.account = app.config["KV_ACCOUNT_IDENTIFIER"]
        self.namespace = app.config["KV_NAMESPACE_IDENTIFIER"]
        self.email = app.config["EMAIL"]
        self.x_auth_key = app.config["X_AUTH_KEY"]
        self.headers = {"X-Auth-Email": self.email, "X-Auth-Key": self.x_auth_key}
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account}/storage/kv/namespaces/{self.namespace}/values/"

    def read(self, key):
        url = self.base_url + key
        r = requests.get(url, headers=self.headers)
        try:
            msg = r.json()
        except json.decoder.JSONDecodeError:
            return r.content.decode("utf-8")
        else:
            return msg["success"]

    def write(self, value, key):
        # create and update
        write_headers = self.headers.copy()
        write_headers["Content-Type"] = "text/plain"
        url = self.base_url + key
        r = requests.put(url, headers=write_headers, data=value)
        return r.json()["success"]

    def delete(self, key):
        url = self.base_url + key
        r = requests.delete(url, headers=self.headers)
        return r.json()["success"]


kv = KV()
