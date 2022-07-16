import pygame as pg
from typing import Tuple

class PanelHud:
    '''Hud base class to inherite.'''
    def __init__(self, size:Tuple[int,int], hud_color):
        self.width, self.height = size
        self.hud_color = hud_color
        self.surface = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(0,0))
        self.surface.fill(self.hud_color)

    def draw(self, screen:pg.Surface, draw_pos:Tuple[int, int]=(0,0)):
        screen.blit(self.surface, draw_pos)