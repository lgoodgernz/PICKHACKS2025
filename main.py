import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
import subprocess  # For running another Python script
import sys
import os

# Function to run the game and reopen the menu after the game closes
def run_game_and_reopen_menu(game_script):
    root.quit()  # Close the main menu
    game_process = subprocess.Popen(["python", game_script])  # Run the game script in a separate process
    game_process.wait()  # Wait for the game process to close before reopening the menu
    reopen_menu()  # Reopen the menu after the game closes

def reopen_menu():
    subprocess.Popen([sys.executable, "main.py"])  # Run the main menu script again, but in a separate process

# Functions for each game (Placeholders for now)
def horse_game():
    run_game_and_reopen_menu("horse_game.py")

def spinner_game():
    run_game_and_reopen_menu("spinner_game.py")

def blackjack():
    run_game_and_reopen_menu("blackjack.py")

def clicker():
    run_game_and_reopen_menu("clicker.py")

def exit_game():
    root.quit()  # Close the main menu
    exit()  # Exit the program

# Create the main window
root = tk.Tk()
root.title("Game Menu")

# Set window size to 1000x600
root.geometry("1000x600")  # Adjust the size of the window

# Load the casino background image (resize to match the window size)
bg_image = Image.open("Casino.png")  # Path to the image you added
bg_image = bg_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize it to 1000x600
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Make the background fill the entire window

# Title label for the game
title_label = tk.Label(root, text="Select a Game", font=("Arial", 18), bg="red", fg="white")
title_label.pack(pady=20)  # Add space above the title

# Create buttons for each game with text-only design and solid colors
button_bg_color = "black"  # Button background color
button_fg_color = "white"  # Button text color
button_font = ("Arial", 14)

horse_button = tk.Button(root, text="Horse Game", command=horse_game, font=button_font, fg=button_fg_color, bg=button_bg_color)
spinner_button = tk.Button(root, text="Spinner Game", command=spinner_game, font=button_font, fg=button_fg_color, bg=button_bg_color)
blackjack_button = tk.Button(root, text="BlackJack", command=blackjack, font=button_font, fg=button_fg_color, bg=button_bg_color)
clicker_button = tk.Button(root, text="Clicker", command=clicker, font=button_font, fg=button_fg_color, bg=button_bg_color)
exit_button = tk.Button(root, text="Exit", command=exit_game, font=button_font, fg=button_fg_color, bg=button_bg_color)

# Adjust button positions to make sure they fit within the window size
# Allowing padding to prevent them from being too close to the edges
button_width = 120
button_height = 40

# Top-left corner (with padding)
horse_button.place(x=20, y=20, width=button_width, height=button_height)  # Ensure it fits

# Top-right corner (with padding)
spinner_button.place(x=1000 - button_width - 20, y=20, width=button_width, height=button_height)  # Adjusted for new window size

# Bottom-left corner (with padding)
blackjack_button.place(x=20, y=600 - button_height - 20, width=button_width, height=button_height)  # Adjusted for new window size

# Bottom-right corner (with padding)
clicker_button.place(x=1000 - button_width - 20, y=600 - button_height - 20, width=button_width, height=button_height)  # Adjusted for new window size

# Center of the window (Exit button)
exit_button.place(relx=0.5, rely=0.5, anchor="center", width=button_width, height=button_height)

# Start the Tkinter event loop
root.mainloop()
