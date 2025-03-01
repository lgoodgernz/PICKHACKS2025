import pygame
import random
import game_data # Import shared money variable

# Initialize pygame
pygame.init()
money = game_data.load_money()
# Game Constants
    # WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height() # change when implemened into main menu
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

# Load horse images from Downloads folder with transparency support
horse1 = pygame.image.load("horse1.png").convert_alpha()
horse2 = pygame.image.load("horse2.png").convert_alpha()
horse3 = pygame.image.load("horse3.png").convert_alpha()
horse4 = pygame.image.load("horse4.png").convert_alpha()
horse5 = pygame.image.load("horse5.png").convert_alpha()
horse6 = pygame.image.load("horse6.png").convert_alpha()
horse7 = pygame.image.load("horse7.png").convert_alpha()
horse8 = pygame.image.load("horse8.png").convert_alpha()

horse_images = [horse1, horse2, horse3, horse4, horse5, horse6, horse7, horse8]

# Resize horse images
horse_images = [pygame.transform.scale(horse, (80, 50)) for horse in horse_images]

# Horse properties
num_horses = len(horse_images)

def start_race(bet_amount, selected_horse):
    global money  # Use global money to update it
    # Initialize horses
    horses = []
    for i in range(num_horses):
        horses.append({
            "x": 0,
            "y": i * (HEIGHT // num_horses) + 20,
            "speed": random.randint(2, 5)  # Random speed for each horse
        })
    
    # Game loop for the race
    running = True
    clock = pygame.time.Clock()
    winner = None
    while running:
        screen.blit(background, (0, 0))  # Draw background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Move horses with random speed variations, adjusting speed by 2/3
        for horse in horses:
            horse["speed"] += random.randint(-1, 1)  # Randomly increase or decrease speed
            horse["speed"] = max(1, horse["speed"])  # Ensure speed doesn't go below 1
            horse["x"] += int(horse["speed"] * 2 / 3)  # Scale speed to 2/3
            if horse["x"] >= WIDTH - 80:  # Stop when a horse reaches the end
                winner = horses.index(horse) + 1
                running = False
                break
        
        # Draw horses
        for i, horse in enumerate(horses):
            screen.blit(horse_images[i], (horse["x"], horse["y"]))
        
        pygame.display.flip()
        clock.tick(30)

    # Determine winnings or losses
    if winner == selected_horse:
        winnings = bet_amount * 8
        money += winnings
        print(f"Your horse won! You earned ${winnings}!")
    else:
        money -= bet_amount
        print(f"Your horse lost! You lost ${bet_amount}.")

    # Save the updated money
    game_data.money = money
    game_data.save_money(money)

    # Return to main menu
    main_menu()


# Main menu loop
# Main menu loop
def main_menu():
    global money  # Use global money to access and update it
    bet_amount = 10  # Initial bet amount
    horse_number = 1  # Initial horse number selection
    running = True
    while running:
        background = pygame.image.load("horsemenu.png")
        screen.fill(BLACK)
        # Draw the start button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, BUTTON_RECT)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, BUTTON_RECT)
        
        # Draw button text
        font = pygame.font.Font(None, 36)
        text = font.render("Start Race", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))




        pygame.display.flip()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("ESC pressed, returning to menu.")  # Debugging
                game_data.save_money(game_data.money)  # Save before exiting
                return 

        # Display money
        text = font.render(f"Money: ${money}", True, WHITE)
        screen.blit(text, (100, 100))
        
        # Display updated bet amount
        bet_text = font.render(f"Bet Amount: ${bet_amount}", True, (255, 255, 255))
        screen.blit(bet_text, (WIDTH // 2 - bet_text.get_width() // 2, HEIGHT // 2 + 100))

        # Display selected horse number
        horse_text = font.render(f"Horse Number: {horse_number}", True, (255, 255, 255))
        screen.blit(horse_text, (WIDTH // 2 - horse_text.get_width() // 2, HEIGHT // 2 + 150))

        # Instructions for adjusting bet and horse selection
        instructions = font.render("UP/DOWN to adjust bet, LEFT/RIGHT to change horse", True, (255, 255, 255))
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 + 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
                    if bet_amount <= money:
                        start_race(bet_amount, horse_number)  # Start the race when the button is clicked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and bet_amount < money:  # Increase bet if money allows
                    bet_amount = min(bet_amount + 10, money)
                elif event.key == pygame.K_DOWN and bet_amount > 10:  # Decrease bet, with a minimum of 10
                    bet_amount -= 10
                elif event.key == pygame.K_LEFT:  # Select previous horse
                    horse_number = max(1, horse_number - 1)
                elif event.key == pygame.K_RIGHT:  # Select next horse
                    horse_number = min(num_horses, horse_number + 1)

        pygame.display.flip()

    game_data.save_money(money) 
    pygame.quit()


# Run the main menu
main_menu()
