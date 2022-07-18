from distutils.command.build_clib import build_clib
from typing import List
import pygame as pg
import random
import noise

from game.camera import Camera
from game.resource_manager import ResourceManager
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
        self.tiles = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.temp_tile = None
        self.examine_tile = None
        self.hover_tile : tuple[int, int] = None
    
    def update(self, camera:Camera):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        # right click deselect
        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        # building functionality
        self.temp_tile = None
        # si hay algo seleccionado en build_hud
        if self.hud.selected_tile is not None:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if grid_pos is not None:
                # si se puede colocar 
                if self.can_place_tile(grid_pos):

                    img = self.hud.selected_tile["image"].copy()
                    img.set_alpha(100)

                    render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                    iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]

                    self.temp_tile = {
                        "image": img,
                        "render_pos": render_pos,
                        "iso_poly": iso_poly,
                        "collision": collision,
                    }

                    # creating a building
                    if mouse_action[0] and not collision:
                        self.add_building(render_pos, grid_pos, self.resource_manager, self.entities, self.buildings)
        
        # si no hay algo seleccionado en build_hud
        else:
            # examine tile in world by clicking it
            m_grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if m_grid_pos is not None:
                # TODO refactor can_place_tile to better suit the needs here
                # checks if tile is not behind a hud_rect
                if self.can_place_tile(m_grid_pos):
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
                
                # drawing world tiles
                tile = self.world[x][y]['tile']
                if tile != '':
                    screen.blit(self.tiles[tile], 
                        (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                        render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                    '''if (self.hover_tile is not None) and (self.buildings[x][y] is None):
                        if (x == self.hover_tile[0]) and (y == self.hover_tile[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                            pg.draw.polygon(screen, (150, 200, 200), mask, 3)'''
                            
                    '''if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
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
        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x,y in iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

        # HOVER 2: out of x,y loop
        if self.hover_tile is not None:
            #if (x == self.hover_tile[0]) and (y == self.hover_tile[1]):
            tile_name = self.world[self.hover_tile[0]][self.hover_tile[1]]["tile"]
            render_pos = self.world[self.hover_tile[0]][self.hover_tile[1]]["render_pos"]
            if tile_name != "":
                mask = pg.mask.from_surface( self.tiles[tile_name] ).outline()
                #mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tiles[tile_name].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                pg.draw.polygon(screen, (150, 200, 200), mask, 3)
        
        # EXAMINE 2: out of x,y loop
        '''if self.examine_tile is not None:
            if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                mask = pg.mask.from_surface(self.tiles[tile]).outline()
                mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x,y in mask]
                pg.draw.polygon(screen, (255, 255, 255), mask, 3)'''

    def create_world(self):
        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile['render_pos']
                # half the tiles will be in negative X coordinates, so we offset the x
                self.grass_tiles.blit(
                    self.tiles['block'],
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
        mouse_on_panel = False
        for rect in [ self.hud.resources_hud.rect, self.hud.build_hud.rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True

        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False