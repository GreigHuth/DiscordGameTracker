from commands.topgames import topgames
from commands.topusers import topusers
from commands.mygames import mygames
import sys
import  datetime

def generate_output(input, message):
    #input is an array, [0] is the command name [1] is optional parameter
    # message is required as we need server member data for topusers
    # and we need the id of the person who messaged for mygames and future commands

    # if the havent given a month then it sets the month param to current month
    try:
        month = input[1]
    except  IndexError:
        month =  datetime.datetime.now().strftime("%B").upper()


    if input[0] not in  ["!topgames", "!topusers", "!help", "!mygames"]:
        output_message = "Invalid command. Try '!help'. " 


    else:
        options = { "!topgames" : topgames(month),
                    "!topusers" : topusers(month, message.channel),
                    "!help"     : "`!topgames [limit] [month]`",
                    "!mygames"  : mygames(month),
 
        }

        output_message = options[input[0]]()

    return output_message