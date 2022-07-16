from typing import Tuple
import pygame as pg

def draw_text(screen:pg.Surface, text:str, size:int, color:tuple, pos:tuple()):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)

def rgb(r,g,b,a):
    return r,g,b,a