from turtle import right
from typing import Tuple
import pygame as pg


class Camera:


    def __init__(self, width:int, height:int):

        self.width = width
        self.height = height

        self.top_border       = self.height*0.96
        self.right_border     = self.width*0.96
        self.bottom_border    = self.height*0.04
        self.left_border      = self.width*0.04

        self.scroll = pg.Vector2(0, 0)
        self.dx = 0
        self.dy = 0
        self.speed = 25


    def update(self):
        mouse_pos = pg.mouse.get_pos()
        
        # get scroll direction
        self.dx, self.dy = self.get_direction(mouse_pos)
        
        # update camera scroll
        if (self.dx != 0) and (self.dy != 0):
            self.scroll.x += self.dx*self.speed // 2
            self.scroll.y += self.dy*self.speed // 2
        else:
            self.scroll.x += self.dx*self.speed
            self.scroll.y += self.dy*self.speed


    def get_direction(self, mouse_pos:Tuple[int, int]):
        '''Recoge la dirección a la que se quiere mover la cámara.'''
        
        # x movement
        if mouse_pos[0] > self.right_border:
            dx = -1
        elif mouse_pos[0] < self.left_border:
            dx = 1
        else:
            dx = 0

        # y movement
        if mouse_pos[1] > self.top_border:
            dy = -1
        elif mouse_pos[1] < self.left_border:
            dy = 1
        else:
            dy = 0

        return dx, dy