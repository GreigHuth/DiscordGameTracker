import sqlite3
from discord.utils import find
import datetime
from operator import itemgetter

#command that lets people see thier own personal gametimes
def mygames(id, month):

    conn = sqlite3.connect("gametime.db")

    cursor = conn.execute('select * from ' +month+ ',where ID = ' +id)
    times = [time[0] for time in cursor.description]
    times.pop(0)

    cursor = conn.execute('select * from '+month)
    games = [game[0] for game in cursor.description]

    if "Spotify" in games:
        games.remove("Spotify")

    times = filter(lambda x: x == 0, times) # removes 0 entries 
    times =  map(lambda x: x/3600, times) # converts all the times to seconds 
    
    game_times = list(zip(games,times))

    game_times = sorted(game_times,key=itemgetter(1), reverse = True) # sorts the list in descending order


    #begin constructing message
    message = "Top games for YOU in %s:\n```" %(month.lower())
    
    for game in game_times:
        message += "%s - {0:.2f}hours\n".format(game[1]) % game[0]

    return message



