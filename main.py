import pygame
import tkinter as tk
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1479, 778  # Casino.png size

# Create Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Load images
casino_bg = pygame.image.load("Casino.png")
desk_img = pygame.image.load("Desk1.png")

# Resize Desk1 image (if needed)
desk_width = desk_img.get_width() + 25
desk_height = desk_img.get_height() + 25
desk_img = pygame.transform.scale(desk_img, (desk_width, desk_height))

# Desk position (Bottom-right table)
desk_x, desk_y = 1110, 500  # Adjusted for perfect alignment

# Function to run game and reopen menu
def run_game_and_reopen_menu(game_script):
    root.withdraw()  # Hide Tkinter window
    game_process = subprocess.Popen(["python", game_script])
    game_process.wait()  # Wait for game to close
    root.deiconify()  # Show menu again

# Tkinter setup (for text buttons)
root = tk.Tk()
root.title("Game Menu")
root.geometry("200x200")  # Keep small, Pygame handles visuals
root.withdraw()  # Hide Tkinter window (since Pygame is main)

# Game functions
def horse_game():
    run_game_and_reopen_menu("horse_game.py")

def spinner_game():
    run_game_and_reopen_menu("spinner_game.py")

def blackjack():
    run_game_and_reopen_menu("blackjack.py")

def clicker():
    run_game_and_reopen_menu("clicker.py")

def exit_game():
    pygame.quit()
    root.quit()

# Main loop (Pygame handles images and Desk1 click detection)
running = True
while running:
    screen.blit(casino_bg, (0, 0))  # Draw background
    screen.blit(desk_img, (desk_x, desk_y))  # Draw Desk1 image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if desk_x <= mx <= desk_x + desk_width and desk_y <= my <= desk_y + desk_height:
                clicker()  # Open clicker.py

    pygame.display.update()

pygame.quit()
root.quit()
