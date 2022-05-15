import json
from utils.config import Configs
from utils.utilities import Requester,Log
import enum

class MessageImportanceLevel(enum.Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    VULNERABLE=4

class Slack:
    __url=Configs.ConstSlackWebHook
    __json_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": "",
                        "value": "",
                        "short": "false",
                    }
                ]
            }
            ]
          }
    @staticmethod
    def send(msg,title,importance=MessageImportanceLevel.INFO):
        Slack.slack_data["attachments"][0]["fields"][0]["value"]=msg
        Slack.slack_data["attachments"][0]["fields"][0]["title"]=title
        
        if(importance==MessageImportanceLevel.INFO or importance==MessageImportanceLevel.WARNING):
            Slack.slack_data["icon_emoji"]=":large_blue_square:"
        elif(importance==MessageImportanceLevel.ERROR):
            Slack.slack_data["icon_emoji"]=":large_yellow_square:"
        elif(importance==MessageImportanceLevel.VULNERABLE):
            Slack.slack_data["icon_emoji"]=":large_red_square:"
        else:
            Slack.slack_data["icon_emoji"]=":large_purple_square:"
        headers = {'Content-Type': "application/json"}
        requester_obj=Requester()
        requester_obj.HEADERS=headers
        response = requester_obj.send_post(url=Slack.__url,data=Slack.__json_data,auth=None,json=None)
        if(response.status_code!=200):
            Log.info(response.text)
