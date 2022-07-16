from typing import Tuple
import pygame as pg

from game.buildings import Stonemasonry
from game.resource_manager import ResourceManager
from hud.build_hud import BuildHud
from hud.resources_hud import ResourcesHud
import game.utils as utils

class Hud:
    def __init__(self, width, height, resource_manager:ResourceManager):
        self.resource_manager = resource_manager
        self.width = width
        self.height = height
        self.resources_hud_start_pos = (0,0)
        self.build_hud_start_pos = (self.width*0.84, self.height*0.74)


        self.hud_color = utils.rgb(150, 100, 200, 175)

        # resources hud
        self.resources_hud = ResourcesHud(self.resources_hud_start_pos, (width, height*0.03), self.hud_color, self.resource_manager)

        # build hud
        self.images = self.load_images()
        self.build_hud = BuildHud(self.build_hud_start_pos, (width*0.15, height*0.25), self.hud_color, self.resource_manager, self.images)

        # select hud
        self.select_surface = pg.Surface((width*0.3, height*0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width*0.35, self.height*0.79))
        self.select_surface.fill(self.hud_color)

        self.selected_tile = None
        self.examined_tile = None


    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        #TODO mover a build_hud?
        for tile in self.build_hud.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False

            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile


    def draw(self, screen:pg.Surface):

        # resources
        self.resources_hud.draw(screen)

        # build
        self.build_hud.draw(screen)
        
        # select
        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width*0.35, self.height*0.79))
            #img = self.images[self.examined_tile["tile"]].copy()
            img = self.examined_tile.image.copy()
            img_scale = utils.scale_image(img, h=h*0.70)
            screen.blit(img_scale, (self.width*0.35 + 10, self.height*0.79 + 40))
            #draw_text(screen, self.examined_tile["tile"], 40, (255, 255, 255), self.select_rect.center)
            utils.draw_text(screen, self.examined_tile.name, 40, (255, 255, 255), self.select_rect.topleft)



    def load_images(self):
        lumbermill = pg.image.load("assets/graphics/building01.png")
        stonemasonry = pg.image.load("assets/graphics/building02.png")

        images = {
            "lumbermill": lumbermill,
            "stonemasonry": stonemasonry,
        }

        return images
