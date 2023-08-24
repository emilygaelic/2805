import pygame
import sys
import random


pygame.init()


class StartupPage:

    font = pygame.font.SysFont('Courier', 50, 'bold')

    def __init__(self):
        self.start = 'Start'
        self.scores = 'Scores'
        self.configure = 'Configure'
        self.exit = 'Exit'

        self.start = pygame.Rect(425, 440, 153, 50)
        self.scores = pygame.Rect(50, 600, 183, 50)
        self.configure = pygame.Rect(360, 600, 275, 50)
        self.exit = pygame.Rect(800, 600, 125, 50)

    def draw_startup_page(self, win):
        pygame.display.set_caption('Welcome')
        pic = pygame.image.load('TetrisLogo.png')
        font = pygame.font.SysFont('Courier', 50, 'bold')
        font2 = pygame.font.SysFont('Courier', 20)
        yr = font2.render('2023, 2805ICT', True, (0, 0, 0))
        names = font2.render('Emily Gaelic, Sunwoo Nam, Adriana Naughton',
                             True, (0, 0, 0))
        text1 = font.render('Start', True, (0, 0, 0))
        text2 = font.render('Exit', True, (0, 0, 0))
        text3 = font.render('Scores', True, (0, 0, 0))
        text4 = font.render('Configure', True, (0, 0, 0))
        win.blit(pic, pic.get_rect(center=win.get_rect().center))
        win.blit(yr, (430, 10))
        win.blit(names, (250, 40))
        pygame.draw.rect(win, (255, 0, 0), self.exit)
        pygame.draw.rect(win, (255, 165, 0), self.configure)
        pygame.draw.rect(win, (0, 255, 0), self.start)
        pygame.draw.rect(win, (255, 255, 0), self.scores)
        win.blit(text1, (self.start.x, self.start.y))
        win.blit(text2, (self.exit.x, self.exit.y))
        win.blit(text3, (self.scores.x, self.scores.y))
        win.blit(text4, (self.configure.x, self.configure.y))

    def handle_mouse_click(self, win, mouse_pos):
        if self.exit.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()
        elif self.start.collidepoint(mouse_pos):
            self.start = "start"
        elif self.configure.collidepoint(mouse_pos):
            from ConfigurePage import ConfigurePage
            configure_page = ConfigurePage()
            win.fill((255, 255, 255))
            pygame.display.set_caption("Tetris Setting")
            configure_page.draw_configure_page(win)
            pygame.mixer.music.load("background.wav")
            pygame.mixer.music.play(-1)
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        configure_page.handle_mouse_click(win, mouse_pos)

                pygame.display.flip()
                clock = pygame.time.Clock()
                clock.tick(30)

        elif self.scores.collidepoint(mouse_pos):
            from TopscorePage import show_top_scores
            pygame.display.set_caption('Top Scores')

            # Generate random player scores
            player_scores = [(f'Player {i}', random.randint(15000, 25000)) for i in range(1, 11)]

            # Score range between 15000-25000
            player_scores[0] = ('Player 1', 25000)
            player_scores[-1] = ('Player 10', 15000)

            # sort scores in desc order
            player_scores.sort(key=lambda x: x[1], reverse=True)

            show_top_scores(player_scores, win)
