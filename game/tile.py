import pygame as pg

from game.camera import Camera
from game.settings import TILE_SIZE


class Tile:

    def __init__(self, grid_x, grid_y, rect, iso_poly, minx, miny, name):

        self.grid = [grid_x, grid_y]
        self.cart_rect = rect
        self.iso_poly = iso_poly
        self.render_pos = [minx, miny]
        self.name = name
        self.collision = False if self.name == "" else True

    def draw(self, screen: pg.Surface, render_pos, camera: Camera, grass_tiles, image: pg.image):
        screen.blit(
            image,
            (render_pos[0] + grass_tiles.get_width() / 2 + camera.scroll.x,
             render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
        )
