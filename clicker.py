import pygame
import game_data  # Import shared money variable

def clicker_game(SCREEN):
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    font = pygame.font.Font(None, 36)

    # Load OFFICE_DESK image
    desk_img = pygame.image.load("OFFICE_DESK.png")
    original_desk_img = pygame.transform.scale(desk_img, (150, 150))  # Default size
    clicked_desk_img = pygame.transform.scale(desk_img, (130, 130))  # Click effect
    desk_img = original_desk_img

    desk_rect = desk_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centered
    exit_button = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)  # Move to bottom-right

    running = True
    clicked = False  # Track click state

    while running:
        SCREEN.fill(WHITE)

        # Display money
        text = font.render(f"Money: {game_data.money}", True, BLACK)
        SCREEN.blit(text, (20, 20))

        # Draw Clickable Money Button (OFFICE_DESK)
        SCREEN.blit(desk_img, desk_rect.topleft)

        # Draw Exit Button
        pygame.draw.rect(SCREEN, RED, exit_button)
        exit_text = font.render("Exit", True, WHITE)
        SCREEN.blit(exit_text, (exit_button.x + 20, exit_button.y + 10))

        pygame.display.flip()  # Ensure everything is updated before checking events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)  # Save before quitting
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse Clicked at: {event.pos}")  # Debugging
                if exit_button.collidepoint(event.pos):
                    print("Exit button clicked!")  # Debugging
                    game_data.save_money(game_data.money)  # Save before exiting
                    return  # Exit back to menu
                elif desk_rect.collidepoint(event.pos):
                    game_data.money += 1  # Increase money
                    desk_img = clicked_desk_img  # Shrink image for click effect
                    clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and clicked:
                desk_img = original_desk_img  # Reset image after clicking
                clicked = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("ESC pressed, returning to menu.")  # Debugging
                game_data.save_money(game_data.money)  # Save before exiting
                return  # Exit back to main menu
