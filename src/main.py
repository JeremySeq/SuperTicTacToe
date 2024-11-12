import pygame

import settings
import board


class Main:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("super-ttt")

        self.font = pygame.freetype.SysFont("3270 Nerd Font Mono", 20)
        self.font_big = pygame.freetype.SysFont("3270 Nerd Font Mono", 24)
        self.font_bigger = pygame.freetype.SysFont("3270 Nerd Font Mono", 36)

        big_board_rect = pygame.Rect(
            settings.BOARD_PADDING,
            settings.BOARD_PADDING,
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_WIDTH / 2,
        )
        self.big_board = board.MetaBoard(big_board_rect)

        self.current_move_player = 1
        self.current_move_i = -1

        self.quit = False
        self.won = False
        self.god = False  # good for debugging

    def _valid_move(self, i, j) -> bool:
        if i is None or j is None:
            return False
        return (
            not self.won
            and (i == self.current_move_i or self.current_move_i == -1)
            and self.big_board.boards[i].tiles[j].player == 0
            and self.big_board.boards[i].winner() == 0
        ) or self.god

    def run(self):
        while not self.quit:
            self.update()
            self.render()

    def update(self):
        self.handle_events()

        if self.big_board.winner():
            self.won = True

    def render(self):
        mouse_x, mouse_y, mouse_tile_i, mouse_tile_j = self.get_mouse_stuff()

        hints = [([], [[] for _ in range(9)]) for _ in range(9)]

        self.screen.fill(settings.COLOR_BOARD_0)
        self.big_board.draw(self.screen, settings.COLOR_BOARD_1)

        for i, mini_board in enumerate(self.big_board.boards):

            if mini_board.winner():
                self.render_mini_board_winner(mini_board)
                continue

            next_move = self._valid_move(mouse_tile_i, mouse_tile_j) and i == mouse_tile_j

            self.render_mini_board(mouse_tile_i, mouse_tile_j, i, mini_board, next_move)

            mini_board_hints = hints[i][0]
            tile_hints = hints[i][1]

            if next_move:
                mini_board_hints.append("next move")

            for j, tile in enumerate(mini_board.tiles):
                self.render_tile(mouse_tile_i, mouse_tile_j, i, j, mini_board, tile)
                tile_hints[j] += self.tile_hints(i, j, mini_board)

            # hints[i] = (mini_board_hints, tile_hints)

        self.render_hints(hints)
        if not self.won:
            self.render_mouse_hints(mouse_x, mouse_y, mouse_tile_i, mouse_tile_j, hints)

        pygame.display.flip()

    def get_mouse_stuff(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_tile_i, mouse_tile_j = None, None
        for i, mini_board in enumerate(self.big_board.boards):
            for j, tile in enumerate(mini_board.tiles):
                if tile.rect.collidepoint(mouse_x, mouse_y):
                    mouse_tile_i, mouse_tile_j = i, j
        return mouse_x, mouse_y, mouse_tile_i, mouse_tile_j

    def render_mouse_hints(self, mouse_x, mouse_y, mouse_tile_i, mouse_tile_j, hints):
        text_surf, text_rect = self.font_big.render(
            settings.PLAYER_SYMBOLS[self.current_move_player], settings.COLOR_BOARD_0
        )
        text_rect.move_ip(mouse_x + 10, mouse_y)

        bg_rect = pygame.Rect(mouse_x, mouse_y, 32, 32)
        bg_surf = pygame.Surface(bg_rect.size)
        bg_surf.set_alpha(200)
        bg_surf.fill(settings.COLOR_BOARD_4)

        self.screen.blit(bg_surf, bg_rect)
        self.screen.blit(text_surf, text_rect)

        bottom = mouse_y + bg_surf.get_rect().bottom

        if mouse_tile_i is not None:
            tile_smth = hints[mouse_tile_i][1]
        else:
            return

        if tile_smth:
            tile_hints = tile_smth[mouse_tile_j]
        else:
            return

        if tile_hints:
            for n, tile_hint in enumerate(tile_hints):
                text_surf, text_rect = self.font.render(tile_hint, settings.COLOR_BOARD_0)
                text_rect.move_ip(mouse_x - 1, bottom + text_surf.get_height() * n - 14)

                bg_rect = text_rect.copy()
                bg_rect.width += 8
                bg_rect.height += 4

                text_rect.x += 4
                text_rect.y += 2

                bg_surf = pygame.Surface(bg_rect.size)
                bg_surf.set_alpha(200)
                bg_surf.fill(settings.COLOR_BOARD_4)

                self.screen.blit(bg_surf, bg_rect)
                self.screen.blit(text_surf, text_rect)

                bottom += text_surf.get_height() - 13

    def render_hints(self, all_hints):
        for i, board_hints in enumerate(all_hints):
            if not board_hints[0]:
                continue
            for n, hint in enumerate(board_hints[0]):
                board_rect = self.big_board.boards[i].rect

                text_surf, text_rect = self.font.render(hint, settings.COLOR_BOARD_0)

                text_rect.x = (
                    board_rect.right
                    if board_rect.right + text_surf.get_rect().width <= self.big_board.rect.right
                    else board_rect.left - text_surf.get_rect().width - 4
                )
                text_rect.y = board_rect.top + text_surf.get_rect().height * n

                bg_rect = text_rect.copy()
                bg_rect.width += 8
                bg_rect.height += 4

                bg_surf = pygame.Surface(bg_rect.size)
                bg_surf.set_alpha(200)
                bg_surf.fill(settings.COLOR_BOARD_4)

                text_rect.x += 4
                text_rect.y += 2

                self.screen.blit(bg_surf, bg_rect)
                self.screen.blit(text_surf, text_rect)

    def render_tile(self, mouse_tile_i, mouse_tile_j, i, j, mini_board, tile):
        if self.won:
            tile.draw(self.screen, settings.COLOR_BOARD_3)
        elif i == mouse_tile_i and j == mouse_tile_j and self._valid_move(i, j):
            tile.draw(self.screen, settings.COLOR_BOARD_1)
        elif j in mini_board.almost_winning_squares():
            tile.draw(self.screen, settings.COLOR_BOARD_ALERT_2)
        elif self.big_board.boards[j].almost_winners():
            tile.draw(self.screen, settings.COLOR_BOARD_ALERT_1)
        elif self.big_board.boards[j].winner():
            tile.draw(self.screen, settings.COLOR_BOARD_ALERT_0)
        else:
            tile.draw(self.screen, settings.COLOR_BOARD_3)

    def tile_hints(self, i, j, mini_board):
        hints = []
        if j in mini_board.almost_winning_squares():
            hints.append("wins this mini board")
            if i == j:
                hints.append("next move can play anywhere")
        if self.big_board.boards[j].almost_winners() and not (i == j and j in mini_board.almost_winning_squares()):
            hints.append("next move can win mini board")
        if self.big_board.boards[j].winner():
            hints.append("next move can play anywhere")
        return hints

    def render_mini_board(self, mouse_tile_i, mouse_tile_j, i, mini_board, next_move):
        if self.won:
            mini_board.draw(self.screen, settings.COLOR_BOARD_2)
        elif i == self.current_move_i:
            mini_board.draw(self.screen, settings.COLOR_BOARD_4)
        elif next_move:
            mini_board.draw(self.screen, settings.COLOR_BOARD_4)
        else:
            mini_board.draw(self.screen, settings.COLOR_BOARD_2)

    def render_mini_board_winner(self, mini_board):
        surf = self.font_bigger.render(
            settings.PLAYER_SYMBOLS[mini_board.winner()],
            settings.COLOR_MARK,
            settings.COLOR_BOARD_2,
        )[0]
        pygame.draw.rect(self.screen, settings.COLOR_BOARD_2, mini_board.rect)
        self.screen.blit(
            surf,
            (
                mini_board.rect.centerx - surf.get_rect().width / 2,
                mini_board.rect.centery - surf.get_rect().height / 2,
            ),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                self.handle_keypress(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_click(event)

    def handle_keypress(self, event: pygame.event.Event):
        if event.key == pygame.K_q:
            self.quit = True

    def handle_click(self, event: pygame.event.Event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_tile_i, mouse_tile_j, mouse_tile = -1, -1, None
        for i, mini_board in enumerate(self.big_board.boards):
            for j, tile in enumerate(mini_board.tiles):
                if tile.rect.collidepoint(mouse_x, mouse_y):
                    mouse_tile_i, mouse_tile_j, mouse_tile = i, j, tile

        if mouse_tile and self._valid_move(mouse_tile_i, mouse_tile_j):
            mouse_tile.set_player(self.current_move_player)
            if self.big_board.boards[mouse_tile_j].winner():
                self.current_move_i = -1
            else:
                self.current_move_i = mouse_tile_j
            self.current_move_player = 1 + (self.current_move_player % settings.NUM_PLAYERS)


if __name__ == "__main__":
    main = Main()
    main.run()
