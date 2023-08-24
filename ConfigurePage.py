import pygame
import sys


pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)


class ConfigurePage:
    def __init__(self):
        self.selected_size = "10*20"
        self.game_lines = 0
        self.selected_level = "Easy"
        self.game_mode = "Normal"
        self.player_mode = "Player"

        self.size_options = ["10x20", "10x24"]
        self.size_10x20_rect = pygame.Rect(50, 150, 200, 50)
        self.size_10x24_rect = pygame.Rect(300, 150, 200, 50)
        self.easy_mode_rect = pygame.Rect(50, 265, 200, 50)
        self.medium_mode_rect = pygame.Rect(300, 265, 200, 50)
        self.hard_mode_rect = pygame.Rect(550, 265, 200, 50)
        self.normal_mode_rect = pygame.Rect(50, 380, 200, 50)
        self.extended_mode_rect = pygame.Rect(300, 380, 200, 50)
        self.player_mode_rect = pygame.Rect(50, 520, 200, 50)
        self.ai_mode_rect = pygame.Rect(300, 520, 200, 50)
        self.close_button_rect = pygame.Rect(750, 650, 100, 30)
        self.back_button_rect = pygame.Rect(50, 650, 100, 30)

    def draw_configure_page(self, screen):
        screen.fill(WHITE)

        # Draw size buttons
        text = FONT.render("Field size:", True, pygame.Color('black'))
        screen.blit(text, (50, 110))
        size_10x20_text = FONT.render("10x20", True, pygame.Color('black'))
        size_10x24_text = FONT.render("10x24", True, pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color('gray'), self.size_10x20_rect)
        pygame.draw.rect(screen, pygame.Color('gray'), self.size_10x24_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.size_10x20_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.size_10x24_rect, 2)

        screen.blit(size_10x20_text, (self.size_10x20_rect.x + 20, self.size_10x20_rect.y + 15))
        screen.blit(size_10x24_text, (self.size_10x24_rect.x + 20, self.size_10x24_rect.y + 15))

        # Draw level buttons
        text = FONT.render("Game level:", True, pygame.Color('black'))
        screen.blit(text, (50, 230))

        pygame.draw.rect(screen, pygame.Color('gray'), self.easy_mode_rect)
        pygame.draw.rect(screen, pygame.Color('gray'), self.medium_mode_rect)
        pygame.draw.rect(screen, pygame.Color('gray'), self.hard_mode_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.easy_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.medium_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.hard_mode_rect, 2)

        easy_text = FONT.render("Easy", True, pygame.Color('black'))
        normal_text = FONT.render("Medium", True, pygame.Color('black'))
        hard_text = FONT.render("Hard", True, pygame.Color('black'))

        screen.blit(easy_text, (self.easy_mode_rect.x + 10, self.easy_mode_rect.y + 10))
        screen.blit(normal_text, (self.medium_mode_rect.x + 10, self.medium_mode_rect.y + 10))
        screen.blit(hard_text, (self.hard_mode_rect.x +10, self.hard_mode_rect.y + 10))

        #game mode (normal/extended)
        text = FONT.render("Game mode:", True, pygame.Color('black'))
        screen.blit(text, (50, 340))

        pygame.draw.rect(screen, pygame.Color('gray'), self.normal_mode_rect)
        pygame.draw.rect(screen, pygame.Color('gray'), self.extended_mode_rect)

        pygame.draw.rect(screen, pygame.Color('black'), self.normal_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.extended_mode_rect, 2)

        normal_text = FONT.render("Normal", True, pygame.Color('black'))
        extended_text = FONT.render("Extended", True, pygame.Color('black'))

        screen.blit(normal_text, (self.normal_mode_rect.x + 10, self.normal_mode_rect.y + 10))
        screen.blit(extended_text, (self.extended_mode_rect.x + 10, self.extended_mode_rect.y + 10))

        #player mode (Player/AI)
        text = FONT.render("Player mode:", True, pygame.Color('black'))
        screen.blit(text, (50, 470))

        pygame.draw.rect(screen, pygame.Color('gray'), self.player_mode_rect)
        pygame.draw.rect(screen, pygame.Color('gray'), self.ai_mode_rect)

        pygame.draw.rect(screen, pygame.Color('black'), self.player_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.ai_mode_rect, 2)

        player_text = FONT.render("Player", True, pygame.Color('black'))
        ai_text = FONT.render("AI", True, pygame.Color('black'))

        screen.blit(player_text, (self.player_mode_rect.x + 10, self.player_mode_rect.y + 10))
        screen.blit(ai_text, (self.ai_mode_rect.x + 10, self.ai_mode_rect.y + 10))

        # Draw close button
        pygame.draw.rect(screen, pygame.Color('black'), self.close_button_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.close_button_rect, 2)
        close_text = FONT.render("Close", True, pygame.Color('white'))
        screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y + 5))

        # back button
        pygame.draw.rect(screen, pygame.Color('black'), self.back_button_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.back_button_rect, 2)
        back_text = FONT.render("Back", True, pygame.Color('white'))
        screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def handle_mouse_click(self, screen, mouse_pos,loop):
        if self.size_10x20_rect.collidepoint(mouse_pos):
            self.selected_size = "10x20"
        elif self.size_10x24_rect.collidepoint(mouse_pos):
            self.selected_size = "10x24"
        elif self.easy_mode_rect.collidepoint(mouse_pos):
            self.selected_level = "Easy"
        elif self.medium_mode_rect.collidepoint(mouse_pos):
            self.selected_level = "Medium"
        elif self.hard_mode_rect.collidepoint(mouse_pos):
            self.selected_level = "Hard"
        elif self.normal_mode_rect.collidepoint(mouse_pos):
            self.game_mode = "Normal"
        elif self.extended_mode_rect.collidepoint(mouse_pos):
            self.game_mode = "Extended"
        elif self.player_mode_rect.collidepoint(mouse_pos):
            self.player_mode = "Player"
        elif self.ai_mode_rect.collidepoint(mouse_pos):
            self.player_mode = "AI"
        elif self.close_button_rect.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()
        elif self.back_button_rect.collidepoint(mouse_pos):
            loop = False
            screen.fill((255, 255, 255))
            from StartupPage import StartupPage
            startup_page = StartupPage()
            startup_page.draw_startup_page(screen)





