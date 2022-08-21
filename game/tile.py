import pygame as pg

from game.drawable import Drawable


class Tile(Drawable):

    def __init__(self, grid_x: int, grid_y: int, rect: pg.Rect,
                 iso_poly, minx: int, miny: int, name: str, image: pg.image):
        # TODO change to tuples
        self.grid_pos = (grid_x, grid_y)
        self.cart_rect = rect
        self.iso_poly = iso_poly
        self.render_pos = (minx, miny)
        self.name = name
        self.image = image
        self.collision = False if (self.name == "") else True

    def draw(self, screen: pg.Surface, render_pos, image: pg.image,
             hover_outline=False, selected_outline=False):
        super().draw(screen, render_pos, image=image,
                     hover_outline=hover_outline, selected_outline=selected_outline)
