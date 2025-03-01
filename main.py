import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os
import game_data  # Import shared money variable

# Function to run the game and reopen the menu after the game closes
def run_game_and_reopen_menu(game_script):
    root.quit()  # Close the main menu
    game_process = subprocess.Popen(["python", game_script])  # Run the game script in a separate process
    game_process.wait()  # Wait for the game process to close before reopening the menu
    game_data.money = game_data.load_money()  # Reload money when returning
    reopen_menu()  # Reopen the menu after the game closes

def reopen_menu():
    subprocess.Popen([sys.executable, "main.py"])  # Run the main menu script again

def clicker():
    run_game_and_reopen_menu("clicker.py")

def exit_game():
    root.quit()
    exit()

# Create the main window
root = tk.Tk()
root.title("Game Menu")
root.geometry("1000x600")

bg_image = Image.open("Casino.png")
bg_image = bg_image.resize((1000, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

title_label = tk.Label(root, text="Select a Game", font=("Arial", 18), bg="red", fg="white")
title_label.pack(pady=20)

# Money Display Label
money_label = tk.Label(root, text=f"Money: {game_data.money}", font=("Arial", 16), bg="black", fg="white")
money_label.pack()

clicker_button = tk.Button(root, text="Clicker", command=clicker, font=("Arial", 14), fg="white", bg="black")
clicker_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_game, font=("Arial", 14), fg="white", bg="black")
exit_button.pack(pady=10)

root.mainloop()
