import pygame
import random
import game_data  # Import shared money variable

def horse_game():
    # Initialize pygame
    pygame.init()
    money = game_data.load_money()

    # Game Constants
    WIDTH, HEIGHT = 1000, 600
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)
    BUTTON_HOVER_COLOR = (0, 200, 0)
    BUTTON_RECT = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    BET_TEXT_RECT = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Horse Race")

    # Load background image
    background = pygame.image.load("horsebackground.png").convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load horse images
    horse_images = [
        pygame.transform.scale(pygame.image.load(f"horse{i}.png").convert_alpha(), (80, 50))
        for i in range(1, 9)
    ]

    num_horses = len(horse_images)

    def start_race(bet_amount, selected_horse):
        nonlocal money  # Use nonlocal to modify money inside horse_game
        horses = [
            {"x": 0, "y": i * (HEIGHT // num_horses) + 20, "speed": random.randint(2, 5)}
            for i in range(num_horses)
        ]

        running = True
        clock = pygame.time.Clock()
        winner = None
        while running:
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            for horse in horses:
                horse["speed"] += random.randint(-1, 1)
                horse["speed"] = max(1, horse["speed"])
                horse["x"] += int(horse["speed"] * 2 / 3)
                if horse["x"] >= WIDTH - 80:
                    winner = horses.index(horse) + 1
                    running = False
                    break

            for i, horse in enumerate(horses):
                screen.blit(horse_images[i], (horse["x"], horse["y"]))

            pygame.display.flip()
            clock.tick(30)

        if winner == selected_horse:
            winnings = bet_amount * 8
            money += winnings
            print(f"Your horse won! You earned ${winnings}!")
        else:
            money -= bet_amount
            print(f"Your horse lost! You lost ${bet_amount}.")

        game_data.money = money
        game_data.save_money(money)
        main_menu()

    def main_menu():
        nonlocal money
        bet_amount = 10
        horse_number = 1
        running = True
        background = pygame.image.load("horsemenu.png")

        while running:
            screen.blit(background, (0, 0))
            pygame.event.pump()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, BUTTON_RECT)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, BUTTON_RECT)

            font = pygame.font.Font(None, 36)
            text = font.render("Start Race", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            text = font.render(f"Money: ${money}", True, WHITE)
            screen.blit(text, (100, 100))
            bet_text = font.render(f"Bet Amount: ${bet_amount}", True, (255, 255, 255))
            screen.blit(bet_text, (WIDTH // 2 - bet_text.get_width() // 2, HEIGHT // 2 + 100))
            horse_text = font.render(f"Horse Number: {horse_number}", True, (255, 255, 255))
            screen.blit(horse_text, (WIDTH // 2 - horse_text.get_width() // 2, HEIGHT // 2 + 150))
            instructions = font.render("UP/DOWN to adjust bet, LEFT/RIGHT to change horse", True, (255, 255, 255))
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 + 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BUTTON_RECT.collidepoint((mouse_x, mouse_y)) and bet_amount <= money:
                        start_race(bet_amount, horse_number)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and bet_amount < money:
                        bet_amount = min(bet_amount + 10, money)
                    elif event.key == pygame.K_DOWN and bet_amount > 10:
                        bet_amount -= 10
                    elif event.key == pygame.K_LEFT:
                        horse_number = max(1, horse_number - 1)
                    elif event.key == pygame.K_RIGHT:
                        horse_number = min(num_horses, horse_number + 1)
                    elif event.key == pygame.K_ESCAPE:
                        game_data.save_money(game_data.money)
                        return

            pygame.display.flip()

        game_data.save_money(money)
        pygame.quit()

    # Run the main menu
    main_menu()

# Call the horse_game function to start the game
horse_game()
