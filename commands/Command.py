from config.config import EMBED_COLOUR, EMBED_URL
import math
from abc import abstractmethod

class Command:
    

    def __init__(self, conn, g_filter):
        self.max = 10 #max number of things outputted when the command is called
        self.conn = conn #database connection
        self.EMBED_COLOUR = EMBED_COLOUR
        self.filter = g_filter # list of games to filter out of output

    @abstractmethod
    def execute(self, user_id):
        pass

        #builds the message returned by mygames and topgames, topusers is a special case
    def construct_response(self, totals):
            i = 1
            response = ""
            for item, time  in totals:
                hours = math.floor(time)
                minutes = round((time - hours)*60)
                response += "{}: {} - {} hours {} minutes  \n\n".format(i,item,hours,minutes) 
                i += 1

                if i > self.max:
                    break
                
                return response   
        



