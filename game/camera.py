from turtle import right
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

        # x movement
        if mouse_pos[0] > self.right_border:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width*0.03:
            self.dx = self.speed
        else:
            self.dx = 0

        # y movement
        if mouse_pos[1] > self.top_border:
            self.dy = -self.speed
        elif mouse_pos[1] < self.left_border:
            self.dy = self.speed
        else:
            self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy