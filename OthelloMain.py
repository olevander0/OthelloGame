import pygame as p
import OthelloGameState

# Dimension variables
HEIGHT = WIDTH = 800
LENGTH = (HEIGHT // 4) * 3.5
BREDDDIFF = 0
DIMENSION = 8
SQ_SIZE = LENGTH // DIMENSION
LINEWIDTH = LENGTH // 200
STARTY = HEIGHT - LENGTH
STARTX = STARTY // 2
INNERSTARTY = STARTY + LINEWIDTH + SQ_SIZE // 2
INNERSTARTX = STARTX + LINEWIDTH + SQ_SIZE // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (238, 238, 238)
GREEN = (0, 90, 0)
CIRCLEGREEN = (0, 150, 0)
HIGHLIGHTGREEN = (0, 205, 0)
HIGHLIGHTGREEN2 = (0, 255, 170)


def main():
    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)

    # Sets windowname
    p.display.set_caption('Othello')

    # Ininatlizes GameState that tracks the board, DIMENSION decides board size
    gs = OthelloGameState.GameState(DIMENSION)

    # Draws the inital board
    drawGameState(screen, gs)

    # sqselected and updatingscreen used to determine squarehighlighting
    sqselected = (-1, -1)
    updatingscreen = False

    randommode, aimode = False, False
    gameover = False
    running = True
    gamemode = 0
    selectedplayer = True

    # Gamelopp
    while running:
        # Checks for events
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Updates screen and dimension variables if videosize change
            elif e.type == p.VIDEORESIZE:
                screen = toggle_fullscreen()
                drawGameState(screen, gs)
                sqselected = (-1, -1)

            # Makes a move if the selected position is valid
            elif e.type == p.MOUSEBUTTONDOWN:
                x = e.pos[0]
                y = e.pos[1]
                tryMove(screen, gs, x, y)
                updatingscreen = True
                sqselected = (-1, -1)

            elif e.type == p.KEYDOWN:
                # Undo last move
                if e.key == p.K_z:
                    gs.undoMove()
                    gameover = False
                    updatingscreen = True
                    sqselected = (-1, -1)
                # Restarts game
                elif e.key == p.K_x:
                    gs = OthelloGameState.GameState(DIMENSION)
                    gameover = False
                    updatingscreen = True
                    sqselected = (-1, -1)
                # Makes random moves
                elif e.key == p.K_r:
                    randommode = not randommode
                    aimode = False
                # Selects ai vs playermode
                elif e.key == p.K_SPACE:
                    gamemode += 1 if gamemode != 2 else -2
                    aimode = False
                    randommode = False
                    selectedplayer = gs.player
                    print(gamemode)
                elif e.key == p.K_a:
                    aimode = not aimode
                    randommode = False

        if not gameover:
            if gamemode == 0:
                allowedtomove = False
            elif gamemode == 1:
                allowedtomove = True if selectedplayer == gs.player else False
            else:
                allowedtomove = True
            if (randommode or aimode) and allowedtomove:
                gs.makeRandomMoves() if randommode else gs.makeComputerMove()
                updatingscreen = True
                sqselected = (-1, -1)
            if drawScore(screen, gs):
                gameover = True
                randommode = False
                aimode = False
                gamemode = 0
            if not updatingscreen:
                sqselected = highlight(screen, gs, sqselected)
            drawGameState(screen, gs)
            if sqselected != (-1, -1):
                if sqselected in gs.allPossibleMoves():
                    drawCircle(screen, sqselected[0],
                               sqselected[1], HIGHLIGHTGREEN2)
                else:
                    drawCircle(screen, sqselected[0],
                               sqselected[1], HIGHLIGHTGREEN)
            updatingscreen = False
        p.display.flip()


def toggle_fullscreen():
    p.display.flip()
    screen = p.display.get_surface()
    w = screen.get_width()
    h = screen.get_height()
    globals()["HEIGHT"] = h
    globals()["WIDTH"] = HEIGHT
    globals()["BREDDDIFF"] = (w - HEIGHT) // 2
    globals()["LENGTH"] = (HEIGHT // 4) * 3.5
    globals()["SQ_SIZE"] = LENGTH // DIMENSION
    globals()["LINEWIDTH"] = LENGTH // 200
    globals()["STARTY"] = HEIGHT - LENGTH
    globals()["STARTX"] = STARTY // 2
    globals()["INNERSTARTY"] = STARTY + LINEWIDTH + SQ_SIZE // 2
    globals()["INNERSTARTX"] = STARTX + LINEWIDTH + SQ_SIZE // 2

    # loadTextDict()

    screen = p.display.set_mode((w, HEIGHT), p.RESIZABLE)
    return screen


def tryMove(screen, gs, x, y):
    try:
        selectedcolor = (screen.get_at((x, y)))
        if selectedcolor == HIGHLIGHTGREEN2:
            x, y = getCord(x, y)
            gs.makeMove(x, y)
    except Exception:
        print(Exception)


def highlight(screen, gs, sqselected):
    try:
        x, y = p.mouse.get_pos()
        selectedcolor = (screen.get_at((x, y)))
        if (selectedcolor == CIRCLEGREEN or selectedcolor == HIGHLIGHTGREEN2) \
           and sqselected == (-1, -1):
            x, y = getCord(x, y)
            return (x, y)
        elif (selectedcolor != HIGHLIGHTGREEN and sqselected
              != (-1, -1) and selectedcolor != HIGHLIGHTGREEN2):
            return (-1, -1)
    except Exception:
        pass
    return sqselected


def getCord(x, y):
    for y0 in range(DIMENSION):
        for x0 in range(DIMENSION):
            xCompare = (x0 * SQ_SIZE + INNERSTARTX + BREDDDIFF) - x
            yCompare = (y0 * SQ_SIZE + INNERSTARTY) - y
            if abs(yCompare) <= SQ_SIZE // 2.2 and \
                    abs(xCompare) <= SQ_SIZE // 2.2:
                return x0, y0


def drawCircle(screen, x, y, color=None):
    if color is None:
        color = CIRCLEGREEN
    pos = (x * SQ_SIZE + INNERSTARTX + BREDDDIFF, y * SQ_SIZE + INNERSTARTY)
    p.draw.circle(screen, color, pos, SQ_SIZE // 2.2)


def drawBoard(screen):
    p.draw.rect(screen, GREEN, (BREDDDIFF, 0, WIDTH, HEIGHT))
    for i in range(DIMENSION + 1):
        # linjer Yled
        p.draw.rect(screen, BLACK, (i * SQ_SIZE + STARTX + BREDDDIFF, STARTY,
                    LINEWIDTH, LENGTH))
        # linjer Xled
        p.draw.rect(screen, BLACK, (STARTX + BREDDDIFF, i * SQ_SIZE + STARTY,
                    LENGTH, LINEWIDTH))


def drawAllCircles(screen, gs):
    for y in range(DIMENSION):
        for x in range(DIMENSION):
            color = gs.board[y][x]
            if color == 0:
                drawCircle(screen, x, y)
            else:
                c = WHITE if color == 1 else BLACK
                drawCircle(screen, x, y, c)


def fillScreen(screen, gs):
    if gs.player:
        screen.fill(WHITE)
    else:
        screen.fill(BLACK)


def drawGameState(screen, gs):
    fillScreen(screen, gs)
    drawBoard(screen)
    drawAllCircles(screen, gs)


def drawScore(screen, gs):
    if gs.checkGameOver():
        white = gs.score[0]
        black = gs.score[1]
        if white > black:
            print("White Won")
        elif black > white:
            print("Black Won")
        else:
            print("draw")
        print("White:", white, "  Black:", black)
        return True
    return False


if __name__ == '__main__':
    main()
