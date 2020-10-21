#class for discord user that stores various info while they are playing a game
import time

class User:
	def __init__(self, id, game):
		self.id = str(id)
		self.game = game
		self.last_update = time.time()
	