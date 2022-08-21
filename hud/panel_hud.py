import pygame as pg
from typing import Tuple


class PanelHud:
    '''Hud base class to inherite.'''
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], hud_color):
        self.pos = pos
        self.width, self.height = size
        self.hud_color = hud_color
        self.surface = pg.Surface(size, pg.SRCALPHA)
        self.rect: pg.Rect = self.surface.get_rect(topleft=pos)
        self.surface.fill(self.hud_color)

    def draw(self, screen: pg.Surface):
        screen.blit(self.surface, self.pos)
