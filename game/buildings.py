
import pygame as pg
from game import drawable

from game import resource_manager


class Building(drawable.Drawable):

    def __init__(
            self, pos, name: str, image: pg.image,
            resource_manager: resource_manager.ResourceManager, resource=None):
        self.image = image
        self.name = name
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

        self.resource = resource

    def update(self):
        if self.resource is not None:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.resource_manager.resources[self.resource] += 1
                self.resource_cooldown = now

    def draw(self, screen: pg.Surface, render_pos, image: pg.image = None,
             hover_outline=False, selected_outline=False):
        super().draw(screen, render_pos, self.image, hover_outline, selected_outline)


class Lumbermill(Building):
    name = "lumbermill"
    resource = "wood"
    image = pg.image.load("assets/graphics/lumbermill.png")

    def __init__(self, pos, resource_manager: resource_manager.ResourceManager):
        super().__init__(
            pos,
            Lumbermill.name,
            Lumbermill.image,
            resource_manager,
            resource=Lumbermill.resource
        )

    def update(self):
        super().update()


class Stonemasonry(Building):
    name = "stonemasonry"
    resource = "stone"
    image = pg.image.load("assets/graphics/stonemasonry.png")

    def __init__(self, pos, resource_manager: resource_manager.ResourceManager):
        super().__init__(
            pos,
            Stonemasonry.name,
            Stonemasonry.image,
            resource_manager,
            resource=Stonemasonry.resource
        )

    def update(self):
        super().update()
