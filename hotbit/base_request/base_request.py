import requests
import hashlib
from uuid import uuid1
import collections
import json


class HotbitBaseRestApi(object):
    def __init__(
        self,
        key: str = "",
        secret: str = "",
        url: str = "https://api.hotbit.io",
        api_level: int = 2,
    ):
        """

        Args:
            key (str, optional): hotbit api key
            secret (str, optional): hotbit api secret
            url (str, optional): hotbit api url. Defaults to "https://api.hotbit.io".
            api_level (int, optional): api interaction level. Defaults to 2.
        """
        self.url = url
        self.key = key
        self.secret = secret
        self.api_level = api_level
        self.url_api_level = self.url + f"/v{api_level}"

    def _request(self, method, uri, params=None, timeout=5, auth=True):
        data_json = ""
        parameters_string = ""
        if params:
            params_sorted = collections.OrderedDict(sorted(params.items()))
            strl = []
            for key in params_sorted:
                strl.append(f"{key}={params_sorted[key]}")
            data_json += "&".join(strl)
            parameters_string = data_json

        if auth:
            data_json_temp = data_json + "&secret_key=" + self.secret
            sign = hashlib.md5(data_json_temp.encode("utf-8")).hexdigest().upper()
            parameters_string += "&sign=" + sign
            if method == "POST":
                params["sign"] = sign

        if method == "POST":
            url = self.url + "/" + uri
        else:
            url = self.url + "/" + uri + "?" + parameters_string

        if method == "POST":
            headers = {"Content-Type": "application/json"}
            response_data = requests.post(
                url, json.loads(json.dumps(params, sort_keys=True, indent=4)), headers
            )
        else:
            response_data = requests.request(method, url, timeout=timeout)

        return self.__check_response_data(response_data)

    def _set_permission_level(self, permission_level):
        self.url = self.url_api_level + f"/p{permission_level}"

    @staticmethod
    def __check_response_data(response_data):

        if response_data.status_code == 200:
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)

            if "ticker" in data:
                return data["ticker"]

            if data and "error" in data:
                if not data.get("error"):
                    return data["result"]
                else:
                    raise Exception("{}-{}".format(response_data.status_code, response_data.text))
        else:
            raise Exception("{}-{}".format(response_data.status_code, response_data.text))

    @property
    def _return_unique_id(self):
        return "".join([each for each in str(uuid1()).split("-")])
