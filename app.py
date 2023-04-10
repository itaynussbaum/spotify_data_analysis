import os
import discogs_client
import logging
from spotify import Spotify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get credentials from environment variables
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_pass = os.environ['SPOTIFY_CLIENT_SECRET']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
whatsapp_number = 'whatsapp:+14155238886'
target_number = 'whatsapp:+972547404734'  # replace with the phone number you want to send the message to

# Initialize APIs
spotify = Spotify(client_id, client_pass)
discogs = discogs_client.Client('my_user_agent/1.0', user_token=os.environ['DISCOGS_USER_TOKEN'])
client = Client(account_sid, auth_token)


def get_user_tracks():
    """Get the user's top tracks from Spotify."""
    top_tracks = spotify.get_top_tracks()
    return top_tracks['items']

def get_user_recently_played():
    """Get the user's recently played tracks from Spotify."""
    recently_played = spotify.current_user_recently_played()
    return recently_played

def get_master_ids(tracks):
    """Get the master release IDs for the given tracks from Discogs."""
    master_ids = []

    for track in tracks:
        logging.info(f"Getting master release for track: {track['album']['name']} - {track['name']}")

        # search Discogs for the master release
        master_search_results = discogs.search(track['album']['name'] + " " + track['name'], type='master').page(1)

        if master_search_results:
            # extract the master ID from the item
            master_id = master_search_results[0].id
            master_ids.append(master_id)
            logging.info(f"Found master release: {master_id}")
        else:
            logging.error("No results found for page 1.")

    return master_ids


def get_discogs_info(master_ids):
    results = []

    for master_id in master_ids:
        try:
            # Get the master release object
            master_release = discogs.master(master_id)

            # Get the Discogs URL for the master release
            discogs_url = master_release.url

            # Find the version with the lowest price
            lowest_price = master_release.data["lowest_price"]
            # get the URL of the first image in the master release's images list
            image_url = None
            if len(master_release.images) > 0:
                image_url = master_release.images[0]['uri']
            results.append([discogs_url, image_url, lowest_price])
        except:
            logging.error(f"Could not get Discogs info for master release ID {master_id}")
            continue

    return results


def validator(results):
    for discogs_url, image_url, lowest_price in results:
        logging.info(f"Discogs URL: {discogs_url}")
        if image_url:
            logging.info(f"Image URL: {image_url}")
        else:
            logging.error("No image available.")
        if lowest_price:
            logging.info(f"Lowest Price: {lowest_price}")
        else:
            logging.error("No price available.")


def send_a_message(results):
    # define the master release IDs and the message text
    message_text = "Some cool records you should check!"

    # create a Twilio MessagingResponse object and add the message text
    twiml = MessagingResponse()
    twiml.message(message_text)

    # add a Media message for each album in the results list

    for discogs_url, image_url, lowest_price in results:
        images = []
        msg = f"{message_text}: {discogs_url}. \n Price Start With: {str(lowest_price)} $"
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

        logging.info(f"Message sent! SID: {message.sid}")
def get_credentials():
    return client_id, client_pass

def main():
    tracks = get_user_tracks()
    recently_played = get_user_recently_played()
    master_ids = get_master_ids(tracks)
    results = get_discogs_info(master_ids)
    validator(results)
    send_a_message(results)


if __name__ == "__main__":
    main()