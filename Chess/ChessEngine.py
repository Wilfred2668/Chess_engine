'''
The following class contains:
1. Used to maintain current game state
2. Make a move
3. Generate all the valid moves
4. Generate moves for each and every piece
'''

class GameState():
    def __init__(self):
        # maintain board state in list
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves} # map all the pieces to their move generation function
        self.whiteToMove = True # track whose move it is white or black
        self.moveLog = [] # maintains move logs
        self.blackKingLocation = (0,4) # Keeps track of black king
        self.whiteKingLocation = (7,4) # Keeps track of white king
        self.inCheck = False
        self.checks = []
        self.pins = []
        # self.checkMate = False
        # self.staleMate = False

    '''
    Makes moves by:
    1. Making start square empty '--'
    2. move the piece from start square to end square
    3. append the move to move log
    4. change move to opponent by setting whiteToMove as not whiteToMove
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # Update kings location if moved
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)


    '''
    Undoing a move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # Update kings location if needed
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)

    # =========================================================================
    # [DEPRECATED / REFERENCE ONLY] Naive Move Generation Algorithm
    # Methods: getValidMoves (naive), isCheck, squareUnderAttack
    # =========================================================================
    # '''
    # All moves considering check
    # '''
    # def getValidMoves(self):
    #     # 1. Generate all possible moves
    #     moves = self.getAllPossibleMoves()

    #     # 2. for each move, make a move
    #     for i in range(len(moves)-1, -1, -1):
    #         self.makeMove(moves[i])
    #         # 3. generate all the opponents move
    #         # 4. for each of your opponents moves, see if they attack your king
    #         # 5. if they do attack your king not a valid move
    #         self.whiteToMove = not self.whiteToMove
    #         if self.isCheck():
    #             moves.pop(i)
    #         self.whiteToMove = not self.whiteToMove
    #         self.undoMove()

    #     if len(moves) == 0: # either checkmate or stalemate
    #         if self.isCheck():
    #             self.checkMate = True
    #         else:
    #             self.staleMate = True
    #     else:
    #         self.checkMate = False
    #         self.staleMate = False
    #     return moves

    # '''
    # Determine if current player is in check
    # '''
    # def isCheck(self):
    #     if self.whiteToMove:
    #         return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    # '''
    # Determine if the enemy can attack the square r, c
    # '''
    # def squareUnderAttack(self, r, c):
    #     self.whiteToMove = not self.whiteToMove
    #     oppMoves = self.getAllPossibleMoves()
    #     self.whiteToMove = not self.whiteToMove
    #     for move in oppMoves:
    #         if move.endRow == r and move.endCol == c:
    #             return True
    #     return False
    
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: # only one check -> either block it or move king
                moves = self.getAllPossibleMoves()
                # to block a check we must move a piece into a square between king and enemy piece
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece causing the check
                validSquares = [] # square that the piece can move to
                # if knight, must capture it or move the king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow+check[2]*i, kingCol+check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # get rid of any moves that dont block check or move king
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.pop(i)
            else: # double check, the king has to move 
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check so all the moves are fine
            moves = self.getAllPossibleMoves()
                

        return moves
    
    '''
    Return if a player is in check, a list of pins and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] # squares where ally pieces are pinned and which direction it is pinned from
        checks = [] # squares from which enemy is applying check
        inCheck = False

        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pin
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): # first allied piece that could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # there is second piece present so no pins or checks possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here in complex conditional
                        # 1. orthogonally away from king and the piece is a rook
                        # 2. diagonally away from king and the piece is a bishop
                        # 3. one square away from king and the piece is a pawn
                        # 4. Any direction and the piecee is queen
                        # 5. Any direction 1 square away and piece is king (this is necessary to prevent a king to move to square controlled by enemy king)
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking, so directly check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # piece blocking check, so pin
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check
                            break
                else: # off board
                    break
        
        # one more piece remaining is knight
        knightMoves = ((-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks


    '''
    All moves without considering a check
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    '''
    Generate pawn moves
    '''
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.pop(i)
                break

        # If its white's turn
        if self.whiteToMove:
            if self.board[r-1][c] == '--': # If the next sqaure is empty for it to move one step ahead
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    # if the white pawn is at inital postion (r = 6), it can move two squares
                    if r == 6 and self.board[r-2][c] == '--':
                        moves.append(Move((r, c), (r-2, c), self.board))
            
            # Pawns attack moves, here c < 7 and c > 0 prevents searching outside the board
            if c < 7 and self.board[r-1][c+1][0] == 'b': # if the next row diagonal square has black piece
                if not piecePinned or pinDirection == (-1, 1):
                    moves.append(Move((r, c), (r-1,c+1), self.board))
            if c > 0 and self.board[r-1][c-1][0] == 'b':
                if not piecePinned or pinDirection == (-1, -1):
                    moves.append(Move((r, c), (r-1,c-1), self.board))

        # If its black's turn 
        else:
            if self.board[r+1][c] == '--':
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == '--':
                        moves.append(Move((r, c), (r+2, c), self.board))

            if c < 7 and self.board[r+1][c+1][0] == 'w':
                if not piecePinned or pinDirection == (1, 1):
                    moves.append(Move((r, c), (r+1,c+1), self.board))
            if c > 0 and self.board[r+1][c-1][0] == 'w':
                if not piecePinned or pinDirection == (1, -1):
                    moves.append(Move((r, c), (r+1,c-1), self.board))

    '''
    Generate all rook moves
    '''
    def getRookMoves(self, r, c, moves):
        # enemyPiece = 'b' if self.whiteToMove else 'w'
        # for i in range(r-1, -1, -1):
        #     if self.board[i][c] == "--":
        #         moves.append(Move((r, c), (i,c), self.board))
        #     elif self.board[i][c][0] == enemyPiece:
        #         moves.append(Move((r, c), (i,c), self.board))
        #         break
        #     else:
        #         break
        # for i in range(r+1, 8):
        #     if self.board[i][c] == "--":
        #         moves.append(Move((r, c), (i,c), self.board))
        #     elif self.board[i][c][0] == enemyPiece:
        #         moves.append(Move((r, c), (i,c), self.board))
        #         break
        #     else:
        #         break

        # for i in range(c-1, -1, -1):
        #     if self.board[r][i] == "--":
        #         moves.append(Move((r, c), (r,i), self.board))
        #     elif self.board[r][i][0] == enemyPiece:
        #         moves.append(Move((r, c), (r,i), self.board))
        #         break
        #     else:
        #         break
        # for i in range(c+1, 8):
        #     if self.board[r][i] == "--":
        #         moves.append(Move((r, c), (r,i), self.board))
        #     elif self.board[r][i][0] == enemyPiece:
        #         moves.append(Move((r, c), (r,i), self.board))
        #         break
        #     else:
        #         break

        # The above code is faster (by few miliseconds) but too difficult to maintain in long run, so using direction-vectors instead

        pinnedPiece = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                pinnedPiece = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # cant remove queen from pin on rook moves, only remove on bishop moves
                    self.pins.pop(i)
                break

        # Use direction vector to denote direction
        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                # get the square in that direction
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not pinnedPiece or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--': # if the square is empy append it in valid moves
                            moves.append(Move((r, c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemyColor: # if the square contains opponents piece then append the square cause it can be captured, but then break the loop cause it cant go further
                            moves.append(Move((r, c), (endRow,endCol), self.board))
                            break
                        else: # break if any of the ally pieces encountered cause the direction will be blocked further
                            break
                else:
                    break
        
    '''
    Generate all Knight moves
    '''
    def getKnightMoves(self, r, c, moves):
        # no need for pin direction cause the knight cannot capture any piece that is diagonally or orthgonally checking the king
        pinnedPiece = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                pinnedPiece = True
                self.pins.pop(i)
                break
        # Knight moves in fixed square which are combination of (+ve or -ve) 2 and (+ve or -ve) 1 and vice versa
        knightMoves = [(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not pinnedPiece:
                    endPiece = self.board[endRow][endCol]
                    # Basically if the square does not contain an ally piece append the square to moves
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow,endCol), self.board))
                    
                
    '''
    Generate all Bishop moves
    '''
    def getBishopMoves(self, r, c, moves):
        pinnedPiece = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                pinnedPiece = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.pop(i)
                break
        # Same logic as rook moves but only the direction vector is changed since the bishops move diagonally unlike rook, which moves straight
        directions = [(-1,1),(1,-1),(-1,-1),(1,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not pinnedPiece or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow,endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    '''
    Generate all Queen moves
    '''
    def getQueenMoves(self, r, c, moves):
        # Queen move is the easiest to generate as it is combination of both rook moves and bishop moves
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    '''
    Generate all King moves
    '''
    def getKingMoves(self, r, c, moves):
        # King moves one step in any direction from the current square
        kingMoves = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # if the square does not contain an ally piece append the square to moves
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r, c), (endRow,endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        

class Move():
    # Mapping of ranks to rows and vice versa (1 starts from white side to 8 on towards the black side)
    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0
    }
    rowsToRanks = {
        v : i for i, v in ranksToRows.items()
    }

    # Mapping of Files to Columns and vice versa ('a' starts from left side towards the right i.e 'h')
    filesToCols = {
            "h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0
    }
    colsToFiles = {
        v : i for i, v in filesToCols.items()
    }

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol] # moved piece
        self.pieceCaptured = board[self.endRow][self.endCol] # captured piece
        self.moveID = self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol # unique id for each move for object comparison purpose

    '''
    Overriding __eq__ method to compare moveID of two moves instead of default __eq__ which compares address
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID:
                return True
        return False

    '''
    Genrates chess notation
    '''
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    '''
    Converts columns to files and rows to ranks
    '''
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    

    

    