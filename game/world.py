from distutils.command.build_clib import build_clib
from typing import List, Tuple
import pygame as pg
import random
import noise

from game.camera import Camera
from game.resource_manager import ResourceManager
from hud.building_preview import BuildingPreview
from .settings import TILE_SIZE
from hud.hud_manager import Hud
from game.buildings import Lumbermill, Stonemasonry

import random

class World():

    def __init__(self, grid_length_x, grid_length_y, width, height, hud:Hud, entities, resource_manager):
        self.hud = hud
        self.entities = entities
        self.resource_manager = resource_manager
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.perlin_scale = grid_length_x/2

        # the polygons have double the witdh than height
        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + TILE_SIZE*2)).convert_alpha()
        self.tile_images = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.building_preview:BuildingPreview = None
        self.examine_tile = None
        self.hover_tile : tuple[int, int] = None


    def update(self, camera:Camera):
        '''Metodo update que maneja todo lo perteneciente a World.\n'''
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        # right click deselect
        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        # preview y construccion de edificio
        self.building_preview = None
        m_grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if (m_grid_pos is not None) and (self.can_place_tile(m_grid_pos)):
            if self.hud.selected_tile is not None:
                # crea building_preview
                img = self.hud.selected_tile["image"].copy()
                self.building_preview = BuildingPreview(img, m_grid_pos, self.world)

                render_pos = self.world[m_grid_pos[0]][m_grid_pos[1]]["render_pos"]
                collision = self.world[m_grid_pos[0]][m_grid_pos[1]]["collision"]
                
                # construye edificio
                if mouse_action[0] and not collision:
                    self.add_building(render_pos, m_grid_pos, self.resource_manager, self.entities, self.buildings)
    
            # si no hay algo seleccionado en build_hud
            else:
                # TODO refactor can_place_tile to better suit the needs here
                # checks if tile is not behind a hud_rect
                building = self.buildings[m_grid_pos[0]][m_grid_pos[1]]
                collision = self.world[m_grid_pos[0]][m_grid_pos[1]]["collision"]
                self.hover_tile = m_grid_pos
                
                #if mouse_action[0] and collision:
                if mouse_action[0] and (building is not None):
                    self.examine_tile = m_grid_pos
                    self.hud.examined_tile = building
                # TODO  examine tile like tree or rock
                '''elif mouse_action[0] and (collision):
                    self.examine_tile = m_grid_pos
                    self.hud.examined_tile = m_grid_pos'''


    def add_building(self, render_pos, grid_pos, resource_manager:ResourceManager, entities:List, buildings:List):
        '''Añade un edificio a la lista de entidades, a la lista de edificios y actualiza el mundo. y las colisiones.'''
        if self.hud.selected_tile["name"] == "lumbermill":
            ent = Lumbermill(render_pos, self.resource_manager)
            self.entities.append(ent)
            self.buildings[grid_pos[0]][grid_pos[1]] = ent
        elif self.hud.selected_tile["name"] == "stonemasonry":
            ent = Stonemasonry(render_pos, self.resource_manager)
            self.entities.append(ent)
            self.buildings[grid_pos[0]][grid_pos[1]] = ent

        #self.world[grid_pos[0]][grid_pos[1]]["tile"] = self.hud.selected_tile["name"]
        self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
        self.collision_matrix[grid_pos[1]][grid_pos[0]] = 1 # reverse access to collision matrix
        self.hud.selected_tile = None




    def draw(self, screen:pg.Surface, camera:Camera):
        # batch draw all grass blocks
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        # draw other things
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]['render_pos']
                
                # drawing world tile_images
                tile = self.world[x][y]['tile']
                if tile != '':
                    screen.blit(self.tile_images[tile], 
                        (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                        render_pos[1] - (self.tile_images[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                    '''if (self.hover_tile is not None) and (self.buildings[x][y] is None):
                        if (x == self.hover_tile[0]) and (y == self.hover_tile[1]):
                            mask = pg.mask.from_surface(self.tile_images[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tile_images[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                            pg.draw.polygon(screen, (150, 200, 200), mask, 3)'''
                            
                    '''if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(self.tile_images[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tile_images[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)'''
                
                # draw buildings
                building = self.buildings[x][y]
                if (building is not None) and (self.buildings[x][y]) is not None:
                    screen.blit(building.image, 
                        (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                        render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    if self.hover_tile is not None:
                        if (x == self.hover_tile[0]) and (y == self.hover_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                            pg.draw.polygon(screen, (150, 200, 200), mask, 3)
                            
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)


                # draw WORKERS
                worker = self.workers[x][y]
                if worker is not None:
                    screen.blit(worker.image, 
                        (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                        render_pos[1] - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y))

        # dibuja cuadro blanco/rojo cuando hay algo seleccionado en build_hud
        if self.building_preview is not None:
            self.building_preview.draw(screen, camera, self.grass_tiles)


        # HOVER 2: out of x,y loop
        if self.hover_tile is not None:
            #if (x == self.hover_tile[0]) and (y == self.hover_tile[1]):
            tile_name = self.world[self.hover_tile[0]][self.hover_tile[1]]["tile"]
            render_pos = self.world[self.hover_tile[0]][self.hover_tile[1]]["render_pos"]
            grid_pos = self.world[self.hover_tile[0]][self.hover_tile[1]]["grid"]

            if tile_name != "":
                mask = pg.mask.from_surface( self.tile_images[tile_name] ).outline()
                #mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tile_images[tile_name].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                pg.draw.polygon(screen, (150, 200, 200), mask, 3)
        
        # EXAMINE 2: out of x,y loop
        '''if self.examine_tile is not None:
            if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                mask = pg.mask.from_surface(self.tile_images[tile]).outline()
                mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tile_images[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                pg.draw.polygon(screen, (255, 255, 255), mask, 3)'''



    def create_world(self):
        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile['render_pos']
                # half the tile_images will be in negative X coordinates, so we offset the x
                self.grass_tiles.blit(
                    self.tile_images['block'],
                    (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1])
                    )
        
        return world
    
    def grid_to_world(self, grid_x, grid_y):
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
        ]

        iso_poly = [self.cart_to_iso(x, y) for x,y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x/self.perlin_scale, grid_y/self.perlin_scale)

        if (perlin >= 15) or (perlin <= -35):
            tile = 'tree'
        else:
            if r == 1:
                tile = 'tree'
            elif r == 2:
                tile = 'rock'
            else:
                tile = ''

        out = {
            'grid': [grid_x, grid_y],
            'cart_rect': rect,
            'iso_poly': iso_poly,
            'render_pos': [minx, miny],
            'tile': tile,
            'collision': False if tile == "" else True,
        }

        return out


    def create_collision_matrix(self):
        '''NOTE: this collision matrix is accesses reversed cm[y][x] instead of the usual.'''
        # 1 is good to go, 0 is collision
        collision_matrix = [[1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0
        return collision_matrix


    def cart_to_iso(self, x, y):
        iso_x = x-y
        iso_y = (x+y)/2
        return iso_x, iso_y

    def mouse_to_grid(self, x:int, y:int, scroll:pg.Vector2):
        '''Transform from world position from the mouse position.
        Can return the hover_tile if mouse is not out of the world.
        If mouse is out of world and there is no hover tile then it returns None.'''
        #  (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width()/2
        world_y = y - scroll.y

        # transfrom to cart
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x

        # transfrom to grid coordinate
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)

        # if grid_pos is in-bounds of the world
        if (0 <= grid_x < self.grid_length_x) and (0 <= grid_y < self.grid_length_y):
            return grid_x, grid_y
        # else if there was a last grid hovered, return that
        elif self.hover_tile is not None:
            return self.hover_tile
        # else return None
        else:
            return None

    def load_images(self):
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        building1 = pg.image.load("assets/graphics/building01.png").convert_alpha()
        building2 = pg.image.load("assets/graphics/building02.png").convert_alpha()
        tree = pg.image.load("assets/graphics/tree.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()

        images = {
            "building1": building1,
            "building2": building2,
            "tree": tree,
            "rock": rock,
            "block": block
        }

        return images


    def can_place_tile(self, grid_pos):
        '''Comprueba si dada (x,y), esas coordenadas estan dentro de los limites y si hay un panel dentro.'''
        mouse_on_panel = False
        for hud_panel in self.hud.hud_list:
            hud_rect = hud_panel.rect
            if hud_rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True

        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False