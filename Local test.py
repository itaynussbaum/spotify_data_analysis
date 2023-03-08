

# release = discogs.search('meddle', type='master')
# print(release.page(1))
# print the list of track ids

def print_track(top_tracks):
    for track in top_tracks['items']:
        print(track['artists'][0]['name'])
        print(track['album']['name'])
        print(track['name'])
        print(track['preview_url'])
        print(track['album']['images'][0]['url'])

# Discogs credentials
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
