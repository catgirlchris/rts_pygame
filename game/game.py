"""
Game class.
"""
import sys

import pygame as pg
import pygame.constants

from game.world import World
from game.settings import TILE_SIZE
from game.utils import draw_text
from game.camera import Camera
from game.resource_manager import ResourceManager
from game.worker import Worker

from hud.hud_manager import Hud


class Game:
    """Game module.
    """
    def __init__(self, screen: pg.Surface, clock: pg.time.Clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.playing = False

        # entities
        self.entities = []

        # resource manager
        self.resource_manager = ResourceManager()

        # hud
        self.hud = Hud(self.width, self.height, self.resource_manager)

        # world
        self.world = World(
            (50, 50), (self.width, self.height), self.hud, self.entities, self.resource_manager)

        # workers
        for _ in range(10):
            Worker(self.world.world[25][25], self.world)

        # camera
        grid_size = (self.world.grid_length_x, self.world.grid_length_y)
        cam_start_pos = -(
            grid_size[0] * TILE_SIZE // 2 + 600), -(grid_size[1] * TILE_SIZE // 4 + 300)
        self.camera = Camera(self.width, self.height, cam_start_pos[0], cam_start_pos[1])

    def run(self):
        """Run method."""
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Events method."""
        for event in pg.event.get():
            if event.type == pg.constants.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        """Update method."""
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)

        for ent in self.entities:
            ent.update()

    def draw(self):
        """Draw method."""
        # clear
        self.screen.fill((0, 0, 0))

        # world
        self.world.draw(self.screen, self.camera)

        # hud
        self.hud.draw(self.screen)

        # fps
        fps = round(self.clock.get_fps())
        draw_text(
            self.screen,
            f'fps={fps}',
            25,
            (255, 255, 255),
            (10, 10)
        )

        pg.display.flip()
