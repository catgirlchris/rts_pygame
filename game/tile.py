import pygame as pg

class Tile:

    def __init__(self, grid_x, grid_y, rect, iso_poly, minx, miny, name):

        self.grid = [grid_x, grid_y]
        self.cart_rect = rect
        self.iso_poly = iso_poly
        self.render_pos = [minx, miny]
        self.name = name
        self.collision = False if self.name == "" else True

        '''self.tile = {
            'grid': [grid_x, grid_y],
            'cart_rect': rect,
            'iso_poly': iso_poly,
            'render_pos': [minx, miny],
            'tile': tile,
            'collision': False if tile == "" else True,
        }'''
