import pygame
import random


def show_top_scores(scores, screen):
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont('Courier', 50, 'bold')
    title_text = font.render('HIGHSCORES', True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)

    font = pygame.font.SysFont('Courier', 30)

    # Top 10 scores
    for i, (name, score) in enumerate(scores, start=1):
        score_text = font.render(f'{name}: {score}', True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 120 + i * 40))
        screen.blit(score_text, score_rect)

    close_button_rect = pygame.Rect(400, 600, 200, 40)
    pygame.draw.rect(screen, (200, 0, 0), close_button_rect)
    close_button_text = font.render('Close', True, (255, 255, 255))
    close_text_rect = close_button_text.get_rect(center=close_button_rect.center)

    screen.blit(close_button_text, close_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if close_button_rect.collidepoint(mouse_pos):
                    return


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Top Scores')

    # Generate random player scores
    player_scores = [(f'Player {i}', random.randint(15000, 25000)) for i in range(1, 11)]

    # Score range between 15000-25000
    player_scores[0] = ('Player 1', 25000)
    player_scores[-1] = ('Player 10', 15000)

    # sort scores in desc order
    player_scores.sort(key=lambda x: x[1], reverse=True)

    show_top_scores(player_scores, screen)

    pygame.quit()


if __name__ == "__main__":
    main()
