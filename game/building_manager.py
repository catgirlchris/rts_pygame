from typing import List, Tuple
import pygame as pg

from game import buildings, resource_manager
from game.buildings import Building, Lumbermill, Stonemasonry

class BuildingManager:

    def __init__(self, grid_length: Tuple[int, int], entities: List):
        self.buildings: List[List[buildings.Building]] = [
            [None for x in range(grid_length[0])] for y in range(grid_length[1])]
        self.entities = entities

    def update(self):
        pass

    def add_building(
            self, tile_name, render_pos, grid_pos,
            resource_manager: resource_manager.Resource_manager):
        '''Añade un edificio a la lista de edificios.'''
        if tile_name == "lumbermill":
            ent = Lumbermill(render_pos, resource_manager)
            self.buildings[grid_pos[0]][grid_pos[1]] = ent
        elif tile_name == "stonemasonry":
            ent = Stonemasonry(render_pos, resource_manager)
            self.buildings[grid_pos[0]][grid_pos[1]] = ent

        return ent
