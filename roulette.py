import pygame
import random
import game_data

# European Roulette Number Layout
roulette_numbers = {
    "RED": {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36},
    "BLACK": {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35},
    "GREEN": {0}
}

def get_winning_color(number):
    """Returns the color of the landed number"""
    for color, numbers in roulette_numbers.items():
        if number in numbers:
            return color
    return "GREEN"

def roulette_game(SCREEN):
    WIDTH, HEIGHT = 1479, 778
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)

    font = pygame.font.Font(None, 36)

    # Load Background and Table Images
    bg_img = pygame.image.load("roulette_BG.png")
    bg_img = pygame.transform.scale(bg_img, (778, 778))

    table_img = pygame.image.load("roulette_table.png")
    table_img = pygame.transform.scale(table_img, (1486, 1486))

    colors = ["RED", "GREEN", "BLACK"]
    chosen_color_index = 0
    bet_amount = 10
    result_text = ""

    spinning = False
    angle = 0
    spin_speed = 30
    winning_number = None

    running = True
    while running:
        SCREEN.fill(BLACK)

        # Draw Background at (351, 0)
        SCREEN.blit(bg_img, (351, 0))

        # Spin Animation
        if spinning:
            angle += spin_speed
            spin_speed *= 0.98  # Slow down gradually

            if spin_speed < 0.5:  # Stop spinning
                spinning = False
                winning_number = random.randint(0, 36)  # Pick a number 0-36
                spin_result = get_winning_color(winning_number)  # Get actual color

                if spin_result == chosen_color:
                    winnings = bet_amount * (14 if chosen_color == "GREEN" else 2)
                    game_data.money += winnings
                    result_text = f"You won! +${winnings} (Number: {winning_number})"
                else:
                    result_text = f"You lost! (Number: {winning_number})"

        # Rotate and Draw Roulette Table, keeping position stable
        rotated_table = pygame.transform.rotate(table_img, angle)
        table_rect = rotated_table.get_rect(center=(743, 349))  # Keeps (0, -394) stable
        SCREEN.blit(rotated_table, table_rect.topleft)

        # Display Money and Bet
        money_text = font.render(f"Money: {game_data.money}", True, WHITE)
        SCREEN.blit(money_text, (20, 20))

        bet_text = font.render(f"Bet: ${bet_amount}", True, WHITE)
        SCREEN.blit(bet_text, (20, 60))

        chosen_color = colors[chosen_color_index]
        color_text = font.render(
            f"Chosen Color: {chosen_color}",
            True, RED if chosen_color == "RED" else (GREEN if chosen_color == "GREEN" else WHITE)
        )
        SCREEN.blit(color_text, (20, 100))

        # Draw a black rectangle behind the result message with increased width
        result_rect = pygame.Rect(WIDTH // 2 - 175, HEIGHT - 120, 350, 40)  # Increase width to 350
        pygame.draw.rect(SCREEN, WHITE, result_rect, 4)  # White border outline
        pygame.draw.rect(SCREEN, BLACK, result_rect)  # Black background

        # Display Result on top of the black rectangle
        result_display = font.render(result_text, True, GREEN if "won" in result_text else RED)
        SCREEN.blit(result_display, (WIDTH // 2 - 165, HEIGHT - 110))

        # Draw Exit Button in the top-right corner (Red button)
        exit_button = pygame.Rect(WIDTH - 150, 20, 120, 40)  # Position (top-right corner)
        pygame.draw.rect(SCREEN, RED, exit_button)  # Red color for the button
        exit_text = font.render("Exit", True, WHITE)  # White text on red button
        SCREEN.blit(exit_text, (WIDTH - 140, 25))  # Position of the "Exit" text

        pygame.display.flip()

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return

                if not spinning:
                    if event.key == pygame.K_UP and bet_amount + 5 <= game_data.money:
                        bet_amount += 5
                    elif event.key == pygame.K_DOWN and bet_amount - 5 >= 5:
                        bet_amount -= 5
                    elif event.key == pygame.K_LEFT:
                        chosen_color_index = (chosen_color_index - 1) % len(colors)
                    elif event.key == pygame.K_RIGHT:
                        chosen_color_index = (chosen_color_index + 1) % len(colors)

                if event.key == pygame.K_SPACE and not spinning:
                    if bet_amount > game_data.money:
                        result_text = "Not enough money!"
                    else:
                        game_data.money -= bet_amount
                        spinning = True
                        spin_speed = 30

            # Handle Mouse Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button.collidepoint(mouse_pos):
                    game_data.save_money(game_data.money)
                    return  # Exit to main menu
