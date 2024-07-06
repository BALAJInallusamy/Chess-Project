"""
  This class is responsible for storing all the information about the current state of chess game. 
  It will also be responsible for determining the valid moves at the current state.
  It will also keep move log.
"""

class GameState():
    def __init__( self ):
        """
          2x2 List for 2d board of size 8x8
          Contains Color and type of the piece
          1st char of each element => Color
          2nd char => Type
        """

        self.board = [
              ["bR","bN","bB","bQ","bK","bB","bN","bR"],
              ["bp","bp","bp","bp","bp","bp","bp","bp"],
              ["--","--","--","--","--","--","--","--"],
              ["--","--","--","--","--","--","--","--"],
              ["--","--","--","--","--","--","--","--"],
              ["--","--","--","--","--","--","--","--"],
              ["wp","wp","wp","wp","wp","wp","wp","wp"],
              ["wR","wN","wB","wQ","wK","wB","wN","wR"]
              ]
        self.moveFunctions = { 'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves,
                               'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves }
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation=(7, 4)
        self.blackKingLocation=(0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove( self, move ):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)                                       #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove                         #swap players
        # update king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
  
    def undoMove( self ):
        if len(self.movelog) != 0:                                          # make sure that there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove                         # swap players
            # update the king's position if needed
            if move.pieceMoved == "wK":
             self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)
        """
        All moves with considering checks.
        """
    def getValidMoves( self ):
        
        #1) generate all possible moves
        moves= self.getAllPossibleMoves()
        #2)for each move, make a move
        
        for i in range(len(moves)-1, -1, -1):  # iterate through the list backwards when removing elements
            self.makeMove(moves[i])
            
        #3)generate all opponenets's moves
            
        #4)for each of your oppenent moves, check if they attack your king
            self.whiteToMove= not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5)if they attack your king, then its not a valid move
            self.whiteToMove= not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                # TODO stalemate on repeated moves
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves 
        """
        Determine if a current player is in check
        """
    def inCheck(self):
           
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        """
        Determine if enemy can attack the square row col   
        """
        
    def squareUnderAttack(self, r, c):
       
        self.whiteToMove = not self.whiteToMove  # switch to opponent's point of view
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False
    
    def getAllPossibleMoves( self ):
        """
        All moves without considering checks.
        """
        moves = []
        for r in range( len(self.board) ):                                                             # NUmber of rows
            for c in range( len(self.board[r]) ):                                                      # NUmber of cols
                turn = self.board[r][c][0]
                if ( turn == "w" and self.whiteToMove ) or ( turn == "b" and not self.whiteToMove ):     
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece]( r, c, moves );                                        #Calls move funtion according to the piece type
        return moves
  
    def getPawnMoves( self, r, c, moves ):
        """
        Get all the pawn moves for the pawn located at row, col and add the moves to the list.
        """
        if self.whiteToMove:                                                # White pwan moves 
            if self.board[r-1][c] == "--":                                  # 1 Square pawn advance
                moves.append( Move( (r, c), (r-1,c), self.board ) )
                if r==6 and  self.board[r-2][c] == "--":                    # 2 Square pawn advance
                    moves.append( Move( (r,c), (r-2,c), self.board ) )

            if c-1 >= 0:                                                    # Capture Left
                if self.board[r-1][c-1][0] == "b":                          # Enemy piece to capture
                    moves.append( Move( (r,c), (r-1,c-1), self.board ) )

            if c+1 <= 7:                                                    # Capture Right
                if self.board[r-1][c+1][0] == "b" :                         # Enemy piece to capture
                    moves.append( Move( (r,c), (r-1,c+1), self.board ) )

        else: #black pawn moves
            if self.board[r + 1][c] == "--": # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--": # 2 square moves
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures
            if c - 1 >= 0: # capture to left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7: # capture to right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    """
    Get all the rook moves for the ROOKS located at row, col and add the moves to the list.
    """
    def getRookMoves (self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board [endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off boardbreak
                    break
    
    """
        Get all the queen moves for the QUEEN located at row, col and add the moves to the list.
    """
    def getQueenMoves (self, r, c, moves):
        self.getRookMoves (r, c, moves) 
        self.getBishopMoves (r, c, moves)

    """
        Get all the knight moves for the KNIGHTS located at row, col and add the moves to the list.
    """
    def getKnightMoves (self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board [endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    """
        Get all the bishop moves for the BISHOP located at row, col and add the moves to the list.
    """
    def getBishopMoves (self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # 4 diagnoals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board [endRow][endCol]
                    if endPiece == "--": # empty space valid I
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break
    """
        Get all the king moves for the KING located at row, col and add the moves to the list.
    """      
    def getKingMoves (self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):endRow = r + kingMoves[i][0]
        endCol = c + kingMoves[i][1]
        if 0 <= endRow <8 and 0 <= endCol < 8:
            endPiece = self.board [endRow][endCol]
            if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                moves.append(Move((r, c), (endRow, endCol), self.board))
       
class Move():
    #maps keys to values
    #key value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__( self, startSq, endSq, board ):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 
        #print(self.moveID)
    
    def __eq__( self, other ):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation( self ):
        #you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile( self, r, c ):
      return self.colsToFiles [c] + self.rowsToRanks [r]
