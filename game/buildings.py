
import pygame as pg
from game.camera import Camera

from game.resource_manager import ResourceManager
from game.settings import TILE_SIZE


class Building:

    def __init__(
            self, pos, name: str, image: pg.image,
            resource_manager: ResourceManager, resource=None):
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

    def draw(self, screen: pg.Surface, render_pos, hover_outline=False, selected_outline=False):
        screen.blit(
            self.image,
            (render_pos[0],
             render_pos[1])
        )

        if hover_outline:
            self.draw_hover_outline(screen, render_pos)

        if selected_outline:
            self.draw_selected_outline(screen, render_pos)

    def draw_hover_outline(self, screen: pg.Surface, render_pos):
        self.draw_outline(screen, render_pos, (150, 200, 200), 3)

    def draw_selected_outline(self, screen: pg.Surface, render_pos):
        self.draw_outline(screen, render_pos, (255, 255, 255), 3)

    def draw_outline(self, screen: pg.Surface, render_pos, color, width: int):
        mask = pg.mask.from_surface(self.image).outline()
        mask = [
            (x + render_pos[0],
             y + render_pos[1])
            for x, y in mask
        ]
        pg.draw.polygon(screen, color, mask, width)


class Lumbermill(Building):
    name = "lumbermill"
    resource = "wood"
    image = pg.image.load("assets/graphics/building01.png")

    def __init__(self, pos, resource_manager: ResourceManager):
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
    image = pg.image.load("assets/graphics/building02.png")

    def __init__(self, pos, resource_manager: ResourceManager):
        super().__init__(
            pos,
            Stonemasonry.name,
            Stonemasonry.image,
            resource_manager,
            resource=Stonemasonry.resource
        )

    def update(self):
        super().update()
