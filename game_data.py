# game_data.py

# Load money from file
def load_money():
    try:
        with open("money.txt", "r") as file:
            return int(file.read())  # Read the money value
    except FileNotFoundError:
        return 0  # Default to 0 if the file does not exist

# Save money to file
def save_money(money):
    with open("money.txt", "w") as file:
        file.write(str(money))  # Save the money value

money = load_money()  # Load money when the game starts
