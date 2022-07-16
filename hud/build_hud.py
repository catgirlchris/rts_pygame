import pygame as pg
from typing import Tuple

import game.utils as utils
import hud.hud
from hud.panel_hud import PanelHud
from game.resource_manager import ResourceManager

class BuildHud(PanelHud):
    def __init__(self, size:Tuple[int,int], hud_color, images):
        super().__init__(size, hud_color)
        self.images = images

    def draw(self, screen:pg.Surface, draw_pos:Tuple[int, int]=(0,0)):
        super().draw(screen, draw_pos)

    def create_build_hud(self):
        render_pos = [self.width*0.84 + 10, self.height*0.74 + 10]
        object_width = self.surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = hud.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name":image_name,
                    "icon":image_scale,
                    "image":self.images[image_name],
                    "rect":rect,
                    "affordable":True,
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles