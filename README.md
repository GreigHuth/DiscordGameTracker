# GameTracker Bot

GameTracker bot is a bot that keeps track of all the games being played by different people in your discord server and how long they 
have been played for on a month by month basis.

EXAMPLE:
```
discord_user: !topgames5

GameTracker:  Top 5 games played in MARCH (in hours):
              ApexLegends - 18.77 hours played
              LeagueofLegends - 15.43 hours played
              Spotify - 8.56 hours played
              RuneLite - 8.09 hours played
              Overwatch - 6.46 hours played
             
```

## Why would i want this?

GameTracker was built to achieve two things:  
1. To allow server owners of large communities to (somewhat) definitively answer "What does your community play?".  
2. To allow users to make decisions on what to play based on what the other people in the server are playing.

## Current Commands:  
`!topgames10 or !topgames5` - Displays the top 10 or top 5 games played that month
`!help` -  Says a little joke then informs the user that !topgames is the only command.

## Prerequisites
* python 3.6
* virtualenv
* pip

## Install


**Set up virtualenv**

`virtualenv -p $(which python3.6) .venv`

`source .venv/bin/activate`

 To exit the virtualenv just run  
`deactivate`
 

**Install dependencies**

`pip install -r requirements.txt`

**Next, add your discord token in the config.py file.**

**Then, run:**

`python gametracker.py`

## Possible new features

Add the functionality to allow users to PM the bot and get thier own personal playtime data.  
Better formatting for the output.

### Get in touch
If you'd like to add GameTracker to your server or have any critisisms/ideas please PM Gurgashaska#6315 on discord.
