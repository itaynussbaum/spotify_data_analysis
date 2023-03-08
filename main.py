import os
import re
import json
import discogs_client
import spotipy
import pandas as pd
from discogs import Discogs
from spotify import Spotify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Spotify credentials
client_id = os.environ['client_id']
client_pass = os.environ['client_secret']
# Discogs credentials
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']

# Call spotify
spotify = Spotify(client_id, client_pass)
discogs = discogs_client.Client('my_user_agent/1.0', user_token='dEtgKPduASaiXftmQpaNuxMEBVySnUwZvxPlJPgQ')
# Call discogs

# discogs = Discogs(consumer_key, consumer_secret)

# get the user's top tracks
top_tracks = spotify.get_top_tracks()
tracks = top_tracks['items']


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


def get_master_ids(tracks):
    # create a Discogs API client
    master_ids = []
    for track in tracks:
        print(track['album']['name'] + " - " + track['name'])

        # search Discogs for the master release
        master_search_results = discogs.search(track['album']['name'] + " " + track['name'], type='master')

        # get the first page of search results
        page = master_search_results.page(1)

        if page:
            # get the first item in the page
            item = page[0]
            # extract the master ID from the item
            master_id = item.id
            master_ids.append(master_id)
            print(f"Master ID: {master_id}")
        else:
            print("No results found for page 1.")

    return master_ids


def get_discogs_info(master_ids):
    results = []

    for master_id in master_ids:
        # get the master release object
        master_release = discogs.master(master_id)

        # get the Discogs URL for the master release
        discogs_url = master_release.url

        # get the URL of the first image in the master release's images list
        image_url = None
        if len(master_release.images) > 0:
            image_url = master_release.images[0]['uri']

        results.append([discogs_url, image_url])

    return results


master_ids = get_master_ids(tracks)
results = get_discogs_info(master_ids)

for discogs_url, image_url in results:
    print(f"Discogs URL: {discogs_url}")
    if image_url:
        print(f"Image URL: {image_url}")
    else:
        print("No image available.")

# define the Twilio API credentials and the target phone number
account_sid = 'ACc87e68f855dc603c3cbe439347d1a1ba'
auth_token = 'd33438f84a9b7a531ab28e137bb8b4cd'
whatsapp_number = 'whatsapp:+14155238886'
target_number = 'whatsapp:+972547404734'  # replace with the phone number you want to send the message to

# create a Twilio API client
client = Client(account_sid, auth_token)

# define the master release IDs and the message text
message_text = "Some cool records you should check!"

# fetch the Discogs URLs and album image URLs for the master releases
results = []
for master_id in master_ids:
    master_release = discogs.master(master_id)
    discogs_url = master_release.url
    image_url = None
    if len(master_release.images) > 0:
        image_url = master_release.images[0]['uri']
    results.append((discogs_url, image_url))

# create a Twilio MessagingResponse object and add the message text
twiml = MessagingResponse()
twiml.message(message_text)

# add a Media message for each album in the results list
for discogs_url, image_url in results:
    images = []
    msg = message_text + " " + discogs_url + "\n"
    if image_url:
        images.append(image_url)
        #twiml.message(discogs_url).media(image_url)
    else:
        pass
        #twiml.message(discogs_url)

    # send the message via the Twilio API
    message = client.messages.create(
        media_url=images,
        body=msg,
        from_=whatsapp_number,
        to=target_number,
        # status_callback='https://yourapp.com/status_callback'
    )

    print(f"Message sent! SID: {message.sid}")

