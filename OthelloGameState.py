import numpy as np
import random as r


class GameState:

    def genBoard(self, dimension):
        iterable = (x-x for x in range(dimension))
        xled = np.fromiter(iterable, int)
        board = ([np.stack(xled) for i in range(dimension)])
        center = dimension // 2 - 1
        board[center][center] = 1
        board[center + 1][center + 1] = 1
        board[center][center + 1] = 2
        board[center + 1][center] = 2
        return board

    def __init__(self, dimension):
        self.board = self.genBoard(dimension)
        self.dimension = dimension
        self.player = True
        self.movelog = []
        self.score = (2, 2)

    def placeCircle(self, x, y, color):
        self.board[y][x] = color

    def validSquares(self, x, y, color):
        oppcolor = 2 if color == 1 else 1
        squares = []
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1),
                      (1, 0), (0, 1), (-1, 0), (0, -1))
        for d in directions:
            squaresdir = []
            for i in range(1, self.dimension):
                x0 = x + d[0] * i
                y0 = y + d[1] * i
                if 0 <= x0 < self.dimension and 0 <= y0 < self.dimension:
                    if oppcolor == self.board[y0][x0]:
                        squaresdir.append((x0, y0))
                    elif len(squaresdir) > 0 and color == self.board[y0][x0]:
                        squares.extend(squaresdir)
                    else:
                        break
                else:
                    break
        return squares

    def makeMove(self, x, y):
        color = 1 if self.player else 2
        squares = self.validSquares(x, y, color)
        if len(squares) == 0:
            return False

        self.placeCircle(x, y, color)
        for pos in squares:
            self.placeCircle(pos[0], pos[1], color)
        squares.append((x, y))
        self.movelog.append(squares)
        self.player = not self.player
        return True

    def undoMove(self):
        if len(self.movelog) > 0:
            color = 1 if self.player else 2
            squares = self.movelog.pop()
            first = True
            for pos in reversed(squares):
                if first:
                    first = False
                    self.placeCircle(pos[0], pos[1], 0)
                else:
                    self.placeCircle(pos[0], pos[1], color)
            self.player = not self.player

    def allPossibleMoves(self):
        moves = []
        color = 1 if self.player else 2
        for y in range(self.dimension):
            for x in range(self.dimension):
                if self.board[y][x] == 0:
                    if len(self.validSquares(x, y, color)) > 0:
                        moves.append((x, y))
        return moves

    def updateScore(self):
        white = 0
        black = 0
        for row in self.board:
            for n in row:
                if n == 1:
                    white += 1
                elif n == 2:
                    black += 1
        self.score = (white, black)

    def checkGameOver(self):
        self.updateScore()
        if len(self.allPossibleMoves()) < 1:
            return True
        return False

    def makeRandomMoves(self):
        moves = self.allPossibleMoves()
        m = moves[(r.randint(0, len(moves) - 1))]
        self.makeMove(m[0], m[1])

    def tryAllMoves(self):
        for y in range(self.dimension):
            for x in range(self.dimension):
                if self.board[y][x] == 0:
                    if self.makeMove(y, x):
                        pass

    def makeComputerMove(self):
        self.makeRandomMoves()
