"""
  This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""
#import os

import pygame as p 
import ChessEngine


WIDTH = HEIGHT = 512 
DIMENSION = 8                                                                   #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15                                                                     #For animations later on
IMAGES = {}

"""
  Initialize a global dictionary of images. This will be called exactly once in the main
"""

def loadImages():

  pieces=["wR","wp","wB","wQ","wK","wN","bp","bR","bB","bQ","bK","bN"]
  for piece in pieces:
    s = "chess" + "/" + "images/" + piece + ".png"
    IMAGES[ piece ] = p.transform.scale( p.image.load(s), ( SQ_SIZE, SQ_SIZE ) )

#Note: we can access an image by saying 'IMAGES
''' 
  The main driver for our code. This will handle user input and updating the graphics
'''

def main():

  p.init()
  screen = p.display.set_mode( ( WIDTH, HEIGHT ) )
  clock = p.time.Clock()
  screen.fill( p.Color( "white" ) )
  gs = ChessEngine.GameState()
  ValidMoves = gs.getValidMoves()
  moveMade = False                                #flag variable for when a move is made
  loadImages()                                    #only do this once, before the while loop
  running = True
  sqSelected = ()                                 #no square is selected, keep track of the last click of the user (tuple: (row, col))
  playerClicks = []                               #keep track of player clicks (two tuples: [(6, 4), (4, 4)]) moving pwan 2 steps.

  while running:

    for e in p.event.get():

      if e.type == p.QUIT:
        runnning = False
      
      #this is for moving the chess pieces.(by clicking the mouse)
      elif e.type == p.MOUSEBUTTONDOWN :

          location = p.mouse.get_pos()            #(x, y) location of mouse
          col = location[0] // SQ_SIZE            
          row = location[1] // SQ_SIZE       

          if sqSelected == ( row, col):            #the user clicked the same square twice
              sqSelected = ()                     #deselect
              playerClicks = []                   #clear player clicks

          else:
              sqSelected= (row, col)
              playerClicks.append(sqSelected)     #append for both 1st and 2nd clicks

          if len(playerClicks) == 2:              #after 2nd click

              move = ChessEngine.Move( playerClicks[0], playerClicks [1], gs.board )
              print( move.getChessNotation() )
              for i in range(len(ValidMoves)):
                if move == ValidMoves[i]:
                    gs.makeMove( ValidMoves[i] )
                    moveMade=True

                    sqSelected = ()                      #reset user clicks
                    playerClicks = []
              if not moveMade:
                  playerClicks = [sqSelected]

      # key handler
      elif e.type == p.KEYDOWN:                    
            if e.key == p.K_z:                     # undo when 'z' is pressed		                   
                gs.undoMove()
                moveMade = True
     
      if moveMade:
         ValidMoves=gs.getValidMoves()
         moveMade=False

    drawGameState( screen, gs )
    clock.tick( MAX_FPS )
    p.display.flip()

''' 
  Draw the squares on the board.
'''

def drawGameState( screen, gs ):
  drawBoard( screen ) 				                        #To draw scores on board 
  drawPieces( screen, gs.board )	                    #draw peices on top of squares

'''
  Draw the squares on the board
'''

def drawBoard( screen ):
  colors = [p.Color("white"), p.Color("#B6A09F")]
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      color = colors[ ( (r+c) % 2) ]
      p.draw.rect( screen, color, p.Rect( c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE ) )

'''
  Draw pieces on board using the current GameState.board
''' 

def drawPieces( screen, board ):
  for r in range( DIMENSION ):
    for c in range( DIMENSION ):
      piece = board[r][c]
      # If not empty square
      if piece != "--": 
        screen.blit( IMAGES[ piece ], p.Rect( c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE ) )


if __name__== "__main__":
  main()

