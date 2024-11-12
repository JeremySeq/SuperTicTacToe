import pygame

import settings
from analysis import Analysis


class Board:

    def __init__(self, rect: pygame.Rect):
        self.rect: pygame.Rect = rect
        self.analysis: Analysis = Analysis()

        self.winner_changed = True
        self.almost_winners_changed = True
        self.cached_analysis_winner = None
        self.cached_analysis_almost_winners = None

    def _rect_grid(self, big_rect: pygame.Rect, i: int) -> pygame.Rect:
        return pygame.Rect(
            big_rect.left + (i % 3) * (big_rect.width - settings.BOARD_PADDING) / 3 + settings.BOARD_PADDING,
            big_rect.top + (i // 3) * (big_rect.height - settings.BOARD_PADDING) / 3 + settings.BOARD_PADDING,
            (big_rect.width - settings.BOARD_PADDING * 4) / 3,
            (big_rect.height - settings.BOARD_PADDING * 4) / 3,
        )

    def draw(self, screen: pygame.Surface, color: pygame.Color):
        pygame.draw.rect(screen, color, self.rect)

    def winner(self) -> int:
        if self.winner_changed:
            self.winner_changed = False
            self.cached_analysis_winner = self.analysis.winner()
        return self.cached_analysis_winner

    def almost_winners(self):
        if self.almost_winners_changed:
            self.almost_winners_changed = False
            self.cached_analysis_almost_winners = self.analysis.almost_winners()
        return self.cached_analysis_almost_winners

    def almost_winning_squares(self):
        return [v for values in self.almost_winners().values() for v in values]


class MetaBoard(Board):

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)
        self.boards: list[TileBoard] = []

        for i in range(9):
            rect = self._rect_grid(self.rect, i)
            self.boards.append(TileBoard(rect, self))

    def to_list(self) -> list[int]:
        return [board.winner() for board in self.boards]

    def update_analysis(self):
        self.analysis.board = self.to_list()
        self.cached_analysis_winner = self.analysis.winner()
        self.cached_analysis_almost_winners = self.analysis.almost_winners()


class TileBoard(Board):

    def __init__(self, rect: pygame.Rect, parent: MetaBoard):
        super().__init__(rect)
        self.tiles: list[Tile] = []
        self.parent: MetaBoard = parent

        for i in range(9):
            rect = self._rect_grid(self.rect, i)
            self.tiles.append(Tile(rect, self))

    def to_list(self) -> list[int]:
        return [tile.player for tile in self.tiles]

    def update_analysis(self):
        self.analysis.board = self.to_list()
        self.cached_analysis_winner = self.analysis.winner()
        self.cached_analysis_almost_winners = self.analysis.almost_winners()
        self.parent.update_analysis()


class Tile:

    def __init__(self, rect: pygame.Rect, parent: TileBoard):
        self.rect: pygame.Rect = rect
        self.font: pygame.font.SysFont = pygame.freetype.SysFont("3270 Nerd Font Mono", 22)
        self.player: int = 0
        self.parent: TileBoard = parent

    def draw(self, screen: pygame.Surface, color: pygame.Color):
        pygame.draw.rect(screen, color, self.rect)

        letter = settings.PLAYER_SYMBOLS[self.player]

        surf = self.font.render(letter, settings.COLOR_MARK)[0]
        screen.blit(surf, (self.rect.centerx - 5, self.rect.centery - 4))

    def set_player(self, v):
        self.player = v
        self.parent.update_analysis()
