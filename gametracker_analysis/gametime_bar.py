#script to make a bar chart for the given month

import matplotlib.pyplot as plt 
import numpy as np
import sqlite3
import sys
from operator import itemgetter

    
def get_gametimes(month):

    conn = sqlite3.connect("gametime.db")
    cursor = conn.execute('select * from ' + month) # gets all the columns from the db
    
    games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list
    games.pop(0)

    # need to hard code to remove spotify
    if "Spotify" in games:
        games.remove("Spotify")

    totals = [0]*len(games)
    for i in range(len(games)): # puts all the totals in a  list
        
       cursor = conn.execute('select sum('+games[i]+') from '+month)
       totals[i] = cursor.fetchone()[0]# converts total to int
        

    totals = map(lambda x: round(x/3600), totals) # converts all the totals to hours

    game_totals = list(zip(games,totals)) #zips totals with the games then turns it back into a list because it works

    game_totals = sorted(game_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

    return game_totals

plt.rcdefaults()
fig, ax = plt.subplots(figsize=(30,20))

month = sys.argv[1]
games = get_gametimes(month)[:100] #gets top 100 games

names = [game[0] for game in games]
totals = [game[1] for game in games]

y_pos = np.arange(len(names))

ax.barh( y_pos, totals, align='center',alpha=0.5)

for i, v in enumerate(totals):#displays numbers next to the bars
    ax.text(v + 3, i + .25, str(v), fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()
ax.set_xlabel('Time Played (Hours)')
ax.set_title("Game Tracker Data for March")

plt.savefig('gt_march_bar.png')