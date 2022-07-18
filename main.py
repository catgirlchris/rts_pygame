import pygame as pg
import os
from game.game import Game

def main():
    running = True
    playing = True
    x = 50
    y = 25
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((1200, 680), flags=pg.RESIZABLE)
    clock = pg.time.Clock()

    # implement menus

    # implement game
    game = Game(screen, clock)

    while running:
        # start menu

        while playing:
            # game loop
            game.run()


if __name__ == '__main__':
    main()