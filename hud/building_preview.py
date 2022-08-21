from typing import List
import pygame as pg
from game.camera import Camera
from game.settings import TILE_SIZE
from game.tile import Tile


class BuildingPreview:

    # def create_temp_tile(self, img, grid_pos):
    def __init__(self, img: pg.Surface, grid_pos, world_tiles: List[List[Tile]]):
        '''Crea el temptile a partir de una imagen y la posicion en el grid.\n'''
        self.image = img
        self.world_tiles = world_tiles
        self.show_surrounding_polygon: bool = True

        self.image.set_alpha(100)
        self.render_pos = self.world_tiles[grid_pos[0]][grid_pos[1]].render_pos
        self.iso_poly = self.world_tiles[grid_pos[0]][grid_pos[1]].iso_poly
        self.collision = self.world_tiles[grid_pos[0]][grid_pos[1]].collision

    def draw(self, screen: pg.Surface, camera: Camera, grass_tiles):
        '''Dibuja el surrounding_polygon y la imagen.\n
        Si show_surrounding_polygon es False entonces no dibuja el poligono.\n'''
        if self.show_surrounding_polygon:
            self.draw_surrounding_polygon(screen, camera, grass_tiles)

        screen.blit(
            self.image,
            (
                self.render_pos[0] + grass_tiles.get_width() / 2 + camera.scroll.x,
                self.render_pos[1] - (self.image.get_height() - TILE_SIZE) + camera.scroll.y
            )
        )

    def draw_surrounding_polygon(self, screen: pg.Surface, camera: Camera, grass_tiles):
        '''Dibuja un cuadrado alrededor de la imagen de preview_build.'''
        iso_poly = self.iso_poly
        iso_poly = [(x + grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y)
                    for x, y in iso_poly]
        if self.collision:
            pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
        else:
            pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
