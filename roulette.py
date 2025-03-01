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
    return "GREEN"  # Should never reach this

def roulette_game(SCREEN):
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)

    font = pygame.font.Font(None, 36)

    # Load Roulette Wheel Image
    wheel_img = pygame.image.load("wheel.png")
    wheel_img = pygame.transform.scale(wheel_img, (300, 300))
    wheel_rect = wheel_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

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
        SCREEN.fill(WHITE)

        # Display Money and Bet
        money_text = font.render(f"Money: {game_data.money}", True, BLACK)
        SCREEN.blit(money_text, (20, 20))

        bet_text = font.render(f"Bet: ${bet_amount}", True, BLACK)
        SCREEN.blit(bet_text, (20, 60))

        chosen_color = colors[chosen_color_index]
        color_text = font.render(f"Chosen Color: {chosen_color}", True, RED if chosen_color == "RED" else (GREEN if chosen_color == "GREEN" else BLACK))
        SCREEN.blit(color_text, (20, 100))

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

        # Rotate and Draw the Wheel
        rotated_wheel = pygame.transform.rotate(wheel_img, angle)
        new_rect = rotated_wheel.get_rect(center=wheel_rect.center)
        SCREEN.blit(rotated_wheel, new_rect.topleft)

        # Display Result
        result_display = font.render(result_text, True, GREEN if "won" in result_text else RED)
        SCREEN.blit(result_display, (WIDTH // 2 - 150, HEIGHT - 100))

        pygame.display.flip()

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return  # Exit back to menu

                if not spinning:  # Allow arrow keys only if not spinning
                    if event.key == pygame.K_UP and bet_amount + 5 <= game_data.money:
                        bet_amount += 5
                    elif event.key == pygame.K_DOWN and bet_amount - 5 >= 5:
                        bet_amount -= 5
                    elif event.key == pygame.K_LEFT:
                        chosen_color_index = (chosen_color_index - 1) % len(colors)  # Cycle left
                    elif event.key == pygame.K_RIGHT:
                        chosen_color_index = (chosen_color_index + 1) % len(colors)  # Cycle right

                if event.key == pygame.K_SPACE and not spinning:
                    if bet_amount > game_data.money:
                        result_text = "Not enough money!"
                    else:
                        game_data.money -= bet_amount
                        spinning = True
                        spin_speed = 30  # Reset speed for new spin
