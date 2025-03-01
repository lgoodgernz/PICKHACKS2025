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
desk_original = pygame.transform.scale(desk_img, (200, 200))
desk_pressed = pygame.transform.scale(desk_img, (180, 180))
desk_rect = desk_original.get_rect(topleft=(1110, 500))

# Game state
current_game = None
clicked = False

def draw_main_menu():
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(desk_pressed if clicked else desk_original, desk_rect.topleft)
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
            current_game = None  # <---- This makes sure the menu returns
        elif current_game == "spinner":
            spinner_game(SCREEN)
            current_game = None  # <---- Same for spinner

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_game is None:
                if desk_rect.collidepoint(event.pos):
                    current_game = "clicker"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_game = None  # Return to main menu

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
