import os
import sys
import time
from datetime import datetime
import pandas as pd
from clients.draftkings_client import DraftkingsClient


def my_task():
  start_time = datetime.now()
  time.sleep(3)
  return { "start_time": start_time, "end_time": datetime.now() }

def run_simulations(date):
  dk_client = DraftkingsClient()
  df = dk_client.get_available_players()

  limit = 100
  contest_max = 50000
  positions = ["PG", "SG", "SF", "PF", "C", "G", "F", ""]
  lineups = []
  step = 0

  for i in range(limit):
    lineup = { "salary": 0, "fantasy_points": 0 }
    selected_players_ids = []
    for position in positions:
      player_set = df[df['position'].str.contains(position)]
      player = select_player(player_set, selected_players_ids, contest_max - lineup["salary"])
      if player is None:
        break
      new_player = {
        "id": player['playerId'],
        "name": player['displayName'],
        "position": position,
        "fantasy_points": player['projected'],
        "salary": player['salary'],
      }
      lineup[position] = new_player
      lineup["salary"] += player['salary']
      lineup["fantasy_points"] += player['projected']
      selected_players_ids.append(player['playerId'])
    lineup["UTIL"] = lineup.pop('', None)
    if lineup not in lineups:
      lineups.append(lineup)
    step += 1
  
  return { "date": date, "lineups": lineups }
  
def select_player(df, selected_players_ids, salary_remaining):
  available_players = df.loc[~df['playerId'].isin(selected_players_ids)]
  player_set = available_players.loc[available_players["salary"] < salary_remaining]
  if player_set.empty:
    return None
  return player_set.sample(n=1).iloc[0]
