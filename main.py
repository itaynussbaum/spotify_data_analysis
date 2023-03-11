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

# Call spotify
spotify = Spotify(client_id, client_pass)
# Call discogs
discogs = discogs_client.Client('my_user_agent/1.0', user_token='dEtgKPduASaiXftmQpaNuxMEBVySnUwZvxPlJPgQ')

# define the Twilio API credentials and the target phone number
account_sid = 'ACc87e68f855dc603c3cbe439347d1a1ba'
auth_token = '6291681b5b8f6ff992d24daa8c27c1e6'
whatsapp_number = 'whatsapp:+14155238886'
target_number = 'whatsapp:+972547404734'  # replace with the phone number you want to send the message to

# create a Twilio API client
client = Client(account_sid, auth_token)


def get_user_tracks():
    top_tracks = spotify.get_top_tracks()
    top_tracks = top_tracks['items']
    return top_tracks


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

        # Find the version with the lowest price
        lowest_price = master_release.data["lowest_price"]
        # get the URL of the first image in the master release's images list
        image_url = None
        if len(master_release.images) > 0:
            image_url = master_release.images[0]['uri']

        results.append([discogs_url, image_url, lowest_price])

    return results


def validator(results):
    for discogs_url, image_url, lowest_price in results:
        print(f"Discogs URL: {discogs_url}")
        if image_url:
            print(f"Image URL: {image_url}")
        else:
            print("No image available.")
        if lowest_price:
            print(f"Lowest Price: {lowest_price}")
        else:
            print("No price available.")


def send_a_message(results):
    # define the master release IDs and the message text
    message_text = "Some cool records you should check!"

    # create a Twilio MessagingResponse object and add the message text
    twiml = MessagingResponse()
    twiml.message(message_text)

    # add a Media message for each album in the results list

    for discogs_url, image_url, lowest_price in results:
        images = []
        msg = message_text + " " + discogs_url + " " + "\n" + "Price Start With " + str(lowest_price)
        if image_url:
            images.append(image_url)
        else:
            pass

        # send the message via the Twilio API
        message = client.messages.create(
            media_url=images,
            body=msg,
            from_=whatsapp_number,
            to=target_number,
            # status_callback='https://yourapp.com/status_callback'
        )

        print(f"Message sent! SID: {message.sid}")


tracks = get_user_tracks()
master_ids = get_master_ids(tracks)
results = get_discogs_info(master_ids)
validator(results)
send_a_message(results)
