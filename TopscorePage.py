import sys
import pygame
import random

class HighscorePage:

    def __init__(self):
        self.font_large = pygame.font.SysFont('Courier', 50, 'bold')
        self.font = pygame.font.SysFont('Courier', 30)

    def showTopScores(self, screen, startup_instance):
        # Fetch scores from the PlayGame's method
        scores = startup_instance.GetScores()

        # If there are fewer than 10 scores, fill the rest with random values
        while len(scores) < 10:
            random_name = self._get_random_name()
            random_score = self._get_random_score()
            scores.append((random_name, random_score))

        # Sort the scores in descending order
        scores.sort(key=lambda x: x[1], reverse=True)

        screen.fill((255, 255, 255))

        # Display the title
        self._display_text(screen, 'HIGHSCORES', self.font_large, (screen.get_width() // 2, 50))

        # Display the scores
        for i, (name, score) in enumerate(scores[:10], start=1):
            self._display_text(screen, f'{i}. {name}: {score}', self.font, (screen.get_width() // 2, 120 + i * 40))

        # Buttons
        button_width, button_height = 200, 40
        button_spacing = 20
        total_button_width = 2 * button_width + button_spacing

        back_button_rect = self._draw_button(screen, 'Back', (screen.get_width() - total_button_width) // 2, 600, button_width, button_height)
        close_button_rect = self._draw_button(screen, 'Close', back_button_rect.right + button_spacing, 600, button_width, button_height)

        pygame.display.flip()

        self._handle_events(screen, back_button_rect, close_button_rect, startup_instance)

    def _display_text(self, screen, text, font, position):
        rendered_text = font.render(text, True, (0, 0, 0))
        text_rect = rendered_text.get_rect(center=position)
        screen.blit(rendered_text, text_rect)

    def _draw_button(self, screen, text, x, y, width, height):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (200, 0, 0), button_rect)
        self._display_text(screen, text, self.font, button_rect.center)
        return button_rect

    def _handle_events(self, screen, back_button_rect, close_button_rect, startup_instance):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        screen.fill((255, 255, 255))
                        startup_instance.DrawStartupPage(screen)
                        return
                    elif close_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def _get_random_name(self):
        # You can customize this list with real names
        names = ["Sarah", "Linda", "John", "Adriana", "Emily", "Sunwoo", "Amy", "James", "Susan", "Robert"]
        return random.choice(names)

    def _get_random_score(self):
        # Generate random score based on the specified rule
        lines_cleared = random.randint(10, 50)
        return lines_cleared * 100
