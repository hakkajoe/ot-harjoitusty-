from random import random
from game.piece import Piece


class Board:
    def __init__(self, size, prob):
        self._size = size
        self._prob = prob
        self._lost = False
        self._won = False
        self._NumClicked = 0
        self._NumNonBombs = 0
        self.SetBoard()

    def SetBoard(self):
        self._board = []
        for row in range(self._size[0]):
            row = []
            for col in range(self._size[1]):
                HasBomb = random() < self._prob
                if not HasBomb:
                    self._NumNonBombs += 1
                piece = Piece(HasBomb)
                row.append(piece)
            self._board.append(row)
        self._SetNeighbors_board()

    def _SetNeighbors_board(self):
        for row in range(self._size[0]):
            for col in range(self._size[1]):
                piece = self._GetPiece((row, col))
                neighbors = self._GetListOfNeighbors((row, col))
                piece.SetNeighbors_piece(neighbors)

    def GetSize(self):
        return self._size

    def _GetPiece(self, index):
        return self._board[index[0]][index[1]]

    def _GetListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                OutOfBounds = row < 0 or row >= self._size[0] or col < 0 or col >= self._size[1]
                same = row == index[0] and col == index[1]
                if same or OutOfBounds:
                    continue
                neighbors.append(self._GetPiece((row, col)))
        return neighbors

    def HandleClick_board(self, piece, flag):
        if piece.GetClicked() or not flag and piece.GetFlagged():
            return
        if flag:
            piece.ToggleFlag()
            return
        piece.click()
        if piece.GetHasBomb():
            self._lost = True
            return
        self._NumClicked += 1
        if piece.GetNumAround() != 0:
            return
        for neighbor in piece.GetNeighbors():
            if not neighbor.GetHasBomb() and not neighbor.GetClicked():
                self.HandleClick_board(neighbor, False)

    def GetLost(self):
        return self._lost

    def GetWon(self):
        return self._NumNonBombs == self._NumClicked
