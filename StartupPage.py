import pygame
import sys
import random
from GamePage import PlayGame

pygame.init()

class StartupPage:

    font = pygame.font.SysFont('Courier', 50, 'bold')

    def __init__(self):
        self.start = pygame.Rect(425, 440, 153, 50)
        self.scores = pygame.Rect(50, 600, 183, 50)
        self.configure = pygame.Rect(360, 600, 275, 50)
        self.exit = pygame.Rect(800, 600, 125, 50)
        
        # user game configurations
        self.game_extension = False
        self.AI = False
        self.game_level = 1
        # game board size 
        self.board_length = 10
        self.board_height = 20

    def draw_startup_page(self, start_page):
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
        start_page.blit(pic, pic.get_rect(center=start_page.get_rect().center))
        start_page.blit(yr, (430, 10))
        start_page.blit(names, (250, 40))
        pygame.draw.rect(start_page, (255, 0, 0), self.exit)
        pygame.draw.rect(start_page, (255, 165, 0), self.configure)
        pygame.draw.rect(start_page, (0, 255, 0), self.start)
        pygame.draw.rect(start_page, (255, 255, 0), self.scores)
        start_page.blit(text1, (self.start.x, self.start.y))
        start_page.blit(text2, (self.exit.x, self.exit.y))
        start_page.blit(text3, (self.scores.x, self.scores.y))
        start_page.blit(text4, (self.configure.x, self.configure.y))

    def handle_mouse_click(self, start_page, mouse_pos):
        pygame.display.set_caption('Tetris 44')
        if self.exit.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()
        elif self.start.collidepoint(mouse_pos):    # GAME PLAY
            clock = pygame.time.Clock()  # start clock
            pygame.time.set_timer(pygame.USEREVENT, 300)
            run = True  # run game variable
            game = PlayGame(self.board_length, self.board_height, self.game_extension, self.AI, self.game_level)
            rotate_sound = pygame.mixer.Sound("can_rotate.wav")
            while run:

                # DISPLAY - fill screen with grid and surfaces
                start_page.fill((0, 0, 0))  # black background
                game.draw_game(start_page)

                # PLAYER ACTIONS
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # user quits
                        if (game.quit_game()):
                            run = False
                            sys.exit()
                        else:
                            continue

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # quits with escape key
                            if (game.quit_game()):
                                start_page.fill((255, 255, 255))
                                from StartupPage import StartupPage
                                startup_page = StartupPage()
                                startup_page.draw_startup_page(start_page)
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse = pygame.mouse.get_pos()
                                            startup_page.handle_mouse_click(start_page, mouse)
                                    pygame.display.flip()
                            else:
                                print("continue")
                                continue

                        if event.key == pygame.K_RIGHT:  # move right
                            game.move_block(True)
                        if event.key == pygame.K_LEFT:  # move left
                            game.move_block(False)
                        if event.key == pygame.K_UP:  # rotate
                            game.rotate()
                            rotate_sound.play()
                        if event.key == pygame.K_DOWN:  # move down
                            game.block_falls()

                    if event.type == pygame.USEREVENT:
                        game.block_falls()

                if game.game_over == True:
                    run = False

                pygame.display.update()
                clock.tick(30)

        elif self.configure.collidepoint(mouse_pos):

            from ConfigurePage import ConfigurePage
            configure_page = ConfigurePage()
            start_page.fill((255, 255, 255))
            pygame.display.set_caption("Tetris Setting")
            configure_page.draw_configure_page(start_page)
            pygame.mixer.music.load("background.wav")
            pygame.mixer.music.play(-1)
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        configure_page.handle_mouse_click(start_page, mouse_pos)

                pygame.display.flip()
                clock = pygame.time.Clock()
                clock.tick(30)

        elif self.scores.collidepoint(mouse_pos):
            from TopscorePage import HighscorePage
            pygame.display.set_caption('Top Scores')

            # Generate random player scores
            player_scores = [(f'Player {i}', random.randint(15000, 25000)) for i in range(1, 11)]

            # Score range between 15000-25000
            player_scores[0] = ('Player 1', 25000)
            player_scores[-1] = ('Player 10', 15000)

            # sort scores in desc order
            player_scores.sort(key=lambda x: x[1], reverse=True)

            HighscorePage.show_top_scores(player_scores, start_page)
