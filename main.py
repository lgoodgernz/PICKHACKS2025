import pygame
import game_data
from clicker import clicker_game

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

# New Desk3 button
desk3_img = pygame.image.load("Desk3.png")
desk3_original = pygame.transform.scale(desk3_img, (251, 124))  # Resizing Desk3 to 251x124
desk3_pressed = pygame.transform.scale(desk3_img, (251, 124))  # Make pressed version the same size
desk3_rect = desk3_original.get_rect(topleft=(232, 199))  # Desk3 position at (232, 199)

# New Exit button
exit_img = pygame.image.load("Exit.png")
exit_original = pygame.transform.scale(exit_img, (90, 32))  # Resizing Exit button to 90x32
exit_pressed = pygame.transform.scale(exit_img, (90, 32))  # Make pressed version the same size
exit_rect = exit_original.get_rect(topleft=(693, 728))  # Exit button position at (693, 728)

# Game state
current_game = None
clicked = False

def draw_main_menu():
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(desk_pressed if clicked else desk_original, desk_rect.topleft)
    SCREEN.blit(desk2_pressed if clicked else desk2_original, desk2_rect.topleft)  # Draw Desk2
    SCREEN.blit(desk3_pressed if clicked else desk3_original, desk3_rect.topleft)  # Draw Desk3
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_game is None:
                if desk_rect.collidepoint(event.pos):
                    current_game = "clicker"  # All buttons now bring you to clicker game
                elif desk2_rect.collidepoint(event.pos):
                    current_game = "clicker"  # All buttons now bring you to clicker game
                elif desk3_rect.collidepoint(event.pos):
                    current_game = "clicker"  # All buttons now bring you to clicker game
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
