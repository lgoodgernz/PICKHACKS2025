import pygame

def help_page(SCREEN):
    pygame.display.flip()
    screen_width, screen_height = SCREEN.get_size()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 50)

    exit_button = pygame.Rect(20, screen_height - 50, 100, 30)

    running = True
    while running:
        SCREEN.fill(BLACK)

        SCREEN.blit(title_font.render("Casino Game Help Page", True, WHITE), (screen_width // 2 - 200, 20))
        SCREEN.blit(font.render("- Click on desks to select a game", True, WHITE), (50, 100))
        SCREEN.blit(font.render("- Go to work! Click to earn money under the get money sign", True, WHITE), (50, 140))
        SCREEN.blit(font.render("- Roulette: Bet on a colour", True, WHITE), (50, 180))
        SCREEN.blit(font.render("- Horse Racing: Bet on a horse to win", True, WHITE), (50, 220))
        SCREEN.blit(font.render("- NBA Betting: Place bets on matchups", True, WHITE), (50, 260))
        SCREEN.blit(font.render("- Spinner: Spin the wheel and guess higher or lower", True, WHITE), (50, 300))
        SCREEN.blit(font.render("- Blackjack: Try to hit 21", True, WHITE), (50, 340))
        SCREEN.blit(font.render("- Mouse Click: Select options", True, WHITE), (50, 380))
        SCREEN.blit(font.render("- ESC: Exit to main menu", True, WHITE), (50, 420))

        pygame.draw.rect(SCREEN, RED, exit_button)
        SCREEN.blit(font.render("Exit", True, WHITE), (30, screen_height - 45))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()# Write your code here :-)
