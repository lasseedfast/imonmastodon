import requests
import config
from requests_oauthlib import OAuth2Session, OAuth1Session

class API:
    def __init__(self):

        conf = config.get_config()
        if 'twitter_token' not in conf:
            config.update('twitter_token', input('Twitter token:'))
        self.bearer_token = conf['twitter_token']
        self.user_agent = "v2UserLookupPython"
        self.bot_username = conf['bot_username']
    
    def bearer_oauth(self, r):
        """ Method required by bearer token authentication. """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = self.user_agent
        return r

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FilteredStreamPython"
        return r

    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", auth=self.bearer_oauth
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        return response.json()


    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload
        )

    def set_rules(self):
        # You can adjust the rules if needed
        rules = [
            {"value": f"@{self.bot_username}"}
        ]
        payload = {"add": rules}
        requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
