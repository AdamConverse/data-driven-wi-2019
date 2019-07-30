import os
from datetime import date
from slackclient import SlackClient as slack_client

class SlackClient:
  def __init__(self):
    self.client = slack_client(os.environ["SLACK_API_TOKEN"])
    self.channel = os.environ["SLACK_CHANNEL_ID"]

  def post(self, num_games, date):
    url = "https://data-driven-wi-2019-1.herokuapp.com/run-simulations/{}".format(date)
    self.client.api_call(
      "chat.postMessage",
      channel=self.channel,
      text="<!here> {} games slated for {}.".format(num_games, date),
      attachments= [
        {
          "fallback": "*Run Simulations:* {}".format(url),
          "actions": [
            {
              "type": "button",
              "text": "Run Simulations :robot_face:",
              "url": url
            }
          ]
        }
      ]
    )

  def has_posted(self, date):
    rsp = self.client.api_call(
      "conversations.history",
      channel=self.channel
    )
    for message in rsp["messages"]:
      if date in message["text"]:
        return message["ts"]
    return None
