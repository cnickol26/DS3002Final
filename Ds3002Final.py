# -*- coding: utf-8 -*-

# -- Sheet --

!pip install tweepy
import tweepy 

# Authenticate to Twitter
auth = tweepy.OAuthHandler("7YiG9tBjQ401S4iTJ6DlXdDWf", "e35ilb5uGN52MYe366RVRunxWwqGZidIKV5chnfdM0e3CWLcCr")
auth.set_access_token("1243684016454328321-SMz9y75H5Bo4a5EDfg2A6UHPeQ5Dt4", "rQ3HY3ihjb6CfabS1ZOTKy3du67kOBOgnxeySSuku0uob")

# Create API object
api = tweepy.API(auth)


# Create a tweet
api.update_status("Test tweet from Tweepy Python")

!pip install tweepy
import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    consumer_key = "7YiG9tBjQ401S4iTJ6DlXdDWf"
    consumer_secret = "e35ilb5uGN52MYe366RVRunxWwqGZidIKV5chnfdM0e3CWLcCr"
    access_token = "1243684016454328321-SMz9y75H5Bo4a5EDfg2A6UHPeQ5Dt4"
    access_token_secret = "rQ3HY3ihjb6CfabS1ZOTKy3du67kOBOgnxeySSuku0uob"

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api




!pip install tweepy
import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Please reach us via DM",
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()

