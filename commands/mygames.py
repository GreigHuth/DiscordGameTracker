import sqlite3
from discord.utils import find
import datetime
from operator import itemgetter



#command that lets people see thier own personal gametimes
def mygames(id, month):

    conn = sqlite3.connect("gametime.db")
    cursor = conn.execute('select * from ' +month+ ',where ID = ' +id)


    games = [game[0] for game in cursor.description]

