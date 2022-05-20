"""
Main driver file
Responsible for handling user input and displaying the current GameState object
"""

from numpy import diagonal
import pygame as p
import ttt_engine
import random

WIDTH = 240
HEIGHT = 320
DIMENSION = 3
SQ_SIZE = 80
MAX_FPS = 15
IMAGES = {}
score = [0, 0]  # player X, player O


def loadImages():
    IMAGES["x"] = p.transform.scale(p.image.load(
        "images/x.png"), (SQ_SIZE // 2, SQ_SIZE // 2))
    IMAGES["o"] = p.transform.scale(p.image.load(
        "images/o.png"), (SQ_SIZE // 2, SQ_SIZE // 2))


def mainMenu():
    global gs, screen, clock
    p.init()
    screen = p.display.set_mode((WIDTH + 1, HEIGHT + 1))
    clock = p.time.Clock()
    gs = ttt_engine.GameState()
    drawMainMenu()
    p.display.update()
    loadImages()

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()    # (x, y) location of the mouse
                if 20 <= location[0] <= 220 and 20 <= location[1] <= 80:
                    running = False
                    main()
                elif 20 <= location[0] <= 220 and 85 <= location[1] <= 145:
                    running = False
                    setDifficulty()
                    mainAI()


def setDifficulty():
    global difficulty
    drawDifficultyMenu()
    p.display.update()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()    # (x, y) location of the mouse
                if 20 <= location[0] <= 220 and 20 <= location[1] <= 80:
                    running = False
                    difficulty = 1  # easy
                elif 20 <= location[0] <= 220 and 85 <= location[1] <= 145:
                    running = False
                    difficulty = 2  # hard
    return difficulty


def drawDifficultyMenu():
    p.display.set_caption("ttt v1.0")
    screen.fill((0, 0, 0))
    font = p.font.SysFont("comicsans", 25)
    label = font.render("Easy", 1, (255, 255, 255))
    label2 = font.render("Hard", 1, (255, 255, 255))
    p.draw.rect(screen, (255, 255, 255), p.Rect(20, 20, 200, 60), 2)
    p.draw.rect(screen, (255, 255, 255), p.Rect(20, 85, 200, 60), 2)
    screen.blit(label, (WIDTH /
                        2 - (label.get_width() / 2), 30))
    screen.blit(label2, (WIDTH /
                         2 - (label2.get_width() / 2), 95))


def drawMainMenu():
    p.display.set_caption("ttt v1.0")
    screen.fill((0, 0, 0))
    font = p.font.SysFont("comicsans", 25)
    label = font.render("Player vs Player", 1, (255, 255, 255))
    label2 = font.render("Player vs AI", 1, (255, 255, 255))
    p.draw.rect(screen, (255, 255, 255), p.Rect(20, 20, 200, 60), 2)
    p.draw.rect(screen, (255, 255, 255), p.Rect(20, 85, 200, 60), 2)
    screen.blit(label, (WIDTH /
                        2 - (label.get_width() / 2), 30))
    screen.blit(label2, (WIDTH /
                         2 - (label2.get_width() / 2), 95))


def mainAI():
    running = True
    while running:
        if not gs.XToMove and difficulty == 1:
            moveAIEasy(gs)    # AI makes move (easy)
            gs.XToMove = True
            if gs.EndGameCheck():
                whoWins()
                p.display.update()
                restart = False
                while not restart:
                    for key in p.event.get():
                        if key.type == p.QUIT:
                            p.quit()
                        elif key.type in (p.KEYDOWN, p.MOUSEBUTTONDOWN):
                            restart = True
                restartGame(gs)
        elif not gs.XToMove and difficulty == 2:
            moveAIHard(gs)    # AI makes move (hard) CHANGE TO HARD LATER
            gs.XToMove = True
            if gs.EndGameCheck():
                whoWins()
                p.display.update()
                restart = False
                while not restart:
                    for key in p.event.get():
                        if key.type == p.QUIT:
                            p.quit()
                        elif key.type in (p.KEYDOWN, p.MOUSEBUTTONDOWN):
                            restart = True
                restartGame(gs)
        else:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()    # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE - 1
                    if gs.board[row][col] == "-":
                        gs.board[row][col] = "x"
                        gs.XToMove = not gs.XToMove
                        if gs.EndGameCheck():
                            whoWins()
                            p.display.update()
                            restart = False
                            while not restart:
                                for key in p.event.get():
                                    if key.type == p.QUIT:
                                        p.quit()
                                    elif key.type in (p.KEYDOWN, p.MOUSEBUTTONDOWN):
                                        restart = True
                            restartGame(gs)

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.update()


def main():
    running = True
    while running:
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.update()
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()    # (x, y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE - 1
                if gs.board[row][col] == "-":
                    if gs.XToMove:
                        gs.board[row][col] = "x"
                    else:
                        gs.board[row][col] = "o"
                    if gs.EndGameCheck():
                        whoWins()
                        p.display.update()
                        restart = False
                        while not restart:
                            for key in p.event.get():
                                if key.type == p.QUIT:
                                    restart = True
                                    running = False
                                elif key.type in (p.KEYDOWN, p.MOUSEBUTTONDOWN):
                                    restart = True
                        restartGame(gs)
                    gs.XToMove = not gs.XToMove


def moveAIEasy(gs):
    fail = random.choice([0, 0, 1])   # failrate 33%
    if fail == 0:
        winIfPossibleAI(gs)
    fail = random.choice([0, 0, 1])   # failrate 33%
    if not gs.XToMove and fail == 0:
        defendIfNeededAI(gs)
    if not gs.XToMove:
        row = 0
        col = 0
        while gs.board[row][col] != "-":
            row = random.choice([0, 1, 2])
            col = random.choice([0, 1, 2])
        gs.board[row][col] = "o"


def moveAIHard(gs):
    winIfPossibleAI(gs)       # if possible, place mark to win
    if not gs.XToMove:
        defendIfNeededAI(gs)      # if needed, block player's possible win
    if not gs.XToMove:
        bestPossibleMoveAI(gs)    # move to: mid -> corner -> edge


def winIfPossibleAI(gs):
    triples = []
    if (gs.board[0][0] + gs.board[1][1] + gs.board[2][2]) == "oo-" or (gs.board[0][0] + gs.board[1][1] + gs.board[2][2]) == "o-o" or (gs.board[0][0] + gs.board[1][1] + gs.board[2][2]) == "-oo":
        gs.board[0][0] = gs.board[1][1] = gs.board[2][2] = "o"
        gs.XToMove = True
    elif (gs.board[0][2] + gs.board[1][1] + gs.board[2][0]) == "oo-" or (gs.board[0][2] + gs.board[1][1] + gs.board[2][0]) == "o-o" or (gs.board[0][2] + gs.board[1][1] + gs.board[2][0]) == "-oo":
        gs.board[0][2] = gs.board[1][1] = gs.board[2][0] = "o"
        gs.XToMove = True
    else:
        for i in range(len(gs.board)):
            triples.append(gs.board[i][0] +
                           gs.board[i][1] + gs.board[i][2])
            if "oo-" in triples or "o-o" in triples or "-oo" in triples:
                gs.board[i][0] = gs.board[i][1] = gs.board[i][2] = "o"
                gs.XToMove = True
                break
            triples.append(gs.board[0][i] +
                           gs.board[1][i] + gs.board[2][i])
            if "oo-" in triples or "o-o" in triples or "-oo" in triples:
                gs.board[0][i] = gs.board[1][i] = gs.board[2][i] = "o"
                gs.XToMove = True
                break


def defendIfNeededAI(gs):
    diagonal = (gs.board[0][0] + gs.board[1][1] + gs.board[2][2])
    antidiagonal = (gs.board[0][2] + gs.board[1][1] + gs.board[2][0])
    if diagonal in ["xx-", "x-x", "-xx"]:
        index = diagonal.index("-")
        gs.board[index][index] = "o"
        gs.XToMove = True
    elif antidiagonal in ["xx-", "x-x", "-xx"]:
        index = antidiagonal.index("-")
        gs.board[index][2 - index] = "o"
        gs.XToMove = True
    else:
        for i in range(len(gs.board)):
            triple = (gs.board[i][0] +
                      gs.board[i][1] + gs.board[i][2])
            if triple in ["xx-", "x-x", "-xx"]:
                index = triple.index("-")
                gs.board[i][index] = "o"
                gs.XToMove = True
                break
            triple = (gs.board[0][i] +
                      gs.board[1][i] + gs.board[2][i])
            if triple in ["xx-", "x-x", "-xx"]:
                index = triple.index("-")
                gs.board[index][i] = "o"
                gs.XToMove = True
                break


def bestPossibleMoveAI(gs):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]  # indices of corners
    random.shuffle(corners)
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]    # indices of edges
    random.shuffle(edges)
    # place "o" in the middle if possible
    if gs.board[1][1] == "-":
        gs.board[1][1] = "o"
    # place "o" in random corner if possible
    elif gs.board[corners[0][0]][corners[0][1]] == "-":
        gs.board[corners[0][0]][corners[0][1]] = "o"
    elif gs.board[corners[1][0]][corners[1][1]] == "-":
        gs.board[corners[1][0]][corners[1][1]] = "o"
    elif gs.board[corners[2][0]][corners[2][1]] == "-":
        gs.board[corners[2][0]][corners[2][1]] = "o"
    elif gs.board[corners[3][0]][corners[3][1]] == "-":
        gs.board[corners[3][0]][corners[3][1]] = "o"
    # place "o" in random edge if possible
    elif gs.board[edges[0][0]][edges[0][1]] == "-":
        gs.board[edges[0][0]][edges[0][1]] = "o"
    elif gs.board[edges[1][0]][edges[1][1]] == "-":
        gs.board[edges[1][0]][edges[1][1]] = "o"
    elif gs.board[edges[2][0]][edges[2][1]] == "-":
        gs.board[edges[2][0]][edges[2][1]] = "o"
    elif gs.board[edges[3][0]][edges[3][1]] == "-":
        gs.board[edges[3][0]][edges[3][1]] = "o"


def whoWins():
    drawGameState(screen, gs)
    if gs.EndGameCheck() == "player X":
        score[0] += 1
        font = p.font.SysFont("comicsans", 30, bold=True)
        labelWinX = font.render(
            "X WINS!", 1, (0, 0, 0))
        background = p.Surface(labelWinX.get_size())
        background.fill((255, 255, 255))
        background.blit(labelWinX, (0, 0))
        screen.blit(background, ((WIDTH // 2 -
                    labelWinX.get_width() // 2), 55))
    elif gs.EndGameCheck() == "player O":
        score[1] += 1
        font = p.font.SysFont("comicsans", 30, bold=True)
        labelWinO = font.render(
            "O WINS!", 1, (0, 0, 0))
        background = p.Surface(labelWinO.get_size())
        background.fill((255, 255, 255))
        background.blit(labelWinO, (0, 0))
        screen.blit(background, ((WIDTH // 2 -
                    labelWinO.get_width() // 2), 55))
    else:
        gs.XToMove = not gs.XToMove


def restartGame(gs):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            gs.board[x][y] = "-"
    gs.XToMove = gs.XToMoveLast = not gs.XToMoveLast


def drawGameState(screen, gs):
    screen.fill((0, 0, 0))
    drawBoard(screen)           # draw lines on the board
    drawXO(screen, gs.board)    # draw XOs on the board
    drawText(screen, score)     # draw all text labels
    if gs.XToMove:
        screen.blit(IMAGES["x"], p.Rect(
            10, 35, SQ_SIZE, SQ_SIZE))
    else:
        screen.blit(IMAGES["o"], p.Rect(
            WIDTH - 10 - IMAGES["o"].get_width(), 35, SQ_SIZE, SQ_SIZE))


def drawText(screen, score):
    font = p.font.SysFont("comicsans", 20)

    label = font.render("Player X : Player O", 1, (255, 255, 255))

    label2 = font.render(f"{score[0]} : {score[1]}", 1, (255, 255, 255))

    screen.blit(label, (WIDTH /
                        2 - (label.get_width() / 2), 0))
    screen.blit(label2, (WIDTH /
                         2 - (label2.get_width() / 2), 25))


def drawBoard(screen):
    for y in range(1, DIMENSION + 2):
        for x in range(0, DIMENSION + 1):
            p.draw.line(screen, "white", (0, y * SQ_SIZE),
                        (DIMENSION * SQ_SIZE, y * SQ_SIZE))
            p.draw.line(screen, "white", (x * SQ_SIZE, y *
                        SQ_SIZE), (x * SQ_SIZE, DIMENSION * SQ_SIZE))


def drawXO(screen, board):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            X_O = board[x][y]
            if X_O != "-":
                screen.blit(IMAGES[X_O], p.Rect(
                    (y + 0.25) * SQ_SIZE, (x + 1.25) * SQ_SIZE, SQ_SIZE, SQ_SIZE))


mainMenu()
