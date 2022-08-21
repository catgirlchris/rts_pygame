
import pygame as pg


def draw_text(screen: pg.Surface, text: str, size: int, color: tuple, pos: tuple()):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)


def rgb(r, g, b, a):
    return r, g, b, a


def scale_image(image: pg.Surface, w: int = None, h: int = None):
    if (w is None) and (h is None):
        pass

    elif h is None:
        scale = w / image.get_width()
        h = scale * image.get_height()
        image = pg.transform.scale(image, (int(w), int(h)))

    elif w is None:
        scale = h / image.get_height()
        w = scale * image.get_width()
        image = pg.transform.scale(image, (int(w), int(h)))
    else:
        image = pg.transform.scale(image, (int(w), int(h)))

    return image
