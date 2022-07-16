import pygame as pg
from typing import Tuple

import game.utils as utils
from hud.panel_hud import PanelHud
from game.resource_manager import ResourceManager

class BuildHud(PanelHud):
    def __init__(self, size:Tuple[int,int], hud_color, images):
        super().__init__(size, hud_color)
        self.images = images
        self.tiles_relative_pos = (10, 10)
        self.tiles = self.create_tile_icons(self.tiles_relative_pos)

    def draw(self, screen:pg.Surface, draw_pos:Tuple[int, int]=(0,0)):
        super().draw(screen, draw_pos)

        # draw tile icons
        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            render_pos = (draw_pos[0] + tile["rect"].topleft[0], draw_pos[1] + tile["rect"].topleft[1])
            screen.blit(icon, render_pos)

    def create_tile_icons(self, draw_pos):
        '''Loads the tiles to be drawn as icons for each tile buildable.'''
        relative_pos = [draw_pos[0]*0.84 + 10, draw_pos[1]*0.74 + 10]
        object_width = self.surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():
            pos = relative_pos.copy()
            image_tmp = image.copy()
            image_scale = utils.scale_image(image_tmp, w=object_width)
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

            relative_pos[0] += image_scale.get_width() + 10

        return tiles