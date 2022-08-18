import pygame as pg
from typing import Tuple

import game.utils as utils
from hud.panel_hud import PanelHud
from game.resource_manager import ResourceManager


class ResourcesHud(PanelHud):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], hud_color,
                 resource_manager: ResourceManager):
        super().__init__(pos, size, hud_color)
        self.resource_manager = resource_manager

    def draw(self, screen: pg.Surface):
        # TODO improve and fix the positioning so it takes the panel into account
        super().draw(screen)
        pos = self.width - 400
        for resource, resource_value in self.resource_manager.resources.items():
            txt = resource + ": " + str(resource_value)
            utils.draw_text(screen, txt, 30, (255, 255, 255), (pos, 0))
            pos += 100
