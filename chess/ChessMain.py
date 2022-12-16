# this will be our Game file which will consider user Input and will display GameState object
import pygame as p
import ChessEngine
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # used for Animations
IMAGES = {}
'''
Intialize a global dictionary for storing images this will be called exactly once in main so its will reduce overall cost of operations
'''
def loadImages():
    pieces = ["bp", "bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
'''
The main driver will handle user inputs and will update the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()  # no sq. selected initially, keep track of user selected sq. (tuple: (row, col))

    playerClicks = []  # keep track of player clicks eg. [(6, 4),(7, 5)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()        # x, y location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()     # deselect the selected cell
                    playerClicks = []   # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)     # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:      # after 2nd click 
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    # print(move.getChessNotation())
                    
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when z is pressed
                    gs.undoMove()
                    moveMade = True
            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
handle all Graphical states and actions
'''
def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gs.board)  # draw pieces on top of those squares

'''
Draw the Squares on the Board
'''
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            # print(color)
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # p.Rect(left, top, width, height)

'''
draw the pieces on the board using current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
