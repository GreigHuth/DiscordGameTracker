#class for discord user that stores various info while they are playing a game

class User:
	def __init__(self, id, game, start, end):
		self.id = id
		self.game = game
		self.start = start
		self.end = end
	