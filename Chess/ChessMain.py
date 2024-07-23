"""
  This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""
#import os

import pygame as p 
import ChessEngine
import ChessAI

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
  animate = False #flag for when we should we animate a move
  loadImages()                                    #only do this once, before the while loop
  running = True
  sqSelected = ()                                 #no square is selected, keep track of the last click of the user (tuple: (row, col))
  playerClicks = []                               #keep track of player clicks (two tuples: [(6, 4), (4, 4)]) moving pwan 2 steps.
  gamOver = False
  playerOne = True
  playerTwo = False
  while running:
    humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
    for e in p.event.get():

      if e.type == p.QUIT:
        runnning = False
      
      #this is for moving the chess pieces.(by clicking the mouse)
      elif e.type == p.MOUSEBUTTONDOWN :
          if not gamOver and humanTurn:
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
                        animate = True
                        sqSelected = ()                      #reset user clicks
                        playerClicks = []
                  if not moveMade:
                      playerClicks = [sqSelected]

      # key handler
      elif e.type == p.KEYDOWN:                    
            if e.key == p.K_z:                     # undo when 'z' is pressed		                   
                gs.undoMove()
                moveMade = True
                animate = False
            if e.key == p.K_z:                     # reset the enitre game(board) when 'r' is pressed		                   
                gs = ChessEngine.GameState()
                ValidMoves = gs.getValidMoves()
                sqSelected = {}
                playerClicks = []
                moveMade = False
                animate = False
      #AI move finder
      if not gamOver and not humanTurn:
         AIMove = ChessAI.findRandomMove(ValidMoves)
         gs.makeMove(AIMove)
         moveMade = True
         animate = True

      if moveMade:
         if animate:
            animateMove(gs.movelog[-1], screen, gs.board, clock)
         ValidMoves=gs.getValidMoves()
         moveMade=False
         animate = False

    drawGameState( screen, gs, ValidMoves, sqSelected)
    if gs.checkmate:
       gamOver = True
       if gs.whiteToMove:
          drawText(screen, 'Black wins by checkmate')
       else:
          drawText(screen, 'White wins by checkmate')
    elif gs.stalemate:
       gamOver = True
       drawText(screen, 'Stalemate')      
    clock.tick( MAX_FPS )
    p.display.flip()


# Highlight square selected and moves for piece selected
def highlightSquares (screen, gs, validMoves, sqSelected):
   if sqSelected != ():
      r, c = sqSelected
      if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
         #highlight selected square
         s = p.Surface((SQ_SIZE, SQ_SIZE))
         s.set_alpha(100) #transperancy value -> transparent; 255 opaque
         s.fill(p.Color('blue'))
         screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
         #highlight moves from that square
         s.fill(p.Color('yellow'))
         for move in validMoves:
            if move.startRow == r and move.startCol == c:
               screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

''' 
  Draw the squares on the board.
'''

def drawGameState( screen, gs , validMoves, sqSelected):
  drawBoard( screen ) 				                        #To draw scores on board 
  highlightSquares (screen, gs, validMoves, sqSelected)
  drawPieces( screen, gs.board )	                    #draw peices on top of squares

'''
  Draw the squares on the board
'''

def drawBoard( screen ):
  global colors
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

def animateMove (move, screen, board, clock):
   global colors
   dR = move.endRow - move.startRow
   dC = move.endCol - move.startCol
   framesPerSquare = 10 #frames to move one square
   frameCount = (abs (dR) +abs(dC)) * framesPerSquare
   for frame in range(frameCount + 1):
      r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
      drawBoard (screen)
      drawPieces (screen, board)
      #erase the piece moved from its ending square
      color = colors [(move.endRow + move.endCol) % 2]
      endSquare =  p. Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
      p.draw.rect(screen, color, endSquare)
      #draw captured piece onto rectangle
      if move.pieceCaptured != '--':
         screen.blit(IMAGES[move.pieceCaptured], endSquare)
      #draw moving piece I
      screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
      p.display.flip()
      clock.tick(60)
def drawText (screen, text):
   font = p.font. SysFont("Helvitca", 32, True, False)
   textObject = font.render(text, 0, p.Color('Gray'))
   textLocation = p. Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
   screen.blit(textObject, textLocation)
   textObject = font.render(text, 0, p.Color('Black'))
   screen.blit(textObject, textLocation.move(2, 2))

if __name__== "__main__":
  main()
