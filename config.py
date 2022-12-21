import os
import json


def create_config():
    # Create a config file. #* Add more keys if necessary.
    config = {}
    with open("config.json", "w") as f:
        # Info for Twitter:
        twitter_token = input("Twitter token bearer: ")
        config["twitter_token"] = twitter_token
        config['bot_username'] = input('Bot username: ')

        # Info for Postgresql database:
        config['postgres_host'] = input('Postgres database host: ')
        config['postgres_user'] = input('Postgres database username: ')
        config['postgres_password'] = input('Postgres database password: ')
        config['postgres_database'] = input('Postgres database name: ')
            
        # Write to file.
        json.dump(config, f)
    return config


def update_config(key, value):
    # Check if the config files with the token exist, create it if not.
    if os.path.exists("config.json"):
        with open("config.json") as f:
            config = json.load(f)
            config[key] = value
    else:
        print("No config file, creating one...")
        config = create_config()
        config[key] = value
    
    # Write updated config to file.
    with open("config.json", "w") as f:
        json.dump(config, f)
    return config


def get_config(check_for=False):
    # Returns a config file, creating one if not existing.
    if os.path.exists("config.json"):
        with open("config.json") as f:
            try:
                config = json.load(f)
            except json.decoder.JSONDecodeError:
                config = create_config()
            if check_for:
                for i in check_for:
                    if i not in config:
                        config = create_config()
    else:
        config = create_config()
    return config


def get_dropbox_tokens(app_key):
    from dropbox import DropboxOAuth2FlowNoRedirect
    '''
    Populate your app key in order to run this locally
    '''

    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, use_pkce=True, token_access_type='offline')

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    oauth_result = auth_flow.finish(auth_code)
    return oauth_result


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    create_config()
    print(f'Configuration file created at {os.path.realpath("config.json")}.')
