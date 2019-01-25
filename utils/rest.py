import os
import requests
import json


class OktaUtil:
    # TODO: This should be configuration driven
    REST_HOST = None
    REST_TOKEN = None
    OKTA_SESSION_ID_KEY = "okta_session_id"
    OKTA_SESSION_TOKEN_KEY = "okta_session_id"
    DEVICE_TOKEN = None
    OKTA_HEADERS = {}
    OKTA_OAUTH_HEADERS = {}
    OIDC_CLIENT_ID = None
    OIDC_CLIENT_SECRET = None
    AUTH_SERVER_ID = None

    def __init__(self, headers):
        # This is to supress the warnings for the older version
        # requests.packages.urllib3.disable_warnings((InsecurePlatformWarning, SNIMissingWarning))

        self.REST_HOST = os.environ["OKTA_ORG_URL"]
        self.REST_TOKEN = os.environ["OKTA_API_TOKEN"]
        self.OIDC_CLIENT_ID = os.environ["OKTA_APP_CLIENT_ID"]
        self.OIDC_CLIENT_SECRET = os.environ["OKTA_APP_CLIENT_SECRET"]
        self.OIDC_REDIRECT_URL = os.environ["OKTA_OIDC_REDIRECT_URL"]
        if "OIDC_CLIENT_ID" in os.environ:
            self.OIDC_CLIENT_ID = os.environ["OIDC_CLIENT_ID"]

        if "OIDC_CLIENT_SECRET" in os.environ:
            self.OIDC_CLIENT_SECRET = os.environ["OIDC_CLIENT_SECRET"]

        if "OIDC_REDIRECT_URL" in os.environ:
            self.OIDC_REDIRECT_URL = os.environ["OIDC_REDIRECT_URL"]

        if "OKTA_AUTHSERVER_ID" in os.environ:
            self.AUTH_SERVER_ID = os.environ["OKTA_AUTHSERVER_ID"]
            print("HAS AUTH SERVER: {0}".format(self.AUTH_SERVER_ID))

        user_agent = ""
        if "User-Agent" in headers:
            user_agent = headers["User-Agent"]

        self.OKTA_HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS {api_token}".format(api_token=self.REST_TOKEN),
            "User-Agent": user_agent
        }

        if "X-Forwarded-For" in headers:
            self.OKTA_HEADERS["X-Forwarded-For"] = headers["X-Forwarded-For"]

        if "X-Forwarded-Port" in headers:
            self.OKTA_HEADERS["X-Forwarded-Port"] = headers["X-Forwarded-Port"]

        if "X-Forwarded-Proto" in headers:
            self.OKTA_HEADERS["X-Forwarded-Proto"] = headers["X-Forwarded-Proto"]

        self.OKTA_OAUTH_HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {encoded_auth}".format(
                encoded_auth=self.get_encoded_auth(
                    client_id=self.OIDC_CLIENT_ID,
                    client_secret=self.OIDC_CLIENT_SECRET))
        }

        print("OKTA_OAUTH_HEADERS: {0}".format(json.dumps(self.OKTA_OAUTH_HEADERS, indent=4, sort_keys=True)))

    def get_o365_groups(self):
        print("get_o365_groups")
        url = "{host}/api/v1/groups?q=Office 365".format(host=self.REST_HOST)
        body = {}

        return self.execute_get(url, body)

    def get_users_by_group_id(self, group_id):
        print("get_users_by_group_id")
        url = "{host}/api/v1/groups/{group_id}/users".format(host=self.REST_HOST, group_id=group_id)
        body = {}

        return self.execute_get(url, body)

    def execute_post(self, url, body, headers=None):
        print("execute_post(): ", url)
        print(body)

        headers = self.reconcile_headers(headers)

        rest_response = requests.post(url, headers=headers, json=body)
        response_json = rest_response.json()

        # print json.dumps(response_json, indent=4, sort_keys=True)
        return response_json

    def execute_put(self, url, body, headers=None):
        print("execute_put(): ", url)
        print(body)

        headers = self.reconcile_headers(headers)

        rest_response = requests.put(url, headers=headers, json=body)
        response_json = rest_response.json()

        # print json.dumps(response_json, indent=4, sort_keys=True)
        return response_json

    def execute_delete(self, url, body, headers=None):
        print("execute_delete(): ", url)
        print(body)

        headers = self.reconcile_headers(headers)

        rest_response = requests.delete(url, headers=headers, json=body)
        try:
            response_json = rest_response.json()
        except Exception as e:
            response_json = {"status": "none"}

        # print json.dumps(response_json, indent=4, sort_keys=True)
        return response_json

    def execute_get(self, url, body, headers=None):
        print("execute_get(): ", url)
        print(body)

        headers = self.reconcile_headers(headers)

        rest_response = requests.get(url, headers=headers, json=body)
        response_json = rest_response.json()

        # print json.dumps(response_json, indent=4, sort_keys=True)
        return response_json

    def reconcile_headers(self, headers):

        if headers is None:
            headers = self.OKTA_HEADERS

        return headers
