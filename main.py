import tkinter as tk
import subprocess
import sys
import os

# Function to run a game, close the menu, and reopen it after the game closes
def run_game_and_reopen_menu(game_script):
    root.quit()  # Close the main menu
    game_process = subprocess.Popen(["python", game_script])  # Run the game script
    game_process.wait()  # Wait for the game process to close
    reopen_menu()  # Reopen the menu after the game closes

def reopen_menu():
    subprocess.Popen([sys.executable, "main.py"])  # Reopen the menu

# Functions for each game
def horse_game():
    run_game_and_reopen_menu("horse_game.py")

def spinner_game():
    run_game_and_reopen_menu("spinner_game.py")

def blackjack():
    run_game_and_reopen_menu("blackjack.py")

def clicker():
    run_game_and_reopen_menu("clicker.py")

def exit_game():
    root.quit()  # Close the menu

# Create the main window
root = tk.Tk()
root.title("Game Menu")
root.geometry("1000x600")  # Set window size

# Load the casino background image using Tkinter's built-in PhotoImage
bg_photo = tk.PhotoImage(file="Casino.png")  # Ensure "Casino.png" exists in the same folder

# Create a label for the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Make it fill the entire window

# Title label for the game
title_label = tk.Label(root, text="Select a Game", font=("Arial", 18), bg="red", fg="white")
title_label.pack(pady=20)  # Add spacing

# Button properties
button_font = ("Arial", 14)
button_fg_color = "white"
button_bg_color = "black"

# Create buttons
horse_button = tk.Button(root, text="Horse Game", command=horse_game, font=button_font, fg=button_fg_color, bg=button_bg_color)
spinner_button = tk.Button(root, text="Spinner Game", command=spinner_game, font=button_font, fg=button_fg_color, bg=button_bg_color)
blackjack_button = tk.Button(root, text="BlackJack", command=blackjack, font=button_font, fg=button_fg_color, bg=button_bg_color)
clicker_button = tk.Button(root, text="Clicker", command=clicker, font=button_font, fg=button_fg_color, bg=button_bg_color)
exit_button = tk.Button(root, text="Exit", command=exit_game, font=button_font, fg=button_fg_color, bg=button_bg_color)

# Position buttons within 1000x600 dimensions
button_width = 120
button_height = 40

horse_button.place(x=20, y=20, width=button_width, height=button_height)  # Top-left
spinner_button.place(x=1000 - button_width - 20, y=20, width=button_width, height=button_height)  # Top-right
blackjack_button.place(x=20, y=600 - button_height - 20, width=button_width, height=button_height)  # Bottom-left
clicker_button.place(x=1000 - button_width - 20, y=600 - button_height - 20, width=button_width, height=button_height)  # Bottom-right
exit_button.place(relx=0.5, rely=0.5, anchor="center", width=button_width, height=button_height)  # Center

# Run the Tkinter event loop
root.mainloop()
