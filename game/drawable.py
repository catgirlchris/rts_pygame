import pygame as pg


class Drawable():

    def __init__(self, image: pg.Surface):
        self.image: pg.Surface = image

    def draw(self, screen: pg.Surface, render_pos, image: pg.Surface = None,
             hover_outline=False, selected_outline=False):

        if image is None:
            image = self.image

        screen.blit(
            image,
            (render_pos[0], render_pos[1])
        )

        if hover_outline:
            self.draw_hover_outline(screen, render_pos)

        if selected_outline:
            self.draw_selected_outline(screen, render_pos)

    def draw_outline(self, screen: pg.Surface, render_pos, color,
                     width: int, image: pg.Surface = None):
        if image is None:
            image = self.image

        mask = pg.mask.from_surface(image).outline()
        mask = [
            (x + render_pos[0],
             y + render_pos[1])
            for x, y in mask
        ]
        pg.draw.polygon(screen, color, mask, width)

    def draw_hover_outline(self, screen: pg.Surface, render_pos, image: pg.Surface = None):
        if image is None:
            image = self.image

        self.draw_outline(screen, render_pos, (150, 200, 200), 3)

    def draw_selected_outline(self, screen: pg.Surface, render_pos, image: pg.Surface = None):
        if image is None:
            image = self.image

        self.draw_outline(screen, render_pos, (255, 255, 255), 3)
