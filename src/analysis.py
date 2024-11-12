class Analysis:

    def __init__(self, board: list[int] = [0] * 9):
        self.board: list[int] = board

    def winner(self):
        vertical_left = self.board[0] == self.board[3] == self.board[6] and self.board[0] != 0
        vertical_middle = self.board[1] == self.board[4] == self.board[7] and self.board[1] != 0
        vertical_right = self.board[2] == self.board[5] == self.board[8] and self.board[2] != 0
        horizontal_top = self.board[0] == self.board[1] == self.board[2] and self.board[0] != 0
        horizontal_middle = self.board[3] == self.board[4] == self.board[5] and self.board[3] != 0
        horizontal_bottom = self.board[6] == self.board[7] == self.board[8] and self.board[6] != 0
        diagonal_topleft_bottomright = self.board[0] == self.board[4] == self.board[8] and self.board[0] != 0
        diagonal_topright_bottomleft = self.board[2] == self.board[4] == self.board[6] and self.board[2] != 0
        if (
            vertical_left
            or vertical_middle
            or vertical_right
            or horizontal_top
            or horizontal_middle
            or horizontal_bottom
            or diagonal_topleft_bottomright
            or diagonal_topright_bottomleft
        ):
            if vertical_middle or horizontal_middle or diagonal_topleft_bottomright or diagonal_topright_bottomleft:
                return self.board[4]
            elif vertical_left or horizontal_top:
                return self.board[0]
            elif vertical_right or horizontal_bottom:
                return self.board[8]
        return 0

    def almost_winners(self) -> dict[int, list[int]]:
        if self.winner():
            return None

        board_copy = list(self.board)
        players = list(set(self.board) - {0})
        almost_players = dict()

        for i, p in enumerate(self.board):
            if p != 0:
                continue
            for _p in players:
                self.board[i] = _p
                if self.winner():
                    if _p not in almost_players:
                        almost_players[_p] = [i]
                    else:
                        almost_players[_p].append(i)
                self.board = list(board_copy)

        self.board = list(board_copy)
        return almost_players
