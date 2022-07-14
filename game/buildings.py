
import pygame as pg

from game.resource_manager import ResourceManager

class Lumbermill:

    def __init__(self, pos, resource_manager:ResourceManager):
        image = pg.image.load("assets/graphics/building01.png")
        self.image = image
        self.name = "lumbermill"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0

    def update(self):
        self.counter += 1



class Stonemasonry:

    def __init__(self, pos, resource_manager:ResourceManager):
        image = pg.image.load("assets/graphics/building02.png")
        self.image = image
        self.name = "stonemasonry"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0

    def update(self):
        self.counter += 1
