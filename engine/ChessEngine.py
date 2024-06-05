"""
	This class is responsible for storing all the information about the current state of chess game. 
	It will also be responsible for determining the valid moves at the current state.
	It will also keep move log.
"""

class GameState():
	def __init__(self):
		"""
			2x2 List for 2d board of size 8x8
			Contains Color and type of the piece
			1st char of each element => Color
			2nd char => Type
		"""

		self.board= [
					["bR","bN","bB","bQ","bK","bB","bN","bR"],
					["bp","bp","bp","bp","bp","bp","bp","bp"],
					["--","--","--","--","--","--","--","--"],
					["--","--","--","--","--","--","--","--"],
					["--","--","--","--","--","--","--","--"],
					["--","--","--","--","--","--","--","--"],
					["wp","wp","wp","wp","wp","wp","wp","wp"],
					["wR","wN","wB","wQ","wK","wB","wN","wR"]
					]
		self.whiteToMove = True
		self.movelog=[]