import pygame as pg
from typing import Tuple

import game.utils as utils
from hud.panel_hud import PanelHud
from game.resource_manager import ResourceManager

class ResourcesHud(PanelHud):
    def __init__(self, size:Tuple[int,int], hud_color, resource_manager:ResourceManager):
        super().__init__(size, hud_color)
        self.resource_manager = resource_manager

    def draw(self, screen:pg.Surface, draw_pos:Tuple[int, int]=(0,0)):
        super().draw(screen, draw_pos)
        pos = self.width - 400
        for resource, resource_value in self.resource_manager.resources.items():
            txt = resource + ": " + str(resource_value)
            utils.draw_text(screen, txt, 30, (255, 255, 255), (pos, 0))
            pos += 100