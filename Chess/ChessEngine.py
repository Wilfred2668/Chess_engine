class GameState():
    def __init__(self):
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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

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
        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c < 7 and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r, c), (r-1,c+1), self.board))
            if c > 0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r, c), (r-1,c-1), self.board))
            
        if not self.whiteToMove:
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

        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
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
    Generate all Knight moves
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2)]
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow,endCol), self.board))
                    
                
    '''
    Generate all Bishop moves
    '''
    def getBishopMoves(self, r, c, moves):
        pass

    '''
    Generate all Queen moves
    '''
    def getQueenMoves(self, r, c, moves):
        pass

    '''
    Generate all King moves
    '''
    def getKingMoves(self, r, c, moves):
        pass
    

class Move():

    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0
    }
    rowsToRanks = {
        v : i for i, v in ranksToRows.items()
    }
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

        self.pieceMoved = board[self.startSqRow][self.startSqCol]
        self.pieceCaptured = board[self.endSqRow][self.endSqCol]
        self.moveID = self.startSqRow*1000+self.startSqCol*100+self.endSqRow*10+self.endSqCol

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID:
                return True
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startSqRow, self.startSqCol) + self.getRankFile(self.endSqRow, self.endSqCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    

    

    