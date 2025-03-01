import pygame
from clicker import clicker_game
from roulette import roulette_game  # Import the roulette game
from horse_game import horse_game  # Import the horse game

pygame.init()

# Constants
WIDTH, HEIGHT = 1479, 778
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casino Game")

# Load assets
BACKGROUND = pygame.image.load("Casino.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

desk_img = pygame.image.load("Desk1.png")
desk_original = pygame.transform.scale(desk_img, (271, 145))  # Resizing Desk1 to 271x145
desk_pressed = pygame.transform.scale(desk_img, (271, 145))  # Make pressed version the same size
desk_rect = desk_original.get_rect(topleft=(1096, 486))  # Desk1 position at (1096, 486)

# New Desk2 button
desk2_img = pygame.image.load("Desk2.png")
desk2_original = pygame.transform.scale(desk2_img, (237, 122))  # Resizing Desk2 to 237x122
desk2_pressed = pygame.transform.scale(desk2_img, (237, 122))  # Make pressed version the same size
desk2_rect = desk2_original.get_rect(topleft=(1001, 199))  # Desk2 position at (1001, 199)

# New Desk3 button (Now leads to clicker game)
desk3_img = pygame.image.load("Desk3.png")
desk3_original = pygame.transform.scale(desk3_img, (251, 124))  # Resizing Desk3 to 251x124
desk3_pressed = pygame.transform.scale(desk3_img, (251, 124))  # Make pressed version the same size
desk3_rect = desk3_original.get_rect(topleft=(232, 199))  # Desk3 position at (232, 199)

# New Desk4 button (Now leads to horse_game)
desk4_img = pygame.image.load("Desk4.png")
desk4_original = pygame.transform.scale(desk4_img, (309, 178))  # Resizing Desk4 to 309x178
desk4_pressed = pygame.transform.scale(desk4_img, (309, 178))  # Make pressed version the same size
desk4_rect = desk4_original.get_rect(topleft=(592, 186))  # Desk4 position at (592, 186)

# New Desk5 button (New button, leads to any specific game)
desk5_img = pygame.image.load("Desk5.png")
desk5_original = pygame.transform.scale(desk5_img, (244, 153))  # Resizing Desk5 to 244x153
desk5_pressed = pygame.transform.scale(desk5_img, (244, 153))  # Make pressed version the same size
desk5_rect = desk5_original.get_rect(topleft=(114, 503))  # Desk5 position at (114, 503)

# New Exit button
exit_img = pygame.image.load("Exit.png")
exit_original = pygame.transform.scale(exit_img, (90, 32))  # Resizing Exit button to 90x32
exit_pressed = pygame.transform.scale(exit_img, (90, 32))  # Make pressed version the same size
exit_rect = exit_original.get_rect(topleft=(693, 728))  # Exit button position at (693, 728)

# New HorseBoard button (Position: (636, 9) and Dimensions: W: 215, H: 175)
horseboard_img = pygame.image.load("HorseBoard.png")
horseboard_original = pygame.transform.scale(horseboard_img, (215, 175))  # Resizing HorseBoard to 215x175
horseboard_pressed = pygame.transform.scale(horseboard_img, (215, 175))  # Make pressed version the same size
horseboard_rect = horseboard_original.get_rect(topleft=(636, 9))  # HorseBoard position at (636, 9)

# New Get_Money button (Position: (279, -24) and Dimensions: W: 157, H: 157)
get_money_img = pygame.image.load("Get_Money.png")
get_money_original = pygame.transform.scale(get_money_img, (157, 157))  # Resizing Get_Money button to 157x157
get_money_pressed = pygame.transform.scale(get_money_img, (157, 157))  # Make pressed version the same size
get_money_rect = get_money_original.get_rect(topleft=(279, -24))  # Get_Money button position at (279, -24)

# New Help button (Position: (947, -78) and Dimensions: W: 277, H: 277)
help_img = pygame.image.load("Help.png")
help_original = pygame.transform.scale(help_img, (277, 277))  # Resizing Help button to 277x277
help_pressed = pygame.transform.scale(help_img, (277, 277))  # Make pressed version the same size
help_rect = help_original.get_rect(topleft=(947, -78))  # Help button position at (947, -78)

# Game state
current_game = None
clicked = False

def draw_main_menu():
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(desk_pressed if clicked else desk_original, desk_rect.topleft)
    SCREEN.blit(desk2_pressed if clicked else desk2_original, desk2_rect.topleft)  # Draw Desk2
    SCREEN.blit(desk3_pressed if clicked else desk3_original, desk3_rect.topleft)  # Draw Desk3
    SCREEN.blit(desk4_pressed if clicked else desk4_original, desk4_rect.topleft)  # Draw Desk4
    SCREEN.blit(desk5_pressed if clicked else desk5_original, desk5_rect.topleft)  # Draw Desk5
    SCREEN.blit(horseboard_pressed if clicked else horseboard_original, horseboard_rect.topleft)  # Draw HorseBoard
    SCREEN.blit(get_money_pressed if clicked else get_money_original, get_money_rect.topleft)  # Draw Get_Money button
    SCREEN.blit(help_pressed if clicked else help_original, help_rect.topleft)  # Draw Help button
    SCREEN.blit(exit_pressed if clicked else exit_original, exit_rect.topleft)  # Draw Exit button
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
            current_game = None  # Return to the main menu after finishing the game
        elif current_game == "roulette":
            roulette_game(SCREEN)  # Show the roulette game
            current_game = None  # Return to the main menu after finishing the game
        elif current_game == "horse_game":
            horse_game(SCREEN)  # Show the horse game
            current_game = None  # Return to the main menu after finishing the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_game is None:
                if desk_rect.collidepoint(event.pos):  # desk1 click should bring to roulette game
                    current_game = "roulette"  # desk1 now leads to roulette game
                elif desk2_rect.collidepoint(event.pos):
                    current_game = "clicker"  # desk2 leads to clicker game
                elif desk3_rect.collidepoint(event.pos):  # desk3 click should bring to clicker game
                    current_game = "clicker"  # desk3 now leads to clicker game
                elif desk4_rect.collidepoint(event.pos):  # desk4 click should bring to horse game
                    current_game = "horse_game"  # desk4 leads to horse game
                elif desk5_rect.collidepoint(event.pos):  # New desk5 click to open desired game
                    print("Desk5 clicked!")  # Test message for Desk5 (change to actual game)
                    current_game = "clicker"  # Change this to the game you want Desk5 to open
                elif horseboard_rect.collidepoint(event.pos):  # HorseBoard click (if needed for another game)
                    print("HorseBoard clicked!")  # Test message for HorseBoard (change to actual game)
                    current_game = "horse_game"  # Open horse game when HorseBoard is clicked
                elif get_money_rect.collidepoint(event.pos):  # Get_Money button clicked
                    print("Get_Money button clicked!")
                    current_game = "clicker"  # Get_Money button triggers clicker game
                elif help_rect.collidepoint(event.pos):  # Help button clicked
                    print("Help button clicked!")
                    current_game = "clicker"  # Help button triggers clicker game
                elif exit_rect.collidepoint(event.pos):  # Check if Exit button is clicked
                    print("Exiting the game...")  # Test message for Exit
                    running = False  # Exit the game loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_game = None  # Return to main menu

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
