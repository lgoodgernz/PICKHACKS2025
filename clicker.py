import pygame
import game_data  # Import shared money variable

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

money_img = pygame.image.load("OFFICE_DESK.png")
original_money_img = pygame.transform.scale(money_img, (100, 100))
pressed_money_img = pygame.transform.scale(money_img, (90, 90))
money_img = original_money_img

money_rect = money_img.get_rect(center=(WIDTH//2, HEIGHT//2))
exit_button = pygame.Rect(20, 450, 100, 30)

font = pygame.font.Font(None, 36)

def run_clicker():
    running = True
    while running:
        screen.fill(WHITE)

        screen.blit(money_img, money_rect.topleft)

        # Display money (now using game_data.money)
        text = font.render(f"Money: {game_data.money}", True, BLACK)
        screen.blit(text, (20, 20))

        # Draw Exit Button
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Exit", True, WHITE)
        screen.blit(exit_text, (30, 455))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)  # Save before quitting
                running = False  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if money_rect.collidepoint(event.pos):
                    game_data.money += 1  # Increase money globally
                elif exit_button.collidepoint(event.pos):
                    game_data.save_money(game_data.money)  # Save before exiting
                    running = False  # Exit back to menu

        pygame.display.flip()

    game_data.save_money(game_data.money)  # Ensure money is saved on exit

if __name__ == "__main__":
    run_clicker()
