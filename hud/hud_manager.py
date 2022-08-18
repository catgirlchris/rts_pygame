
import pygame as pg

from game.resource_manager import ResourceManager
from hud.build_hud import BuildHud
from hud.resources_hud import ResourcesHud
import game.utils as utils
from hud.select_hud import SelectHud


class Hud:
    # TODO singleton
    def __init__(self, width, height, resource_manager: ResourceManager):
        '''Construye al hud manager.\n
        Pide un tamaño y acceso al resource manager.\n
        Se encarga de manejar los paneles de la GUI.\n'''
        self.resource_manager = resource_manager
        self.width = width
        self.height = height
        self.hud_list = list()

        # childs starting position and size
        self.resources_hud_start_pos = (0, 0)
        self.resources_hud_start_size = (self.width, self.height * 0.03)

        self.build_hud_start_pos = (self.width * 0.84, self.height * 0.74)
        self.build_hud_start_size = (self.width * 0.15, self.height * 0.25)

        self.select_hud_start_pos = (self.width * 0.3, self.height * 0.78)
        self.select_hud_start_size = (self.width * 0.35, self.height * 0.20)

        self.hud_color = utils.rgb(150, 100, 200, 175)
        self.images = self.load_images()

        # resources hud
        self.resources_hud = ResourcesHud(self.resources_hud_start_pos,
                                          self.resources_hud_start_size, self.hud_color,
                                          self.resource_manager)
        self.hud_list.append(self.resources_hud)

        # build hud
        self.build_hud = BuildHud(self.build_hud_start_pos,
                                  self.build_hud_start_size,
                                  self.hud_color, self.resource_manager,
                                  self.images)
        self.hud_list.append(self.build_hud)

        # select hud
        self.select_hud = SelectHud(self.select_hud_start_pos,
                                    self.select_hud_start_size,
                                    self.hud_color,
                                    self.images)
        self.hud_list.append(self.select_hud)

        self.selected_tile = None
        ''' build_hud selected tile '''

        self.examined_tile = None
        ''' examine_hud selected tile'''

    def update(self):
        '''Metodo update de hud_manager.
        Llama a los metodos update de los paneles que maneja.'''
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        # TODO mover a build_hud?
        for tile in self.build_hud.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False

            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen: pg.Surface):
        '''Metodo draw de hud_manager.
        Dibuja las ventanas que maneja.'''
        # resources
        self.resources_hud.draw(screen)

        # build
        self.build_hud.draw(screen)

        # select
        self.select_hud.draw(screen, self.examined_tile)

    def load_images(self):
        '''Carga las imágenes necesarias para los paneles.'''
        lumbermill = pg.image.load("assets/graphics/lumbermill.png")
        stonemasonry = pg.image.load("assets/graphics/stonemasonry.png")

        images = {
            "lumbermill": lumbermill,
            "stonemasonry": stonemasonry,
        }

        return images
