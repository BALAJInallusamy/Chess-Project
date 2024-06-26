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

    def makeMove( self, move ):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)                                       #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove                         #swap players
  
    def undoMove( self ):
        if len(self.movelog) != 0:                                          # make sure that there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove                         # swap players

    def getValidMoves( self ):
        """
        All moves with considering checks.
        """
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves( self ):
        """
        All moves without considering checks.
        """
        moves = [ Move( (6,4), (4,4), self.board ) ]
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

        else:                                                               # Black Pwan moves
            pass




    def getRookMoves( self, r, c, moves ):
        """
        Get all the rook moves for the ROOKS located at row, col and add the moves to the list.
        """
        pass 
    def getKnightMoves( self, r, c, moves ):
        """
        Get all the rook moves for the KNIGHTS located at row, col and add the moves to the list.
        """
        pass 
    def getQueenMoves( self, r, c, moves ):
        """
        Get all the rook moves for the QUEEN located at row, col and add the moves to the list.
        """
        pass 
    def getKingMoves( self, r, c, moves ):
        """
        Get all the rook moves for the KING located at row, col and add the moves to the list.
        """
        pass  
    def getBishopMoves( self, r, c, moves ):
        """
        Get all the rook moves for the BISHOP located at row, col and add the moves to the list.
        """
        pass 

            
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
        print(self.moveID)
    
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
