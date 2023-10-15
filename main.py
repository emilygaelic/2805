# Tetris
import sys
import pygame
from ConfigurePage import ConfigurePage
from StartupPage import StartupPage
from GamePage import PlayGame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.mouse.set_visible(1)
    screen.fill((255, 255, 255))
    startupPage = StartupPage()
    startupPage.DrawStartupPage(screen)
    # start page
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                startupPage.HandleMouseClick(screen, mouse)
        pygame.display.flip()

if __name__ == "__main__":
    main()
