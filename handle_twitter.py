import os
import subprocess
from requests_oauthlib import OAuth1Session
import json
import time

def send_tweet(text: str):
    
    payload = {"text": text}
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    if access_token is None or access_token_secret is None:
        print("ACCESS_TOKEN and/or ACCESS_TOKEN_SECRET are not set. Setting them now.")

        # Get request token
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]
        
        # Assuming new_access_token and new_access_token_secret variables hold new values
        subprocess.run(["setx", "ACCESS_TOKEN", access_token])
        subprocess.run(["setx", "ACCESS_TOKEN_SECRET", access_token_secret])
    else:
        print("access tokens found, sending tweet.")

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    print("Response code: {}".format(response.status_code))
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

def tweet():
    text = ""
    print("tweet")
    while True:
        user_input = input("> ")
        if user_input == "":
            text += "\n"
        elif user_input == "send":
            break
        elif user_input == "cancel":
            return ValueError
        else:
            text += ("" if text == "" else "\n") + user_input
    send_tweet(text)
