# Write your code here :-)
import pygame
import random
import game_data  # Import shared money variable

def roulette_game(SCREEN):
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)

    font = pygame.font.Font(None, 36)

    exit_button = pygame.Rect(20, HEIGHT - 50, 100, 30)
    bet_amount = 10  # Default bet
    chosen_color = "RED"  # Default selection

    running = True
    result_text = ""

    while running:
        SCREEN.fill(WHITE)

        # Display Money
        money_text = font.render(f"Money: {game_data.money}", True, BLACK)
        SCREEN.blit(money_text, (20, 20))

        # Display Bet Amount
        bet_text = font.render(f"Bet: ${bet_amount}", True, BLACK)
        SCREEN.blit(bet_text, (20, 60))

        # Display Chosen Color
        color_text = font.render(f"Chosen Color: {chosen_color}", True, RED if chosen_color == "RED" else BLACK)
        SCREEN.blit(color_text, (20, 100))

        # Result Message
        result_display = font.render(result_text, True, GREEN if "won" in result_text else RED)
        SCREEN.blit(result_display, (WIDTH//2 - 100, HEIGHT//2))

        # Draw Exit Button
        pygame.draw.rect(SCREEN, RED, exit_button)
        exit_text = font.render("Exit", True, WHITE)
        SCREEN.blit(exit_text, (30, HEIGHT - 45))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)  # Save before quitting
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    game_data.save_money(game_data.money)  # Save before exiting
                    return  # Exit back to menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return  # Exit back to menu
                elif event.key == pygame.K_UP and bet_amount + 10 <= game_data.money:
                    bet_amount += 10  # Increase bet
                elif event.key == pygame.K_DOWN and bet_amount - 10 > 0:
                    bet_amount -= 10  # Decrease bet
                elif event.key == pygame.K_LEFT:
                    chosen_color = "RED"
                elif event.key == pygame.K_RIGHT:
                    chosen_color = "BLACK"
                elif event.key == pygame.K_SPACE:  # Spin the wheel!
                    if bet_amount > game_data.money:
                        result_text = "Not enough money!"
                    else:
                        game_data.money -= bet_amount  # Deduct bet first
                        spin_result = random.choice(["RED", "BLACK"])  # Random outcome
                        if spin_result == chosen_color:
                            winnings = bet_amount * 2
                            game_data.money += winnings  # Win double the bet
                            result_text = f"You won! +${winnings}"
                        else:
                            result_text = "You lost!"

