import discogs_client
from discogs_client.exceptions import HTTPError






class Discogs:
    # discogs section
    def __init__(self, consumer_key: str, consumer_secret: str,):
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret
        # set up the discogs client
        self.discogs = discogs_client.Client('my_user_agent/1.0',
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )
        self.discogs.get_authorize_url()
        self.discogs.get_access_token('verifier-here')
        me = self.discogs.identity()
        print(me)


    def search(self, name: str):
        results = self.discogs.search(name, type='release')
        return results

# discogs search -
