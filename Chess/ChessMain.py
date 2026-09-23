import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['bR','wR','bN','wN','bK','wK','bp','wp','bQ','wQ','bB','wB']
    for piece in pieces:
        IMAGES[piece] =  p.transform.scale(p.image.load('Chess/images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((HEIGHT,WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            print(move.getChessNotation())
                            moveMade = True
                        sqSelected = ()
                        playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("#fbc273"), p.Color("#cf7633")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

    
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

