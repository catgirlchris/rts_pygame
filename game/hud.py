import pygame as pg

class Hud:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.hud_color = (198, 155, 93, 175)

        # resources hud
        self.resources_surface = pg.Surface((width, height*0.02), pg.SRCALPHA)
        self.resources_surface.fill(self.hud_color)

        # building hud
        self.building_surface = pg.Surface((width*0.15, height*0.25), pg.SRCALPHA)
        self.building_surface.fill(self.hud_color)

        # select hud
        self.select_surface = pg.Surface((width*0.3, height*0.2), pg.SRCALPHA)
        self.select_surface.fill(self.hud_color)

    def draw(self, screen):
        screen.blit(self.resources_surface, (0,0))
        screen.blit(self.building_surface, (self.width*0.84, self.height*0.74))
        screen.blit(self.select_surface, (self.width*0.35, self.height*0.79))

