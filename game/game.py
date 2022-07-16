import pygame as pg
from game.world import World
from game.settings import TILE_SIZE
from game.utils import draw_text
from game.camera import Camera
from hud.hud import Hud
from game.resource_manager import ResourceManager
from game.worker import Worker
import sys

class Game:

    def __init__(self, screen : pg.Surface, clock : pg.time.Clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # entities
        self.entities = []

        # resource manager
        self.resource_manager = ResourceManager()

        # hud
        self.hud = Hud(self.width, self.height, self.resource_manager)

        # world
        self.world = World(50, 50, self.width, self.height, self.hud, self.entities, self.resource_manager)

        # workers
        for _ in range(10): Worker(self.world.world[25][25], self.world)

        # camera
        cam_start_pos = -(self.world.grid_length_x*TILE_SIZE//2 + 600), -(self.world.grid_length_y*TILE_SIZE//4+300)
        self.camera = Camera(self.width, self.height, cam_start_pos[0], cam_start_pos[1])

        

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)

        for ent in self.entities:
            ent.update()

    def draw(self):
        # clear
        self.screen.fill((0, 0, 0))

        # world
        self.world.draw(self.screen, self.camera)

        # hud
        self.hud.draw(self.screen)

        # fps
        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps() )),
            25,
            (255, 255, 255),
            (10, 10)
        )

        pg.display.flip()
