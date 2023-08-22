import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)


class ConfigurePage:
    def __init__(self):
        self.selected_size = "Small"
        self.game_lines = 0
        self.game_level = 5
        self.game_mode = "Normal"
        self.player_mode = "Player"

        self.size_options = ["Small", "Medium", "Large"]
        self.size_dropdown_rect = pygame.Rect(50, 150, 300, 50)
        self.normal_mode_rect = pygame.Rect(50, 450, 200, 50)
        self.extended_mode_rect = pygame.Rect(300, 450, 200, 50)
        self.player_mode_rect = pygame.Rect(50, 600, 200, 50)
        self.ai_mode_rect = pygame.Rect(300, 600, 200, 50)
        self.close_button_rect = pygame.Rect(800, 650, 150, 30)  # Close button

    def draw_configure_page(self, screen):
        screen.fill(WHITE)

        text = FONT.render("Size of the field:", True, pygame.Color('black'))
        screen.blit(text, (50, 100))

        pygame.draw.rect(screen, pygame.Color('gray'), self.size_dropdown_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.size_dropdown_rect, 2)

        size_text = FONT.render(self.selected_size, True, pygame.Color('black'))
        screen.blit(size_text, (self.size_dropdown_rect.x + 10, self.size_dropdown_rect.y + 10))

        text = FONT.render("Game level:", True, pygame.Color('black'))
        screen.blit(text, (50, 400))

        # Draw the game level bar
        level_bar_width = 400
        level_bar_fill_width = int((self.game_lines - (self.game_level - 5) * 10) / 10 * (level_bar_width / 10))
        level_bar_rect = pygame.Rect(50, 450, level_bar_width, 20)
        level_bar_fill_rect = pygame.Rect(50, 450, level_bar_fill_width, 20)

        pygame.draw.rect(screen, pygame.Color('gray'), level_bar_rect)
        pygame.draw.rect(screen, pygame.Color('black'), level_bar_rect, 2)
        pygame.draw.rect(screen, pygame.Color('blue'), level_bar_fill_rect)

        text = FONT.render("Player mode:", True, pygame.Color('black'))
        screen.blit(text, (50, 550))

        pygame.draw.rect(screen, pygame.Color('gray'), self.player_mode_rect)
        pygame.draw.rect(screen, pygame.Color('gray'), self.ai_mode_rect)

        pygame.draw.rect(screen, pygame.Color('black'), self.player_mode_rect, 2)
        pygame.draw.rect(screen, pygame.Color('black'), self.ai_mode_rect, 2)

        player_text = FONT.render("Player", True, pygame.Color('black'))
        ai_text = FONT.render("AI", True, pygame.Color('black'))

        screen.blit(player_text, (self.player_mode_rect.x + 10, self.player_mode_rect.y + 10))
        screen.blit(ai_text, (self.ai_mode_rect.x + 10, self.ai_mode_rect.y + 10))

        # Draw close button
        pygame.draw.rect(screen, pygame.Color('gray'), self.close_button_rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.close_button_rect, 2)
        close_text = FONT.render("Close", True, pygame.Color('black'))
        screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y + 5))

    def handle_mouse_click(self, mouse_pos):
        if self.size_dropdown_rect.collidepoint(mouse_pos):
            selected_size_index = (self.size_options.index(self.selected_size) + 1) % len(self.size_options)
            self.selected_size = self.size_options[selected_size_index]
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


def main():
    # Create the startup screen
    startup_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris Startup")
    configure_page = ConfigurePage()
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                configure_page.handle_mouse_click(mouse_pos)

        configure_page.draw_configure_page(startup_screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
