# Tetris
import sys

import pygame
from ConfigurePage import ConfigurePage
from StartupPage import StartupPage


def main():
    # start page code
    pygame.init()
    win = pygame.display.set_mode((1000, 700))
    pygame.mouse.set_visible(1)
    win.fill((255, 255, 255))
    startup_page = StartupPage()
    startup_page.draw_startup_page(win)
    go = True
    # start page
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                startup_page.handle_mouse_click(win, mouse)

        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
