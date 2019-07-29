import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import requests
import pandas
from pandas.io.json import json_normalize


class DraftkingsClient:
  def __init__(self):
    self.test_mode = True
    self.draft_group = self.get_draft_group()
    self.contest_type = self.get_contest_type()

  def get_draft_group(self):
    """Retrieve Draftkings DraftGroupID."""
    if self.test_mode:
      with open("draftkings/draft_group.json") as json_file:
        r = json.load(json_file)
    else:
      r = requests.get("https://www.draftkings.com/lobby/getcontests?sport=nba").json()
    for contest in r["Contests"]:
      if contest["mec"] is 150:
        return contest["dg"]
    return r["Contests"][0]["dg"]

  def get_contest_type(self):
    """Retrieve Draftkings ContestType."""
    if self.test_mode:
      with open("draftkings/contest_type.json") as json_file:
        r = json.load(json_file)
    else:
      r = requests.get("https://api.draftkings.com/draftgroups/v1/{}?format=json".format(self.draft_group)).json()
    return r["draftGroup"]["contestType"]["contestTypeId"]

  def get_available_players(self):
    if self.test_mode:
      with open("draftkings/available_players.json") as json_file:
        r = json.load(json_file)
    else:
      r = requests.get("https://api.draftkings.com/draftgroups/v1/draftgroups/{}/draftables".format(self.draft_group)).json()
    df = pandas.DataFrame(r["draftables"])
    df = df[['displayName', 'draftableId', 'playerId', 'draftStatAttributes', 'position', 'rosterSlotId', 'salary', 'teamAbbreviation', 'teamId']]
    df['projected'] = df['draftStatAttributes'].apply(lambda x: x[0]["value"] if x[0]["id"] is 219 else x[1]["value"])
    df = df.drop(['draftStatAttributes'], axis=1)
    df.drop_duplicates('playerId', inplace=True)
    return df