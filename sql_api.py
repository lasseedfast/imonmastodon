
import psycopg2

class DB:
    def __init__(self, config):
        # Establish a connection to the database
        self.database = psycopg2.connect(
            host=config['postgres_host'],
            database=config['postgres_database'],
            user=config['postgres_user'],
            password=config['postgres_password']
            )
        self.cursor = self.database.cursor()

    def select(self, sql):
        """Returns a list of dicts from DB."""
        things = self.database.execute(sql).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked

    def commit(self, sql):
        """ Inserts from a query. """
        self.cursor.execute(sql)
        self.database.commit()

    def insert_user(self, twitter_username, mastodon_username, source_tweet):
       
        # Create the INSERT statement
        sql = f"""INSERT INTO usernames (id, mastodon, source) 
        VALUES ('{twitter_username}', '{mastodon_username}', '{source_tweet}') 
        ON CONFLICT (id) DO UPDATE SET id = EXCLUDED.id, mastodon = EXCLUDED.mastodon, source = EXCLUDED.source"""
        # Execute the INSERT statement
        self.cursor.execute(sql)
        # Commit the transaction
        self.database.commit()
