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
        self.inCheck = False
        self.pins = []
        self.checks = []

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
            self.board[move.startRow][move.startCol] = move.pieceMoved      # put piece on starting square
            self.board[move.endRow][move.endCol] = move.pieceCaptured       # put back captured piece
            self.whiteToMove = not self.whiteToMove                         # swap players
            # update the king's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

        """
        All moves with considering checks.
        """

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow=self.whiteKingLocation[0]
            kingCol=self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:                                                            #only 1 check, block check or sove king
                moves = self.getAllPossibleMoves()

                # to block a chuck you must move a piece into one of the squares between the enemy piece and king

                check = self.checks[0] #check information
                checkRow= check[0]
                checkCol= check[1]
                pieceChecking = self.board[checkRow][checkCol]                                 # enemy piece causing the check
                validSquares = []                                                              # squares that pieces can move to
                #if knight, must capture knight or :move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow +check[2]*i, kingCol + check[3]*i)                     # check[2] ,[3] are check direction
                        validSquares.append(validSquares)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:                 # once you get to piece end checks
                            break
                # get rid of any moves that dont block check or move king

                for i in range(len(moves)-1,-1,-1):                                                   # go through backwards when you are removing a list as interating
                    if moves[i].pieceMoved[1] != 'K' :                                                # move doest move king so it must block ot capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares :                   # move doest block check or capture piece
                            moves.remove[moves[i]]
            
            else:                                                                                     # double chech king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        
        else:                                                                                         # not in check so all moves are fine
            moves=self.getAllPossibleMoves()
        return moves

    
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
                    self.moveFunctions[piece]( r, c, moves )                                           #Calls move funtion according to the piece type
        return moves





    def getPawnMoves( self, r, c, moves ):
        """
        Get all the pawn moves for the pawn located at row, col and add the moves to the list.
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] ==c:
                piecePinned =True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:                                                # White pwan moves 
            if self.board[r-1][c] == "--":                                  # 1 Square pawn advance
                if not piecePinned or pinDirection == (-1,0):
                    moves.append( Move( (r, c), (r-1,c), self.board ) )
                    if r==6 and  self.board[r-2][c] == "--":                    # 2 Square pawn advance
                        moves.append( Move( (r,c), (r-2,c), self.board ) )

            if c-1 >= 0:                                                    # Capture Left
                if self.board[r-1][c-1][0] == "b":                          # Enemy piece to capture
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append( Move( (r,c), (r-1,c-1), self.board ) )

            if c+1 <= 7:                                                    # Capture Right
                if self.board[r-1][c+1][0] == "b" :                         # Enemy piece to capture
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append( Move( (r,c), (r-1,c+1), self.board ) )

        else:                                                               #black pawn moves
            if self.board[r + 1][c] == "--":                                # 1 square move
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":                 # 2 square moves
                        moves.append(Move((r, c), (r + 2, c), self.board))
            # captures
            
            if c - 1 >= 0:                                                  # capture to left
                if self.board[r + 1][c - 1][0] == 'w':
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:                                                  # capture to right
                if not piecePinned or pinDirection == (1,1):
                    if self.board[r + 1][c + 1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))


    """
    Get all the rook moves for the ROOKS located at row, col and add the moves to the list.
    """
    def getRookMoves (self, r, c, moves):

        piecePinned = False
        pinDirection = ()
        
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] ==r and self.pins[i][1] == c :
                piecePinned = True 
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':                                          # cant remove queen from pin on rook moves , only remove it on bishop moves
                    self.pins,remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))                                 #up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:                                 # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board [endRow][endCol]
                        if endPiece == "--":                                                # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:                                     # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:                                                               # friendly piece invalid
                            break
                else:                                                                   # off boardbreak
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

        piecePinned = False
        pinDirection = ()
        
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"

        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board [endRow][endCol]
                    if endPiece[0] != allyColor:                                           #not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))
    """
        Get all the bishop moves for the BISHOP located at row, col and add the moves to the list.
    """

    def getBishopMoves (self, r, c, moves):


        piecePinned = False
        pinDirection = ()
        
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))                              # 4 diagnoals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board [endRow][endCol]
                        if endPiece == "--":                                               # empty space valid I
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:                                    # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:                                                              # friendly piece invalid
                            break
                else:                                                                  # off board
                    break
    """
        Get all the king moves for the KING located at row, col and add the moves to the list.
    """      
    def getKingMoves (self, r, c, moves):

        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow <8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:                                                # not an ally piece (empty or enemy piece)
                    # place king on end square check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    
                    inCheck , pins, checks =self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    #place king on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)


    """
        Returns if a player in check, a list of pins, and a list of checks
    """
    
    def checkForPinsAndChecks(self):
        pins = []                                           # squares where allied pinned piece and direction pinned from
        checks = []                                         # squares where enemy is applying check
        inCheck = False
        if self.whiteToMove : 
            enemyColor ="b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else: 
            enemyColor ="w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        # check outward from king for pins and checks, keep track of pins

        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (1,1), (1,-1), (-1,1))

        for j in range( len(directions) ):
            d = directions[j]
            possiblePin = ()                                               # reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])     # 1st allied piece could be pinned
                        else:                                              # 2nd allied piece, so pin or check possible in the direction               
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]                                 
                        """
                        5 possiblities here in this complex conditional
                            1) orthogonally away from king and piece is rook
                            2) diagonally away from king and piece is bishop
                            3) 1 square away diagonally away from king and piece is pawn
                            4) any direction and the piece is queen
                            5) any direction away and the piece is king (neccessary to avoid a king to move to a square controlled by another king)
                        """
                        if ( 0<= j < 3 and type == 'R' ) or (4 <= j and j<=7 and type == 'B') or ( i==1 and type == 'p' and (( enemyColor == 'w' and 6<=j<=7 ) or (enemyColor == 'b' and 4 <= j <= 5))) or ( type == 'Q' ) or ( i==1 and type == 'K'):
                            if possiblePin == ():                                           # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:                                                           # piece blocking so pin
                                pins.append(possiblePin)
                                break

                        else:                                                               # enemy piece not applying check
                            break
                else:
                    break                                                                   # off board
        #check for knight checks
        
        knightMoves = ((-2,-1), (-2,1), (2,1), (2,-1), (1,2), (1,-2), (-1,2), (-1,-2))

        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]

            if 0<= endRow <8 and 0 <= endCol <8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':                       # enemy knight attack
                    inCheck = True
                    checks.append(( endRow, endCol, m[0], m[1]))

        return inCheck,pins,checks


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
