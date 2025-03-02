import pygame
import random
import math
import game_data

def spinner_game(SCREEN):
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    COLORS = [(255, 108, 190), (0, 255, 0), (0, 0, 255),
              (255, 255, 0), (255, 165, 0), (128, 0, 128)]

    # Font
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 50)

    # Spinner variables
    center = (WIDTH // 2, HEIGHT // 2)
    radius = 200
    angle = 0
    spinning = False
    spin_speed = 0

    # Betting variables
    bet_amount = 5
    first_number = None
    second_number = None
    bet_choice = None  # "HIGHER" or "LOWER"
    result_text = ""
    has_bet = False  # Flag to track if player has placed a bet

    # Section labels
    labels = ["1", "2", "3", "4", "5", "6"]

    # Frame rate control
    clock = pygame.time.Clock()

    running = True
    while running:
        SCREEN.fill(WHITE)

        # Title
        title_text = title_font.render("Higher or Lower Spinner", True, BLACK)
        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        # Display Money and Bet
        money_text = font.render(f"Money: ${game_data.money}", True, BLACK)
        SCREEN.blit(money_text, (20, 20))

        bet_text = font.render(f"Bet: ${bet_amount}", True, BLACK)
        SCREEN.blit(bet_text, (20, 60))

        # Display current bet choice if made
        if bet_choice:
            choice_text = font.render(f"Betting: {bet_choice}", True, BLUE if bet_choice == "LOWER" else GREEN)
            SCREEN.blit(choice_text, (20, 100))

        # Spinner
        pygame.draw.circle(SCREEN, BLACK, center, radius, 3)

        for i in range(6):
            section_angle = math.radians(i * 60)
            x = center[0] + radius * math.cos(section_angle)
            y = center[1] + radius * math.sin(section_angle)
            pygame.draw.line(SCREEN, BLACK, center, (x, y), 2)

            # Fill sections
            pygame.draw.polygon(SCREEN, COLORS[i], [center, (x, y),
                (center[0] + radius * math.cos(math.radians((i+1) * 60)),
                 center[1] + radius * math.sin(math.radians((i+1) * 60)))])

            # Section numbers
            text_x = center[0] + (radius // 1.5) * math.cos(math.radians(i * 60 + 30))
            text_y = center[1] + (radius // 1.5) * math.sin(math.radians(i * 60 + 30))
            text_surface = font.render(labels[i], True, BLACK)
            SCREEN.blit(text_surface, (text_x - 10, text_y - 10))

        # Spinner arrow
        arrow_x = center[0] + (radius - 30) * math.cos(math.radians(angle))
        arrow_y = center[1] + (radius - 30) * math.sin(math.radians(angle))
        pygame.draw.line(SCREEN, RED, center, (arrow_x, arrow_y), 5)

        # Instructions and betting options
        if not has_bet and not spinning:
            instruction_text = font.render("Place your bet: Will the second number be HIGHER or LOWER?", True, BLACK)
            SCREEN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 160))

            # Higher/Lower buttons
            higher_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 120, 100, 40)
            lower_btn = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 120, 100, 40)

            pygame.draw.rect(SCREEN, GREEN, higher_btn)
            pygame.draw.rect(SCREEN, BLUE, lower_btn)

            higher_text = font.render("HIGHER", True, BLACK)
            lower_text = font.render("LOWER", True, BLACK)

            SCREEN.blit(higher_text, (higher_btn.x + 10, higher_btn.y + 10))
            SCREEN.blit(lower_text, (lower_btn.x + 15, lower_btn.y + 10))
        elif has_bet and first_number is None and not spinning:
            instruction_text = font.render("Press SPACE for first spin", True, BLACK)
            SCREEN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 120))
        elif has_bet and first_number is not None and second_number is None and not spinning:
            instruction_text = font.render(f"First number: {first_number}. Press SPACE for second spin", True, BLACK)
            SCREEN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 120))

        # Display Result
        if result_text:
            result_display = font.render(result_text, True, GREEN if "won" in result_text else RED)
            SCREEN.blit(result_display, (WIDTH // 2 - result_display.get_width() // 2, HEIGHT - 200))

        # Help text
        controls_text = font.render("UP/DOWN: Adjust Bet | ESC: Return to Menu", True, BLACK)
        SCREEN.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 40))

        pygame.display.flip()

        # Spin animation
        if spinning:
            angle += spin_speed
            spin_speed *= 0.98  # Slow down gradually

            if spin_speed < 0.5:  # Stop spinning
                spinning = False

                # Calculate which section landed on
                landed_section = int(((angle % 360) // 60))
                landed_number = int(labels[landed_section])

                # If this is the first spin
                if first_number is None:
                    first_number = landed_number
                    result_text = f"First number: {first_number}"
                # If this is the second spin (after betting)
                else:
                    second_number = landed_number
                    result_text = f"Second number: {second_number}"

                    # Process bet result
                    if (bet_choice == "HIGHER" and second_number > first_number) or \
                       (bet_choice == "LOWER" and second_number < first_number):
                        game_data.money += bet_amount * 2
                        result_text = f"You won! +${bet_amount * 2} (First: {first_number}, Second: {second_number})"
                    else:
                        if second_number == first_number:
                            result_text = f"Same number ({second_number})! You lose."
                        else:
                            result_text = f"You lost! (First: {first_number}, Second: {second_number})"

                    # Reset for next round
                    first_number = None
                    second_number = None
                    bet_choice = None
                    has_bet = False

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return  # Exit back to menu

                # Allow arrow keys for betting
                if not spinning:
                    if event.key == pygame.K_UP and bet_amount + 5 <= game_data.money:
                        bet_amount += 5
                    elif event.key == pygame.K_DOWN and bet_amount - 5 >= 5:
                        bet_amount -= 5

                # Space to spin
                if event.key == pygame.K_SPACE and not spinning:
                    if has_bet:  # Can only spin after betting
                        spinning = True
                        spin_speed = random.uniform(25, 40)  # Random initial speed
                    else:
                        result_text = "You need to place a bet first!"

            elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                # Check if bet buttons are clicked
                if not has_bet:
                    # Higher button
                    if WIDTH // 2 - 150 <= event.pos[0] <= WIDTH // 2 - 50 and HEIGHT - 120 <= event.pos[1] <= HEIGHT - 80:
                        if bet_amount <= game_data.money:
                            bet_choice = "HIGHER"
                            game_data.money -= bet_amount
                            has_bet = True
                        else:
                            result_text = "Not enough money!"

                    # Lower button
                    elif WIDTH // 2 + 50 <= event.pos[0] <= WIDTH // 2 + 150 and HEIGHT - 120 <= event.pos[1] <= HEIGHT - 80:
                        if bet_amount <= game_data.money:
                            bet_choice = "LOWER"
                            game_data.money -= bet_amount
                            has_bet = True
                        else:
                            result_text = "Not enough money!"

        clock.tick(60)
