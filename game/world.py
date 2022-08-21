"""
Paquete de la clase Mundo.

blalbalblalbs
"""

from typing import List, Tuple
import random
import pygame as pg
import noise

import game
from game import building_manager
from game.building_manager import BuildingManager
from game.settings import TILE_SIZE
from game.camera import Camera
from game.resource_manager import ResourceManager
from game.tile import Tile
from game.buildings import Building, Lumbermill, Stonemasonry
# from game.worker import Worker as Worker

from hud.building_preview import BuildingPreview
from hud.hud_manager import Hud


class World():
    """Clase que maneja el mundo.
    """

    def __init__(
            self, grid_size: Tuple[int, int], screen_size: Tuple[int, int],
            hud: Hud, entities: List, resource_manager: ResourceManager):
        self.hud = hud
        self.entities = entities
        self.resource_manager = resource_manager
        self.grid_length_x = grid_size[0]
        self.grid_length_y = grid_size[1]
        self.grid_size = (self.grid_length_x, self.grid_length_y)
        self.width = screen_size[0]
        self.height = screen_size[1]

        self.perlin_scale = self.grid_length_x / 2

        # the polygons have double the witdh than height
        self.grass_tiles = pg.Surface(
            (self.grid_length_x * TILE_SIZE * 2,
             self.grid_length_y * TILE_SIZE + TILE_SIZE * 2)
        ).convert_alpha()

        self.tile_images = self.load_images()
        self.world: List[List[Tile]] = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.building_manager = BuildingManager(self.grid_size, self.entities)
        self.buildings = self.building_manager.buildings

        self.workers: List[List[game.Worker]] = [
            [None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.building_preview: BuildingPreview = None
        self.examine_tile = None
        self.hover_tile: Tuple[int, int] = None

    def update(self, camera: Camera):
        '''Metodo update que maneja todo lo perteneciente a World.\n'''
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        # right click deselect
        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        # preview y construccion de edificio
        self.building_preview = None
        m_grid_pos = self.mouse_to_grid(mouse_pos, camera.scroll)
        if (m_grid_pos is not None) and (self.can_place_tile(m_grid_pos)):
            if self.hud.selected_tile is not None:
                # crea building_preview
                img = self.hud.selected_tile.image.copy()
                self.building_preview = BuildingPreview(img, m_grid_pos, self.world)

                render_pos = self.world[m_grid_pos[0]][m_grid_pos[1]].render_pos
                collision = self.world[m_grid_pos[0]][m_grid_pos[1]].collision

                # construye edificio
                if mouse_action[0] and not collision:
                    self.add_building(
                        render_pos,
                        m_grid_pos,
                        self.resource_manager,
                        self.entities,
                        self.buildings)

            # si no hay algo seleccionado en build_hud
            else:
                # TODO refactor can_place_tile to better suit the needs here
                # checks if tile is not behind a hud_rect
                building = self.buildings[m_grid_pos[0]][m_grid_pos[1]]
                collision = self.world[m_grid_pos[0]][m_grid_pos[1]].collision
                self.hover_tile = m_grid_pos

                # if mouse_action[0] and collision:
                if mouse_action[0] and (building is not None):
                    self.examine_tile = m_grid_pos
                    self.hud.examined_tile = building
                # TODO  examine tile like tree or rock
                '''elif mouse_action[0] and (collision):
                    self.examine_tile = m_grid_pos
                    self.hud.examined_tile = m_grid_pos'''

    def add_building(
            self, render_pos, grid_pos,
            resource_manager: ResourceManager,
            entities: List, buildings: List):
        '''Añade un edificio a la lista de entidades, a la lista de edificios y actualiza el mundo. y las colisiones.'''

        # TODO mejorar esta llamada, es muy lioso usar diccionarios
        ent = self.building_manager.add_building(self.hud.selected_tile.name, render_pos,
                                                 grid_pos, resource_manager)
        # entities.append(ent)

        self.world[grid_pos[0]][grid_pos[1]].collision = True
        self.collision_matrix[grid_pos[1]][grid_pos[0]] = 1  # reverse access to collision matrix
        self.hud.selected_tile = None

    def draw(self, screen: pg.Surface, camera: Camera):
        # batch draw all grass blocks
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        # draw other things
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y].render_pos

                # drawing world tile_images
                tile = self.world[x][y]
                if tile.name != '':
                    draw_hover_outline = False
                    if (self.hover_tile is not None) and (
                            (x == self.hover_tile[0]) and (y == self.hover_tile[1])):
                        draw_hover_outline = True

                    tile_img = self.tile_images[tile.name]
                    tile.draw(
                        screen,
                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                         render_pos[1] - (tile_img.get_height() - TILE_SIZE) + camera.scroll.y),
                        tile_img, hover_outline=draw_hover_outline
                    )

                # draw buildings
                building = self.buildings[x][y]
                if (building is not None):
                    draw_hover_outline = False
                    if (self.hover_tile is not None) and (
                            (x == self.hover_tile[0]) and (y == self.hover_tile[1])):
                        draw_hover_outline = True

                    draw_selected_outline = False
                    if (self.examine_tile is not None) and (
                            (x == self.examine_tile[0]) and (y == self.examine_tile[1])):
                        draw_selected_outline = True

                    building.draw(
                        screen,
                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                         render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y),
                        hover_outline=draw_hover_outline, selected_outline=draw_selected_outline)

                # draw WORKERS
                worker = self.workers[x][y]
                if worker is not None:
                    screen.blit(
                        worker.image,
                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                         render_pos[1] - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y)
                    )

        # dibuja cuadro blanco/rojo cuando hay algo seleccionado en build_hud
        if self.building_preview is not None:
            self.building_preview.draw(screen, camera, self.grass_tiles)

        # HOVER 2: out of x,y loop
        if self.hover_tile is not None:
            tile_name = self.world[self.hover_tile[0]][self.hover_tile[1]].name
            render_pos = self.world[self.hover_tile[0]][self.hover_tile[1]].render_pos

            if tile_name != '':
                tile_hovered = self.world[self.hover_tile[0]][self.hover_tile[1]]
                tile_hovered.draw_hover_outline(
                    screen,
                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                     render_pos[1] - (tile_img.get_height() - TILE_SIZE) + camera.scroll.y),
                    tile_hovered.image)

    def create_world(self):
        """Crea el mundo."""
        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile.render_pos
                # half the tile_images will be in negative X coordinates, so we offset the x
                self.grass_tiles.blit(
                    self.tile_images['block'],
                    (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1])
                )

        return world

    def grid_to_world(self, grid_x, grid_y) -> Tile:
        '''Recieves a grid_position and returns a procedural generated Tile.\n'''
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)

        if (perlin >= 15) or (perlin <= -35):
            name = 'tree'
        else:
            if r == 1:
                name = 'tree'
            elif r == 2:
                name = 'rock'
            else:
                name = ''
        if name != '':
            tile_image = self.tile_images[name]
        else:
            tile_image = None
        tile_out = Tile(grid_x, grid_y, rect, iso_poly, minx, miny, name, tile_image)

        return tile_out

    def create_collision_matrix(self):
        '''NOTA: esta matriz de colision se accede al contrario, es decir,
        cm[y][x] en vez de c_m[x][y].'''
        # 1 is good to go, 0 is collision
        collision_matrix = [
            [1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y].collision:
                    collision_matrix[y][x] = 0
        return collision_matrix

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def mouse_to_grid(self, mouse_pos: Tuple[int, int], scroll: pg.Vector2):
        '''Transforma de mouse_pos en pixeles a coordenadas grid_pos.
        Devuelve la coordenada de la casilla donde esta el ratón.
        Si mouse_pos está dentro de los límites y anteriormente estuvo en una, devuelve hover_tile.
        Si no está dentro de los límites devuelve None.'''
        #  (removing camera scroll and offset)
        x, y = mouse_pos
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y

        # transfrom to cart
        cart_y = (2 * world_y - world_x) / 2
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
        """Load images."""
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        lumbermill = pg.image.load("assets/graphics/lumbermill.png").convert_alpha()
        stonemasonry = pg.image.load("assets/graphics/stonemasonry.png").convert_alpha()
        tree = pg.image.load("assets/graphics/tree.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()

        images = {
            "lumbermill": lumbermill,
            "stonemasonry": stonemasonry,
            "tree": tree,
            "rock": rock,
            "block": block
        }

        return images

    def can_place_tile(self, grid_pos):
        '''Comprueba si dada (x,y), esas coordenadas estan dentro de los limites
         y si hay un panel dentro.'''
        mouse_on_panel = False
        for hud_panel in self.hud.hud_list:
            hud_rect = hud_panel.rect
            if hud_rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True

        world_bounds = (
            0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False
