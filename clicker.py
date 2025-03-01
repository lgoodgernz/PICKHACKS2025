import pygame

pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load button image
money_img = pygame.image.load("OFFICE_DESK.png")
original_money_img = pygame.transform.scale(money_img, (100, 100))
pressed_money_img = pygame.transform.scale(money_img, (90, 90))
money_img = original_money_img

money_rect = money_img.get_rect(center=(WIDTH//2, HEIGHT//2))

# Exit button
exit_button = pygame.Rect(20, 450, 100, 30)

# Font setup
font = pygame.font.Font(None, 36)

# Money counter (global)
money = 0
button_pressed = False

def run_clicker():
    global money, money_img
    running = True
    while running:
        screen.fill(WHITE)

        screen.blit(money_img, money_rect.topleft)

        # Render text
        text = font.render(f"Money: {money}", True, BLACK)
        screen.blit(text, (20, 20))

        # Draw exit button
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Exit", True, WHITE)
        screen.blit(exit_text, (30, 455))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if money_rect.collidepoint(event.pos):
                    money += 1
                    money_img = pressed_money_img
                    button_pressed = True
                elif exit_button.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_pressed:
                    money_img = original_money_img
                    button_pressed = False

        pygame.display.flip()

if __name__ == "__main__":
    run_clicker()
