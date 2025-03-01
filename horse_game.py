import pygame
import random
import game_data  # Import shared money variable

def horse_game(SCREEN):
    pygame.init()
    money = game_data.load_money()

    # Game Constants
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)
    BUTTON_HOVER_COLOR = (0, 200, 0)
    BUTTON_RECT = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    EXIT_BUTTON = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)  # Exit button

    font = pygame.font.Font(None, 36)

    # Load background and horse images
    background = pygame.image.load("horsebackground.png").convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    horse_images = [pygame.image.load(f"horse{i}.png").convert_alpha() for i in range(1, 9)]
    horse_images = [pygame.transform.scale(horse, (80, 50)) for horse in horse_images]

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Horse Race")

    # Main menu loop
    def main_menu():
        nonlocal money  # Use nonlocal to modify the outer money variable
        bet_amount = 10  # Initial bet amount
        horse_number = 1  # Initial horse number selection
        running = True
        clicked = False  # Track click state
        background = pygame.image.load("horsemenu.png")

        while running:
            screen.blit(background, (0, 0))  # Draw background
            SCREEN.fill(BLACK)

            # Display money
            text = font.render(f"Money: ${money}", True, WHITE)
            screen.blit(text, (20, 20))

            # Draw Start Button with Hover Effect
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, BUTTON_RECT)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, BUTTON_RECT)
            
            text = font.render("Start Race", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            # Draw Exit Button
            pygame.draw.rect(screen, (255, 0, 0), EXIT_BUTTON)
            exit_text = font.render("Exit", True, WHITE)
            screen.blit(exit_text, (EXIT_BUTTON.x + 20, EXIT_BUTTON.y + 10))

            pygame.display.flip()  # Ensure everything is updated before checking events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_data.save_money(money)  # Save before quitting
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if EXIT_BUTTON.collidepoint((mouse_x, mouse_y)):
                        game_data.save_money(money)  # Save before exiting
                        return  # Exit back to menu
                    elif BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
                        if bet_amount <= money:
                            start_race(bet_amount, horse_number)  # Start the race when the button is clicked
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and bet_amount < money:  # Increase bet if money allows
                        bet_amount = min(bet_amount + 10, money)
                    elif event.key == pygame.K_DOWN and bet_amount > 10:  # Decrease bet, with a minimum of 10
                        bet_amount -= 10
                    elif event.key == pygame.K_LEFT:  # Select previous horse
                        horse_number = max(1, horse_number - 1)
                    elif event.key == pygame.K_RIGHT:  # Select next horse
                        horse_number = min(8, horse_number + 1)

        game_data.save_money(money)  # Save before exiting

    def start_race(bet_amount, selected_horse):
        nonlocal money  # Use nonlocal money to update it

        # Initialize horses
        horses = [{"x": 0, "y": i * (HEIGHT // 8) + 20, "speed": random.randint(2, 5)} for i in range(8)]

        # Game loop for the race
        running = True
        clock = pygame.time.Clock()
        winner = None
        while running:
            screen.blit(background, (0, 0))  # Draw background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_data.save_money(money)  # Save before quitting
                    running = False

            # Move horses
            for horse in horses:
                horse["speed"] += random.randint(-1, 1)
                horse["speed"] = max(1, horse["speed"])
                horse["x"] += int(horse["speed"] * 2 / 3)
                if horse["x"] >= WIDTH - 80:
                    winner = horses.index(horse) + 1
                    running = False
                    break

            # Draw horses
            for i, horse in enumerate(horses):
                screen.blit(horse_images[i], (horse["x"], horse["y"]))

            pygame.display.flip()
            clock.tick(30)

        # Calculate winnings or losses
        if winner == selected_horse:
            winnings = bet_amount * 8
            money += winnings
            print(f"Your horse won! You earned ${winnings}!")
        else:
            money -= bet_amount
            print(f"Your horse lost! You lost ${bet_amount}.")

        game_data.save_money(money)  # Save after race

        main_menu()  # Return to main menu

    main_menu()  # Start the game

# Call the horse_game function to start the game
