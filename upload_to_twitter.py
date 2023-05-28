import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import generate_image
from generate_image import prompt
import configparser
import os

def upload_image_to_twitter(image_url, consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Uploads an image to Twitter using the provided token and get the media id.

    Args:
        image_url (str): The URL of the image to be uploaded.
        consumer_key (str): Twitter consumer key.
        consumer_secret (str): Twitter consumer secret.
        access_token (str): Twitter access token.
        access_token_secret (str): Twitter access token secret.

    Returns:
        str: The media id of the uploaded image.
    """
    response = requests.get(image_url)
    response.raise_for_status()
    image_filename = "image.jpg"
    media_params = {
        "media_category": "tweet_image"
    }

    oauth_media = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    with open(image_filename, "wb") as file:
        file.write(response.content)

    with open(image_filename, "rb") as file:
        response = requests.post("https://upload.twitter.com/1.1/media/upload.json", auth=oauth_media, files={"media": file}, data=media_params)


    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    media_id = str(response.json()["media_id"])
    return media_id


def tweet_with_image(prompt, media_id, consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Tweets a message with the attached image using the provided token.
    Since the API version for uploading Twitter images differs from the one used for uploading a tweet with an image, it is essential to authenticate the user again.

    Args:
        prompt (str): The text content of the tweet.
        media_id (str): The media id of the uploaded image.
        consumer_key (str): Twitter consumer key.
        consumer_secret (str): Twitter consumer secret.
        access_token (str): Twitter access token.
        access_token_secret (str): Twitter access token secret.
    """
    oauth_tweet = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    payload = {
        "text": prompt,
        "media": {"media_ids": [media_id]}
    }

    response = oauth_tweet.post("https://api.twitter.com/2/tweets", json=payload)

    if response.status_code != 201:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    print("Successfully uploaded to Twitter!")


def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(directory, "config.ini")
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Read user token from the config file" 
    consumer_key = config.get("Twitter", "consumer_key")
    consumer_secret = config.get("Twitter", "consumer_secret")
    access_token = config.get("Twitter", "access_token")
    access_token_secret = config.get("Twitter", "access_token_secret")

    image_url = generate_image.main()
    media_id = upload_image_to_twitter(image_url, consumer_key, consumer_secret, access_token, access_token_secret)
    tweet_with_image(prompt, media_id, consumer_key, consumer_secret, access_token, access_token_secret)


if __name__ == "__main__":
    main()
