import pygame as p
import ChessEngine

# Here I have defined all the board properties
WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15

# This is the image dict where all the piece image locations will be stored
IMAGES = {}


# Used to load all the images dynamically into the IMAGES dict
def loadImages():
    pieces = ['bR','wR','bN','wN','bK','wK','bp','wp','bQ','wQ','bB','wB']
    for piece in pieces:
        IMAGES[piece] =  p.transform.scale(p.image.load('Chess/images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))


"""
Main chess board rendering logic is defined here
"""

def main():

    # Pygame board initialization
    p.init()
    screen = p.display.set_mode((HEIGHT,WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves() # Generates all the valid moves
    moveMade = False 

    loadImages() # Load all the images during intialization phase
    running = True
    sqSelected = () # Tracks currently selected square
    playerClicks = [] # Stores start square and end square for one move

    # This loop runs for each and every frame
    while running:

        # This loop runs for each and every event in that particular frame (Eg: quit, mouse click, keyboard presses, etc)
        for e in p.event.get():

            # When quit button is clicked
            if e.type == p.QUIT:
                running = False

            # When mouse click happens on the frame (used to check which piece or square is clicked)
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # Gives location of the mouse click (x, y) coordinates
                col = location[0]//SQ_SIZE # x // sq_size gives int in range [0, 7]
                row = location[1]//SQ_SIZE # y // sq_size gives int in range [0, 7]

                # If same square is clicked twice, no need to do anything, hence clear both sqSelected and playerClicks
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []

                # If second square selected is different, make actual move if valid
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append first move (souce) or second click (end move) to playerClicks
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) # Creating a Move object

                        # If the move is present in validMoves generated using the fuction getValidMoves()
                        if move in validMoves:
                            gs.makeMove(move) # Make move
                            print(move.getChessNotation())  # Print the chess notation (Eg: d3d4, a2b3, etc)
                            moveMade = True  # Set move made as True

                            # Reset both sqSelected and playerClicks
                            sqSelected = () 
                            playerClicks = []

                        # This is used in order to not waste clicks, for eg: if a user selects a piece and then selects another piece (Here the other piece will not be selected unless you make the third click), or selecting an empty square first
                        else:
                            playerClicks = [sqSelected]

            # if a key is pressed (for Undo)
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # K_z means key Z
                    gs.undoMove() # Undo previous move when Z key is pressed
                    moveMade = True # Set Movemade as True, so that again valid moves can be generated for previous state

        # If moveMade is True, the for next state generate all the possible moves and set moveMade to False
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        


        drawGameState(screen, gs)
        clock.tick(MAX_FPS) # Used to set fps, here 15 frames are rendered every second
        p.display.flip() # Used to display the rendered frame

'''
Used to draw the current game state
'''
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''
Used to drawn the chess board sqaures (not pieces)
'''
def drawBoard(screen):
    colors = [p.Color("#fbc273"), p.Color("#cf7633")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            # The very first square of the board starts with white color (or light color)
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

'''
Used to draw pieces based on the board 2D list from gamestate
'''
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != '--': # If piece is present in that square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

