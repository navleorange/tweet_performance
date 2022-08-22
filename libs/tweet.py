from typing import List
import tweepy
from pprint import pprint
from libs import create_message

def client_info(api_key:str,api_key_secret:str,bearer_token:str,access_token:str,access_token_secret:str) -> tweepy.Client:
    '''
        APIを呼び出すための情報を登録する

        Args:
            api_key (srt): Twitter API KEY
            api_key_secret (srt): Twitter API SECRET KEY
            bearer_token (srt): Twitter BEARER TOKEN
            access_token (srt): Twitter ACCESS TOKEN
            access_token_secret (srt): Twitter ACCESS TOKEN SECRET

        Returns:
            tweepy.Client: APIを呼び出すための情報を登録したオブジェクト
    '''

    client = tweepy.Client(consumer_key    = api_key,
                           consumer_secret = api_key_secret,
                           bearer_token    = bearer_token,
                           access_token    = access_token,
                           access_token_secret = access_token_secret,
                          )
    return client

def create_tweet_message(client:tweepy.Client,message:str):
    '''
        ツイートするメッセージを作成する

        Args:
            client (tweepy.Client): APIを呼び出すための情報を登録したオブジェクト
            message (str): ツイートする内容
        
        Returns
            tweet: ツイートするメッセージ
    '''

    tweet = client.create_tweet(text=message)
    return tweet

def execute_tweet(api_key:str,api_key_secret:str,bearer_token:str,access_token:str,access_token_secret:str,new_performance:List[map]):
    '''
        更新された成績をツイートする一連の動作を行う

        Args:
            api_key (srt): Twitter API KEY
            api_key_secret (srt): Twitter API SECRET KEY
            bearer_token (srt): Twitter BEARER TOKEN
            access_token (srt): Twitter ACCESS TOKEN
            access_token_secret (srt): Twitter ACCESS TOKEN SECRET
            new_performance (List[map]): 更新された成績
    '''

    client = client_info(api_key,api_key_secret,bearer_token,access_token,access_token_secret)
    pprint(create_tweet_message(client,create_message.create_performance_message(new_performance)))