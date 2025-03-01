import tkinter as tk
import subprocess

# Function to run a game and reopen the menu after it closes
def run_game_and_reopen_menu(game_script):
    root.withdraw()  # Hide the menu window
    game_process = subprocess.Popen(["python", game_script])  # Run the game
    game_process.wait()  # Wait for the game to close
    root.deiconify()  # Show the menu again

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
    root.quit()  # Close the menu

# Create the main window (Resizable)
root = tk.Tk()
root.title("Game Menu")
root.geometry("700x600")  # Initial window size
root.minsize(500, 400)  # Prevent making it too small

# Load the casino background image
bg_photo = tk.PhotoImage(file="Casino.png")  # Ensure "Casino.png" is 700x600
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Background scales with window

# **FRAME-BASED DESK1 OVERLAY**
desk_frame = tk.Frame(root, width=200, height=120, bg="red")  # Set a temporary color to see its position
desk_frame.place(relx=0.5, rely=0.75, anchor="center")  # Adjust this to line it up

# Load Desk1.png as the button image
desk_photo = tk.PhotoImage(file="Desk1.png")  # Ensure "Desk1.png" exists

# Add Desk1 image inside the frame (button overlay)
desk_button = tk.Button(desk_frame, image=desk_photo, command=clicker, borderwidth=0, highlightthickness=0)
desk_button.pack(expand=True, fill="both")  # Expands within frame

# Text buttons (Fixed size but reposition dynamically)
button_font = ("Arial", 12)
button_fg_color = "white"
button_bg_color = "black"

horse_button = tk.Button(root, text="Horse Game", command=horse_game, font=button_font, fg=button_fg_color, bg=button_bg_color)
spinner_button = tk.Button(root, text="Spinner Game", command=spinner_game, font=button_font, fg=button_fg_color, bg=button_bg_color)
blackjack_button = tk.Button(root, text="BlackJack", command=blackjack, font=button_font, fg=button_fg_color, bg=button_bg_color)
exit_button = tk.Button(root, text="Exit", command=exit_game, font=button_font, fg=button_fg_color, bg=button_bg_color)

# **Dynamic button placement (relative positions)**
horse_button.place(relx=0.05, rely=0.05, anchor="nw")  # Top-left
spinner_button.place(relx=0.95, rely=0.05, anchor="ne")  # Top-right
blackjack_button.place(relx=0.05, rely=0.95, anchor="sw")  # Bottom-left
exit_button.place(relx=0.5, rely=0.5, anchor="center")  # Center

# Run the Tkinter event loop
root.mainloop()
