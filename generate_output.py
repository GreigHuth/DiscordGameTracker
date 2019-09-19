from commands.topgames import topgames
from commands.topusers import topusers
from commands.mygames import mygames
import sys
import  datetime

def generate_output(split_message, message):
    #split_message is an array, [0] is the command name [1] is optional parameter
    # message is required as we need server member data for topusers
    # and we need the id of the person who messaged for mygames and future commands

    # if the havent given a month then it sets the month param to current month
    try:
        month = split_message[1]
    except  IndexError:
        month =  datetime.datetime.now().strftime("%B").upper()


    if split_message[0] not in  ["!topgames", "!topusers", "!help", "!mygames"]:
        output_message = "Invalid command. Try '!help'. " 


    #wanted to do some fancy stuff with dictionaries but it didnt work and tbh, its python so its slow anyway (:
    else:
        if split_message[0] ==  '!topgames':
            output_message = topgames(month)

        if split_message[0] ==  '!topusers':
            output_message = topusers(month, message.channel)

        if split_message[0] ==  '!help':
            output_message = "there is no help"

        if split_message[0] ==  '!mygames':
            output_message = mygames(message.author.id, month)

        

    return output_message