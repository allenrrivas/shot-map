import matplotlib.pyplot as plt
from matplotlib.patheffects import withSimplePatchShadow
import numpy as np
import pandas as pd
import mplcursors
from highlight_text import fig_text
from mplsoccer import VerticalPitch

import requests
from bs4 import BeautifulSoup
import json
import re

import sys

def playerShots():
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        shot_type = sys.argv[2]
    else:
        # Use Vinicius Jr. as a fall back
        url = 'https://understat.com/player/7008'
        shot_type = "Goals"
        
    link = url
    res = requests.get(link)
    soup = BeautifulSoup(res.content,'lxml')
    scripts = soup.find_all('script')
    # Get the grouped stats data, it's the second script executed in order
    strings = scripts[3].string
    # Getting rid of unnecessary characters from json data
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')
    data = json.loads(json_data)
    
    # Get name of player from <title>
    name = soup.title.string
    name_list = name.split()

    shots = pd.DataFrame(data)

    # Changing data type
    shots['xG'] = shots['xG'].astype('float64')
    shots['X'] = shots['X'].astype('float64')
    shots['Y'] = shots['Y'].astype('float64')

    # Multiple X and Y by 100, to fit axes
    shots['X'] = (shots['X'])*100
    shots['Y'] = (shots['Y'])*100

    # New dictionaries 
    total_shots = shots[shots.columns[0]].count().tolist()
    xGcumsum = np.round(max(np.cumsum(shots['xG'])),3).tolist()
    xG_per_shot = np.round(max(np.cumsum(shots['xG']))/(shots[shots.columns[0]].count()),3).tolist()
    
    # Get all Goals (Dataframe)
    goal_df = shots[shots['result']=='Goal']
    # Get all Shots on post (Dataframe)
    shot_on_post_df = shots[shots['result']=='ShotOnPost']
    # Get all saved shots (Dataframe)
    saved_shot_df = shots[shots['result']=='SavedShot']
    # Get all blocked shots (Dataframe)
    blocked_shot_df = shots[shots['result']=='BlockedShot']
    # Get all missed shots (Dataframe)
    missed_shot_df = shots[shots['result']=='MissedShots']
    # Count number of goals
    goals = goal_df[goal_df.columns[0]].count().tolist()

    pitch = VerticalPitch(half=True, pitch_type='opta', pitch_color='#22312b', line_color='#ffffff', axis=False)
    fig, ax = pitch.draw(figsize=(12, 9))
    
    if shot_type == "Goals":
        goal_ax = plt.scatter(goal_df['Y'], goal_df['X'], s=(goal_df["xG"]* 720) + 100, c='#2ecc71', label='Goals', alpha=.7)
    elif shot_type == "ShotsOnPost":
        shot_on_post_ax = plt.scatter(shot_on_post_df['Y'], shot_on_post_df['X'], s=shot_on_post_df["xG"]* 720, c='#f1c40f', label='Shots On Post', alpha=.7)
    elif shot_type == "SavedShots":
        saved_shot_ax = plt.scatter(saved_shot_df['Y'], saved_shot_df['X'], s=saved_shot_df["xG"]* 720, c='#3498db', label='Saved Shots', alpha=.7)
    elif shot_type == "BlockedShots":
        blocked_shot_ax = plt.scatter(blocked_shot_df['Y'], blocked_shot_df['X'], s=blocked_shot_df["xG"]* 720, c='#9b59b6', label='Blocked Shots', alpha=.7)
    elif shot_type == "MissedShots":
        missed_shot_ax = plt.scatter(missed_shot_df['Y'], missed_shot_df['X'], s=(missed_shot_df["xG"]* 720), c='#e74c3c', label='Missed Shots', alpha=.7)

    bbox_pad = 2
    bboxprops = {'linewidth': 0, 'pad': bbox_pad}

    s="<{} {} Career Shots>".format(name_list[0], name_list[1])
    highlight_textprops =[{'color': '#ffffff', 'weight': 'bold', 'bbox': {'facecolor':'#22312b', **bboxprops}}]
    fig_text(s=s,
            x=0.27,y=0.15,
            highlight_textprops=highlight_textprops,
            fontname='monospace',
            fontsize=24
    )

    fig_text(x=0.42, y=0.37, s="Shots:\n\nxGcumsum:\n\nxG per shot:\n\nGoals: ", fontsize = 12, fontweight = "bold", c='#ffffff')
    fig_text(x=0.52, y=0.37, s="<{}\n\n{}\n\n{}\n\n{}>".format(total_shots,xGcumsum,xG_per_shot,goals), fontsize = 12, fontweight = "bold", c='#2ecc71')
    
    plt.show()


if __name__ == "__main__":
    playerShots()