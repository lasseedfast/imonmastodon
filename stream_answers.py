import re
import json
import requests

import sql_api
import twitter_api
import config

def extract_mastodon_handle(text):
    """ Get a mastodon alias form a text (assuming a word with 
    two @ and a . in the later part of the wordis a mastodon alias). """
    handle = re.search(r'@\w+@\w+.\w+', text)
    if handle:
        handle = handle.group()
    else:
        handle = False
    return handle

def stream():
    """ Monitor answers to a tweet. """
    # Make connection to SQL databse.
    db = sql_api.DB(config.get_config())
    api = twitter_api.API()

    rules = api.get_rules()
    api.delete_all_rules(rules)
    api.set_rules()
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=referenced_tweets.id,author_id", auth=api.bearer_oauth, stream=True,
    )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            try:
                twitter_username =  json_response['includes']['users'][0]['username']
                mastodon_username = extract_mastodon_handle(json_response['includes']['tweets'][0]['text'])
                if mastodon_username:
                    print(mastodon_username)
                    try:
                        source_tweet = str(json_response['data']['id'])
                    except:
                        source_tweet = 'user'
                    # Add Mastodon username to db.
                    db.insert_user(twitter_username, mastodon_username, source_tweet)

            except:
                pass


if __name__ == "__main__":

    stream()
