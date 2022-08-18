import os
from dotenv import load_dotenv
from typing import List
import tweepy
import datetime
from pprint import pprint

def client_info(api_key:str,api_key_secret:str,bearer_token:str,access_token:str,access_token_secret:str) -> tweepy.Client:
    client = tweepy.Client(consumer_key    = api_key,
                           consumer_secret = api_key_secret,
                           bearer_token    = bearer_token,
                           access_token    = access_token,
                           access_token_secret = access_token_secret,
                          )
    return client

def create_tweet_message(client:tweepy.Client,message:str):
    tweet = client.create_tweet(text=message)
    return tweet

def create_performance_message(new_performance:List[map]) -> str:
    get_time = str(datetime.datetime.now())
    get_time = get_time[:str(datetime.datetime.now()).find(".")]
    get_time = get_time.replace(" ","  ")
    message = "------------------自動更新------------------\n"
    message += "取得時間：" + get_time + "\n"
    message += "以下の教科の成績が更新されました\n"

    for performance in new_performance:
        message += "\n" + performance[0]
    
    return message

def execute_tweet(api_key:str,api_key_secret:str,bearer_token:str,access_token:str,access_token_secret:str,new_performance:List[map]):
    client = client_info(api_key,api_key_secret,bearer_token,access_token,access_token_secret)
    pprint(create_tweet_message(client,create_performance_message(new_performance)))