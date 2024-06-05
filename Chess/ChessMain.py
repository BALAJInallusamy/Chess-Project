"""
	This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""
import pygame as p 
import ChessEngine


WIDTH = HEIGHT = 512 
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #For animations later on
IMAGES = {}
"""
	Initialize a global dictionary of images. This will be called exactly once in the main
"""
def loadImages():
	pieces=["wp","wR","wB","wQ","wK","wN","bp","bR","bB","bQ","bK","bN"]
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))
#Note: we can access an image by saying 'IMAGES
''' 
	The main driver for our code. This will handle user input and updating the graphics
'''
def main():
	p.init()
	screen = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	gs = ChessEngine.GameState()
	loadImages() #only do this once, before the while loop
	runnning = True
	while runnning:
		for e in p.event.get():
			if e.type == p.QUIT:
				runnning = False

		clock.tick(MAX_FPS)
		p.display.flip()

''' 
	Draw the squares on the board.
'''

def drawGameState(screen,gs):
	drawBoard(screen) 				#To draw scores on board 
	drawPieces(screen, gs.board)	#draw peices on top of squares

'''
	Draw the squares on the board
'''

def drawBoard(screen):
	colors = [p.Color("white"), p.Color("gray")]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[((r+c) % 2)]
			p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
	Draw pieces on board using the current GameState.board
''' 

def drawPieces(screen,board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			# If not empty square
			if piece != "--": 
				screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__=="__main__":
	main()
