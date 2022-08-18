
import pygame as pg
from typing import Dict, List, Tuple
from game.drawable import Drawable

from game.resource_manager import ResourceManager
import game.utils as utils
from hud.panel_hud import PanelHud


class TileIcon(Drawable):
    """Tile de los iconos que muestra build_hud."""
    def __init__(self, render_pos: Tuple[int, int], icon: pg.Surface, image: pg.Surface, name: str):
        self.name = name
        self.icon = icon
        self.image = image
        self.rect = image.get_rect(topleft=render_pos)
        self.afforfable = True

    def draw(self, screen: pg.Surface):
        super().draw(screen)


class BuildHud(PanelHud):

    def __init__(self, pos: Tuple[int, int],
                 size: Tuple[int, int], hud_color,
                 resource_manager: ResourceManager,
                 images: Dict[str, pg.Surface]):
        super().__init__(pos, size, hud_color)
        self.resource_manager = resource_manager
        self.images = images
        self.tiles: List[TileIcon] = self.create_tile_icons()

    def draw(self, screen: pg.Surface):
        super().draw(screen)

        # draw tile icons
        for tile_icon in self.tiles:
            icon = tile_icon.icon.copy()
            if not tile_icon.afforfable:
                icon.set_alpha(100)
            screen.blit(icon, tile_icon.rect.topleft)

    def create_tile_icons(self) -> List[TileIcon]:
        '''Loads the tiles to be drawn as icons for each tile buildable.'''
        render_pos = [self.pos[0] + 10, self.pos[1] + 10]
        object_width = self.surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = utils.scale_image(image_tmp, w=object_width)
            image = self.images[image_name]

            tile_icon = TileIcon(pos, image_scale, image, image_name)
            tiles.append(tile_icon)

            render_pos[0] += image_scale.get_width() + 10

        return tiles
