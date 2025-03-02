import pygame
from clicker import clicker_game
from roulette import roulette_game  # Import the roulette game
from horse_game import horse_game  # Import the horse game
from nba import nba_game # Import the NBA game
from spinner import spinner_game # Import the Spinner game
from help_page import help_page
from blackjack import blackjack_game

pygame.init()

# Constants
WIDTH, HEIGHT = 1479, 778
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casino Game")

# Load assets
BACKGROUND = pygame.image.load("Casino.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

desk_img = pygame.image.load("Desk1.png")
desk_original = pygame.transform.scale(desk_img, (271, 145))
desk_pressed = pygame.transform.scale(desk_img, (271, 145))
desk_rect = desk_original.get_rect(topleft=(1096, 486))

# Desk2 button
desk2_img = pygame.image.load("Desk2.png")
desk2_original = pygame.transform.scale(desk2_img, (237, 122))
desk2_pressed = pygame.transform.scale(desk2_img, (237, 122))
desk2_rect = desk2_original.get_rect(topleft=(1001, 199))

# Desk3 button (Updated Position and Dimensions)
desk3_img = pygame.image.load("Desk3.png")
desk3_original = pygame.transform.scale(desk3_img, (248, 131))
desk3_pressed = pygame.transform.scale(desk3_img, (248, 131))
desk3_rect = desk3_original.get_rect(topleft=(230, 199))

# Desk4 button
desk4_img = pygame.image.load("Desk4.png")
desk4_original = pygame.transform.scale(desk4_img, (309, 178))
desk4_pressed = pygame.transform.scale(desk4_img, (309, 178))
desk4_rect = desk4_original.get_rect(topleft=(592, 186))

# Desk5 button
desk5_img = pygame.image.load("Desk5.png")
desk5_original = pygame.transform.scale(desk5_img, (244, 153))
desk5_pressed = pygame.transform.scale(desk5_img, (244, 153))
desk5_rect = desk5_original.get_rect(topleft=(114, 503))

# Exit button
exit_img = pygame.image.load("Exit.png")
exit_original = pygame.transform.scale(exit_img, (90, 32))
exit_pressed = pygame.transform.scale(exit_img, (90, 32))
exit_rect = exit_original.get_rect(topleft=(693, 728))

# HorseBoard button
horseboard_img = pygame.image.load("HorseBoard.png")
horseboard_original = pygame.transform.scale(horseboard_img, (215, 175))
horseboard_pressed = pygame.transform.scale(horseboard_img, (215, 175))
horseboard_rect = horseboard_original.get_rect(topleft=(636, 9))

# Get_Money button
get_money_img = pygame.image.load("Get_Money.png")
get_money_original = pygame.transform.scale(get_money_img, (157, 157))
get_money_pressed = pygame.transform.scale(get_money_img, (157, 157))
get_money_rect = get_money_original.get_rect(topleft=(279, -24))

# Help button
help_img = pygame.image.load("Help.png")
help_original = pygame.transform.scale(help_img, (277, 277))
help_pressed = pygame.transform.scale(help_img, (277, 277))
help_rect = help_original.get_rect(topleft=(947, -78))

# Game state
current_game = None
clicked = False

def draw_main_menu():
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(desk_pressed if clicked else desk_original, desk_rect.topleft)
    SCREEN.blit(desk2_pressed if clicked else desk2_original, desk2_rect.topleft)
    SCREEN.blit(desk3_pressed if clicked else desk3_original, desk3_rect.topleft)
    SCREEN.blit(desk4_pressed if clicked else desk4_original, desk4_rect.topleft)
    SCREEN.blit(desk5_pressed if clicked else desk5_original, desk5_rect.topleft)
    SCREEN.blit(horseboard_pressed if clicked else horseboard_original, horseboard_rect.topleft)
    SCREEN.blit(get_money_pressed if clicked else get_money_original, get_money_rect.topleft)
    SCREEN.blit(help_pressed if clicked else help_original, help_rect.topleft)
    SCREEN.blit(exit_pressed if clicked else exit_original, exit_rect.topleft)

    # Load additional images
    # Playing_card
    playing_card_img = pygame.image.load("Playing_card.png")
    playing_card_img = pygame.transform.scale(playing_card_img, (64, 54))
    playing_card_rect = playing_card_img.get_rect(topleft=(311, 79))
    SCREEN.blit(playing_card_img, playing_card_rect.topleft)

    # Carpet (Updated position and dimensions)
    carpet_img = pygame.image.load("carpet.png")
    carpet_img = pygame.transform.scale(carpet_img, (192, 133))  # Updated dimensions
    carpet_rect = carpet_img.get_rect(topleft=(990, 353))  # Updated position
    SCREEN.blit(carpet_img, carpet_rect.topleft)

    # Spinning Wheel
    spinning_wheel_img = pygame.image.load("Spinning_Wheel.png")
    spinning_wheel_img = pygame.transform.scale(spinning_wheel_img, (41, 41))  # Dimensions rounded
    spinning_wheel_rect = spinning_wheel_img.get_rect(topleft=(230, 420))
    SCREEN.blit(spinning_wheel_img, spinning_wheel_rect.topleft)

    # Pink girl (Updated to Pink_girl_two.png)
    pink_girl_two_img = pygame.image.load("Pink_girl_two.png")
    pink_girl_two_img = pygame.transform.scale(pink_girl_two_img, (52, 80))
    pink_girl_two_rect = pink_girl_two_img.get_rect(topleft=(1120, 434))
    SCREEN.blit(pink_girl_two_img, pink_girl_two_rect.topleft)

    # New Pink_girl image
    pink_girl_img = pygame.image.load("Pink_girl.png")
    pink_girl_img = pygame.transform.scale(pink_girl_img, (54, 84))  # Set dimensions
    pink_girl_rect = pink_girl_img.get_rect(topleft=(316, 115))  # Set position
    SCREEN.blit(pink_girl_img, pink_girl_rect.topleft)

    # Basketball
    basketball_img = pygame.image.load("Basketball.png")
    basketball_img = pygame.transform.scale(basketball_img, (41, 41))
    basketball_rect = basketball_img.get_rect(topleft=(1112, 112))
    SCREEN.blit(basketball_img, basketball_rect.topleft)

    # Roulette table
    roulette_table_img = pygame.image.load("roulette_table.png")
    roulette_table_img = pygame.transform.scale(roulette_table_img, (210, 210))
    roulette_table_rect = roulette_table_img.get_rect(topleft=(1039, 304))
    SCREEN.blit(roulette_table_img, roulette_table_rect.topleft)

    pygame.display.update()

def main():
    global current_game, clicked
    running = True
    while running:
        SCREEN.fill((0, 0, 0))

        if current_game is None:
            draw_main_menu()
        elif current_game == "clicker":
            clicker_game(SCREEN)
            current_game = None
        elif current_game == "roulette":
            roulette_game(SCREEN)
            current_game = None
        elif current_game == "horse_game":
            horse_game(SCREEN)
            current_game = None
        elif current_game == "nba":
            nba_game(SCREEN)
            current_game = None
        elif current_game == "spinner":
            spinner_game(SCREEN)
            current_game = None
        elif current_game == "help_page":
            help_page(SCREEN)
            current_game = None
        elif current_game == "blackjack":
            blackjack_game(SCREEN)
            current_game = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_game is None:
                if desk_rect.collidepoint(event.pos):
                    current_game = "roulette"
                elif desk2_rect.collidepoint(event.pos):
                    current_game = "nba"
                elif desk3_rect.collidepoint(event.pos):
                    current_game = "blackjack"
                elif desk4_rect.collidepoint(event.pos):
                    current_game = "horse_game"
                elif desk5_rect.collidepoint(event.pos):
                    print("Desk5 clicked!")
                    current_game = "spinner"
                elif horseboard_rect.collidepoint(event.pos):
                    print("HorseBoard clicked!")
                    current_game = "horse_game"
                elif get_money_rect.collidepoint(event.pos):
                    print("Get_Money button clicked!")
                    current_game = "clicker"
                elif help_rect.collidepoint(event.pos):
                    print("Help button clicked!")
                    current_game = "help_page"
                elif exit_rect.collidepoint(event.pos):
                    print("Exiting the game...")
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_game = None

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
