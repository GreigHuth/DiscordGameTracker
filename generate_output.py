from commands.topgames import topgames
from commands.topusers import topusers
from commands.mygames import mygames
import re
import sys
import datetime




def generate_output(command, conn):

    #some commands have args so split message by space into array so its easier to deal with later  
    split_message = command.content.split()

    try:
        month = split_message[1]
    except  IndexError:
        month =  datetime.datetime.now().strftime("%B").upper()

    #remove all non-alphanumeric characters to stop those sneaky hackers
    month = re.sub(r'\W+', '', month)


    #i should clean this up
    if split_message[0] ==  '!topgames':
        output_message = topgames(month, conn)

    if split_message[0] ==  '!topusers':
        output_message = topusers(month, command.channel, conn)

    if split_message[0] ==  '!help':
        output_message = "there is no help"

    if split_message[0] ==  '!mygames':
        output_message = mygames(str(command.author.id), month, conn)

        

    return output_message