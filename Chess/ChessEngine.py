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

    '''
    Makes moves by:
    1. Making start square empty '--'
    2. move the piece from start square to end square
    3. append the move to move log
    4. change move to opponent by setting whiteToMove as not whiteToMove
    '''
    def makeMove(self, move):
        self.board[move.startSqRow][move.startSqCol] = "--"
        self.board[move.endSqRow][move.endSqCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    '''
    Undoing a move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startSqRow][move.startSqCol] = move.pieceMoved
            self.board[move.endSqRow][move.endSqCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    All moves considering check
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

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
        # If its white's turn
        if self.whiteToMove:
            # If the next sqaure is empty for it to move one step ahead
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))
                # if the white pawn is at inital postion (r = 6), it can move two squares
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))
            
            # Pawns attack moves, here c < 7 and c > 0 prevents searching outside the board
            if c < 7 and self.board[r-1][c+1][0] == 'b': # if the next row diagonal square has black piece
                moves.append(Move((r, c), (r-1,c+1), self.board))
            if c > 0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r, c), (r-1,c-1), self.board))

        # If its black's turn 
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))

            if c < 7 and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r, c), (r+1,c+1), self.board))
            if c > 0 and self.board[r+1][c-1][0] == 'w':
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

        # Use direction vector to denote direction
        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                # get the square in that direction
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        # Knight moves in fixed square which are combination of (+ve or -ve) 2 and (+ve or -ve) 1 and vice versa
        knightMoves = [(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # Basically if the square does not contain an ally piece append the square to moves
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow,endCol), self.board))
                    
                
    '''
    Generate all Bishop moves
    '''
    def getBishopMoves(self, r, c, moves):
        # Same logic as rook moves but only the direction vector is changed since the bishops move diagonally unlike rook, which moves straight
        directions = [(-1,1),(1,-1),(-1,-1),(1,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
                    moves.append(Move((r, c), (endRow,endCol), self.board))
        

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
        self.startSqRow = startSq[0]
        self.startSqCol = startSq[1]
        self.endSqRow = endSq[0]
        self.endSqCol = endSq[1]

        self.pieceMoved = board[self.startSqRow][self.startSqCol] # moved piece
        self.pieceCaptured = board[self.endSqRow][self.endSqCol] # captured piece
        self.moveID = self.startSqRow*1000+self.startSqCol*100+self.endSqRow*10+self.endSqCol # unique id for each move for object comparison purpose

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
        return self.getRankFile(self.startSqRow, self.startSqCol) + self.getRankFile(self.endSqRow, self.endSqCol)

    '''
    Converts columns to files and rows to ranks
    '''
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    

    

    