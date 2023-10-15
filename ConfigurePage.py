from GamePage import PlayGame
import pygame
import sys
from StartupPage import StartupPage
        

pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SELECTED_COLOR = (173, 216, 239)  # Light Blue
DEFAULT_COLOR = (255, 255, 255)  # White
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)


class ConfigurePage:
    def __init__(self):
        self.gameConfig = StartupPage()

        self.size_5x20_rect = pygame.Rect(50, 150, 200, 50)
        self.size_10x20_rect = pygame.Rect(300, 150, 200, 50)
        self.size_15x20_rect = pygame.Rect(550, 150, 200, 50)
        self.easy_mode_rect = pygame.Rect(50, 265, 200, 50)
        self.medium_mode_rect = pygame.Rect(300, 265, 200, 50)
        self.hard_mode_rect = pygame.Rect(550, 265, 200, 50)
        self.normal_mode_rect = pygame.Rect(50, 380, 200, 50)
        self.extended_mode_rect = pygame.Rect(300, 380, 200, 50)
        self.player_mode_rect = pygame.Rect(50, 520, 200, 50)
        self.ai_mode_rect = pygame.Rect(300, 520, 200, 50)
        self.close_button_rect = pygame.Rect(750, 650, 100, 30)
        self.back_button_rect = pygame.Rect(50, 650, 100, 30)
        self.play_game = None


    def draw_configure_page(self, screen):
        screen.fill(WHITE)

        # Determine button colors based on user selections
        size_5x20_color = SELECTED_COLOR if self.gameConfig.boardSize == 5 else pygame.Color('gray')
        size_10x20_color = SELECTED_COLOR if self.gameConfig.boardSize == 10 else pygame.Color('gray')
        size_15x20_color = SELECTED_COLOR if self.gameConfig.boardSize == 15 else pygame.Color('gray')
        easy_mode_color = SELECTED_COLOR if self.gameConfig.gameLevel == 1 else pygame.Color('gray')
        medium_mode_color = SELECTED_COLOR if self.gameConfig.gameLevel == 2 else pygame.Color('gray')
        hard_mode_color = SELECTED_COLOR if self.gameConfig.gameLevel == 3 else pygame.Color('gray')
        normal_mode_color = SELECTED_COLOR if self.gameConfig.gameExtension == False else pygame.Color('gray')
        extended_mode_color = SELECTED_COLOR if self.gameConfig.gameExtension == True else pygame.Color('gray')
        player_mode_color = SELECTED_COLOR if self.gameConfig.AiMode == False else pygame.Color('gray')
        ai_mode_color = SELECTED_COLOR if self.gameConfig.AiMode == True else pygame.Color('gray')

        # Draw size buttons
        text = FONT.render("Field size:", True, pygame.Color('black'))
        screen.blit(text, (50, 110))
        size_5x20_text = FONT.render("5x20", True, pygame.Color('black'))
        size_10x20_text = FONT.render("10x20", True, pygame.Color('black'))
        size_15x20_text = FONT.render("15x20", True, pygame.Color('black'))
        pygame.draw.rect(screen, size_5x20_color, self.size_5x20_rect)
        pygame.draw.rect(screen, size_10x20_color, self.size_10x20_rect)
        pygame.draw.rect(screen, size_15x20_color, self.size_15x20_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.size_5x20_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.size_10x20_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.size_15x20_rect, 2)

        screen.blit(size_5x20_text, (self.size_5x20_rect.x + 20, self.size_5x20_rect.y + 15))
        screen.blit(size_10x20_text, (self.size_10x20_rect.x + 20, self.size_10x20_rect.y + 15))
        screen.blit(size_15x20_text, (self.size_15x20_rect.x + 20, self.size_15x20_rect.y + 15))

        # Draw level buttons
        text = FONT.render("Game level:", True, pygame.Color('black'))
        screen.blit(text, (50, 230))

        pygame.draw.rect(screen, easy_mode_color, self.easy_mode_rect)
        pygame.draw.rect(screen, medium_mode_color, self.medium_mode_rect)
        pygame.draw.rect(screen, hard_mode_color, self.hard_mode_rect)

        easy_text = FONT.render("Easy", True, pygame.Color('black'))
        medium_text = FONT.render("Medium", True, pygame.Color('black'))
        hard_text = FONT.render("Hard", True, pygame.Color('black'))

        screen.blit(easy_text, (self.easy_mode_rect.x + 10, self.easy_mode_rect.y + 10))
        screen.blit(medium_text, (self.medium_mode_rect.x + 10, self.medium_mode_rect.y + 10))
        screen.blit(hard_text, (self.hard_mode_rect.x + 10, self.hard_mode_rect.y + 10))

        pygame.draw.rect(screen, pygame.Color('black'), self.easy_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.medium_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.hard_mode_rect, 2)

        # Drawing the Game Mode buttons
        text = FONT.render("Game mode:", True, pygame.Color('black'))
        screen.blit(text, (50, 345))
        pygame.draw.rect(screen, normal_mode_color, self.normal_mode_rect)
        pygame.draw.rect(screen, extended_mode_color, self.extended_mode_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.normal_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.extended_mode_rect, 2)

        normal_text = FONT.render("Normal", True, pygame.Color('black'))
        extended_text = FONT.render("Extended", True, pygame.Color('black'))

        screen.blit(normal_text, (self.normal_mode_rect.x + 10, self.normal_mode_rect.y + 10))
        screen.blit(extended_text, (self.extended_mode_rect.x + 10, self.extended_mode_rect.y + 10))

        # Drawing the Player Mode buttons
        pygame.draw.rect(screen, player_mode_color, self.player_mode_rect)
        pygame.draw.rect(screen, ai_mode_color, self.ai_mode_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.player_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.ai_mode_rect, 2)

        player_text = FONT.render("Player", True, pygame.Color('black'))
        ai_text = FONT.render("AI", True, pygame.Color('black'))

        screen.blit(player_text, (self.player_mode_rect.x + 10, self.player_mode_rect.y + 10))
        screen.blit(ai_text, (self.ai_mode_rect.x + 10, self.ai_mode_rect.y + 10))

        #player mode label
        text = FONT.render("Player mode:", True, pygame.Color('black'))
        screen.blit(text, (50, 470))

        # Draw back button on the left side
        pygame.draw.rect(screen, pygame.Color('black'), self.back_button_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.back_button_rect, 2)
        back_text = FONT.render("Back", True, pygame.Color('white'))
        screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

        # Calculate the position of the close button on the right side
        close_button_x = SCREEN_WIDTH - self.close_button_rect.width - 50

        # Draw close button on the right side
        close_button_rect = pygame.Rect(close_button_x, self.close_button_rect.y, self.close_button_rect.width,
                                        self.close_button_rect.height)
        pygame.draw.rect(screen, pygame.Color('black'), close_button_rect)
        pygame.draw.rect(screen, pygame.Color('black'), close_button_rect, 2)
        close_text = FONT.render("Close", True, pygame.Color('white'))
        screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y + 5))

        # Draw the Start button
        start_button_x = (SCREEN_WIDTH - 100) // 2  # Centered between Back and Close
        self.start_button_rect = pygame.Rect(start_button_x, 650, 100, 30)
        pygame.draw.rect(screen, pygame.Color('black'), self.start_button_rect)
        start_text = FONT.render("Start", True, pygame.Color('white'))
        screen.blit(start_text, (self.start_button_rect.x + 20, self.start_button_rect.y + 5))

    def HandleMouseClick(self, startPage, mouse_pos):
        # Handle board size buttons
        if self.size_10x20_rect.collidepoint(mouse_pos):
            self.gameConfig.boardSize = self.getField("10x20")

        elif self.size_5x20_rect.collidepoint(mouse_pos):
            self.gameConfig.boardSize = self.getField("5x20")

        elif self.size_15x20_rect.collidepoint(mouse_pos):
            self.gameConfig.boardSize = self.getField("15x20")

        # Handle game level buttons
        elif self.easy_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.gameLevel = self.getLevel("Easy")

        elif self.medium_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.gameLevel = self.getLevel("Medium")

        elif self.hard_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.gameLevel = self.getLevel("Hard")

        # Handle game mode buttons
        elif self.normal_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.gameExtension = False
        
        elif self.extended_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.gameExtension = True

        # Handle player mode buttons
        elif self.player_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.AiMode = False
        
        elif self.ai_mode_rect.collidepoint(mouse_pos):
            self.gameConfig.AiMode = True

        # Handle system buttons
        elif self.close_button_rect.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()
        
        elif self.start_button_rect.collidepoint(mouse_pos):
            if self.gameConfig.AiMode:  # AI Playing
                self.gameConfig.AIPlaying(startPage)
           
            else:  # User Playing
                self.gameConfig.UserPlaying(startPage)

        elif self.back_button_rect.collidepoint(mouse_pos):
            startPage.fill(WHITE)
            return False
        
        return True


    def getField(self, selectedSize):
        if selectedSize == "5x20":
            return 5
        elif selectedSize == "10x20":
            return 10
        elif selectedSize == "15x20":
            return 15

    def getLevel(self, selectedLevel):
        if selectedLevel == "Easy":
            return 1
        elif selectedLevel == "Medium":
            return 2
        elif selectedLevel == "Hard":
            return 3
