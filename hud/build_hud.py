import pygame as pg
from typing import Tuple

import game.utils as utils
from hud.panel_hud import PanelHud
from game.resource_manager import ResourceManager

class BuildHud(PanelHud):
    def __init__(self, pos:Tuple[int,int], size:Tuple[int,int], hud_color, resource_manager, images):
        super().__init__(pos, size, hud_color)
        self.resource_manager = resource_manager
        self.images = images
        self.tiles = self.create_tile_icons()

    def draw(self, screen:pg.Surface):
        super().draw(screen)
        draw_pos = self.pos
        # draw tile icons
        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

    def create_tile_icons(self):
        '''Loads the tiles to be drawn as icons for each tile buildable.'''
        render_pos = [self.pos[0]+10, self.pos[1]+10]
        object_width = self.surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():
            pos = render_pos.copy()
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

            render_pos[0] += image_scale.get_width() + 10

        return tiles