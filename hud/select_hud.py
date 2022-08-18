import pygame as pg
from typing import Tuple

import game.utils as utils
from hud.panel_hud import PanelHud


class SelectHud(PanelHud):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], hud_color, images):
        super().__init__(pos, size, hud_color)
        self.images = images

    def draw(self, screen: pg.Surface, examined_tile):
        super().draw(screen)
        if examined_tile is not None:
            w, h = self.rect.width, self.rect.height
            # img = self.images[self.examined_tile["tile"]].copy()
            img = examined_tile.image.copy()
            img_scale = utils.scale_image(img, h=h * 0.70)
            screen.blit(img_scale, (self.pos[0] + 10, self.pos[1] + 10))
            # draw_text(screen, examined_tile["tile"], 40, (255, 255, 255), self.rect.center)
            utils.draw_text(screen, examined_tile.name, 40, (255, 255, 255), self.rect.topleft)
