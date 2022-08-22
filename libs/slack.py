from cgitb import text
from email import message
import slackweb
from typing import List
from libs import create_message

def client_info(webhook_url:str) -> slackweb.Slack:
    '''
        slackに通知するためのオブジェクトを生成する

        Args:
            webhook_url (str): Webhook URL
        
        Returns:
            slackに通知するためのオブジェクト
    '''

    return slackweb.Slack(url=webhook_url)

def post_message(slack:slackweb.Slack,message:str):
    '''
        slackに通知を送る

        Args:
            slack (slackweb.Slack): slackに通知するためのオブジェクト
            message (str): 通知をするメッセージ
    '''
    slack.notify(text=message)

def execute_slack(webhook_url:str,new_performance:List[map]):
    '''
        slackに通知をする一連の処理を行う

        Args:
            webhook_url (str): Webhook URL
            new_performance (List[map]): 通知する成績
    '''
    message = create_message.create_performance_message(new_performance)
    post_message(client_info(webhook_url),message)