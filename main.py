# Tetris
import sys

import pygame
from ConfigurePage import ConfigurePage
from StartupPage import StartupPage



def main():
    # start page code
    pygame.init()
    win = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Welcome')
    pygame.mouse.set_visible(1)
    win.fill('white')
    startup_page = StartupPage()

    # configure page code

    configure_page = ConfigurePage()
    clock = pygame.time.Clock()

    go = True
    go2 = True
    # start page
    while go:
        startup_page.draw_startup_page(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                startup_page.handle_mouse_click(win, mouse, go)

                while go2:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            go = False
                            go2 = False
                        elif e.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            configure_page.handle_mouse_click(win, mouse_pos, go2)


                    pygame.display.flip()

                    clock.tick(30)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
