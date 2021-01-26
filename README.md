# GameTracker Bot

GameTracker bot is a bot that keeps track of all the games being played by different people in your discord server and how long they 
have been played for on a month by month basis.

EXAMPLE:
```
discord_user: !topgames 

GameTracker:  Top 10 games played in <current_month> (in hours):

              ApexLegends - 18.77 hours played
              
              LeagueofLegends - 15.43 hours played
              
              Fortnite - 8.56 hours played
              
              Minecraft - 8.09 hours played
              
              Overwatch - 6.46 hours played
             
```

## Why would i want this?

GameTracker was built to achieve two things:  
1. To allow server owners of large communities to (somewhat) answer "What does your community play?".  
2. To allow users to make decisions on what to play based on what the other people in the server are playing.

## Current Commands:  
`!topgames` - displays the games with the highest playtime in the current month.    
`!topusers` - displays the users that have the highest playtime in the current month.  
`!mygames`  -  displays your playtime for this month.  
`!help` -  output is above

## Prerequisites
* python 3.6
* virtualenv
* pip

## Install


**Set up virtualenv**

`virtualenv -p $(which python3) .venv`

`source .venv/bin/activate`

 To exit the virtualenv just run  
`deactivate`
 

**Install dependencies**

`pip install -r requirements.txt`

**Next, add your discord token in the config.py file.**

**Then, run:**

`python gametracker.py`

## Possible new features

Game suggestions???

### Get in touch
If you'd like to add GameTracker to your server or have any critisisms/ideas please PM Gurg#6315 on discord or email me at gurg@edingamesoc.co.uk
