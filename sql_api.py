
import psycopg2
import config

class DB:
    def __init__(self, config):
        self.config = config

    def con(self):
        # Establish a connection to the database
        self.database = psycopg2.connect(
            host=self.config['postgres_host'],
            database=self.config['postgres_database'],
            user=self.config['postgres_user'],
            password=self.config['postgres_password']
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
        self.con()
        # Create the INSERT statement
        sql = f"""INSERT INTO usernames (id, mastodon, source) 
        VALUES ('{twitter_username}', '{mastodon_username}', '{source_tweet}') 
        ON CONFLICT (id) DO UPDATE SET id = EXCLUDED.id, mastodon = EXCLUDED.mastodon, source = EXCLUDED.source"""
        # Execute the INSERT statement
        self.cursor.execute(sql)
        # Commit the transaction
        self.database.commit()
        self.database.close()
