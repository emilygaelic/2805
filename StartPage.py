# Tetris
import tkinter
import pygame


def main():
    pygame.init()
    win = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Welcome')
    pygame.mouse.set_visible(1)
    pic = pygame.image.load('TetrisLogo.png')
    win.fill('white')
    win.blit(pic, pic.get_rect(center=win.get_rect().center))
    font = pygame.font.SysFont('Courier', 50, 'bold')
    font2 = pygame.font.SysFont('Courier', 20)
    yr = font2.render('2023, 2805ICT', True, (0, 0, 0))
    names = font2.render('Emily Gaelic, Sunwoo Nam, Adriana Naughton',
                         True, (0, 0, 0))
    win.blit(yr, (430, 10))
    win.blit(names, (250, 40))
    start = font.render('Start', True, (255, 255, 255))
    win.blit(start, (425, 440))
    end = font.render('Exit', True, (0,0,0))
    config = font.render('Configure', True, (0,0,0))
    scores = font.render('Scores', True, (0,0,0))
    win.blit(end, (100, 600))
    win.blit(config, (360, 600))
    win.blit(scores, (750, 600))

    pygame.display.flip()

    go = True
    while go:
        mouse = pygame.mouse.get_pos()
        if 500 <= mouse[0] <= 550 and 500 <= mouse[1] <= 550:
            pygame.draw.rect(win, (200, 0, 0), [500, 350, 140, 40])
        else:
            pygame.draw.rect(win, (255, 0,0 ), [500, 350, 140, 40])
        for event in pygame.event.get():
            if event.type == pygame.quit:
                go = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 <= mouse[0] <= 550 and 500 <= mouse[1] <= 550:
                    go = False



    pygame.display.flip()


if __name__ == "__main__":
    main()
