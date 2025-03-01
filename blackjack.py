import pygame
import random
import game_data

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
GOLD = (218, 165, 32)
DARK_GREEN = (0, 100, 0)

def deal_card():
    return random.choice(list(CARD_VALUES.keys()))

def calculate_hand_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def draw_text(SCREEN, text, size, x, y, color=WHITE, center=False, max_width=None):
    font = pygame.font.Font(None, size)

    # If max_width is specified, check if text needs to be shortened
    if max_width:
        text_surface = font.render(text, True, color)
        if text_surface.get_width() > max_width:
            # Try shortening the text with ellipsis
            while text and font.render(text + "...", True, color).get_width() > max_width:
                text = text[:-1]
            text = text + "..." if text else "..."

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y) if center else (x, y))
    SCREEN.blit(text_surface, text_rect)

    return text_rect

def draw_card(SCREEN, card, x, y, width=60, height=90):
    # Card background
    pygame.draw.rect(SCREEN, WHITE, (x, y, width, height))
    pygame.draw.rect(SCREEN, BLACK, (x, y, width, height), 2)

    # Card value
    color = RED if card in ['♥', '♦'] else BLACK
    if card == '?':
        # Draw card back pattern
        pygame.draw.rect(SCREEN, RED, (x+5, y+5, width-10, height-10))
        pygame.draw.rect(SCREEN, GOLD, (x+10, y+10, width-20, height-20), 2)
        pygame.draw.lines(SCREEN, GOLD, False, [(x+15, y+15), (x+width-15, y+height-15)], 2)
        pygame.draw.lines(SCREEN, GOLD, False, [(x+width-15, y+15), (x+15, y+height-15)], 2)
    else:
        # Draw card value - ensure it fits
        font_size = 40
        if len(card) > 1:  # For "10", make font smaller
            font_size = 30

        font = pygame.font.Font(None, font_size)
        text = font.render(card, True, BLACK)
        text_rect = text.get_rect(center=(x + width//2, y + height//2))
        SCREEN.blit(text, text_rect)

        # Draw smaller value in corners
        small_font_size = 20
        if len(card) > 1:  # For "10", make font smaller
            small_font_size = 16

        small_font = pygame.font.Font(None, small_font_size)
        small_text = small_font.render(card, True, BLACK)
        SCREEN.blit(small_text, (x + 5, y + 5))
        SCREEN.blit(small_text, (x + width - 15 - (5 if len(card) > 1 else 0), y + height - 20))

def draw_hand(SCREEN, hand, x, y, hidden=False):
    # Calculate the total width needed for all cards
    card_width = 60
    card_spacing = 35  # Reduced spacing between cards
    total_width = (len(hand) - 1) * card_spacing + card_width

    # Start drawing from an adjusted position to center the hand
    for i, card in enumerate(hand):
        # Display first card and hide second if hidden is True
        display_card = card if not hidden or i != 1 else '?'
        draw_card(SCREEN, display_card, x + i * card_spacing, y)

def draw_rounded_rect(SCREEN, rect, color, radius=20, border_width=0, border_color=None):
    """Draw a rectangle with rounded corners"""
    rect = pygame.Rect(rect)

    # Draw the main rectangle
    pygame.draw.rect(SCREEN, color, rect, border_radius=radius)

    # Draw the border if specified
    if border_width > 0:
        border_color = border_color or WHITE
        pygame.draw.rect(SCREEN, border_color, rect, border_width, border_radius=radius)

def blackjack_game(SCREEN):
    # Load blackjack table background
    try:
        table_bg = pygame.image.load("blackjack_table.png")
        screen_width, screen_height = SCREEN.get_size()
        table_bg = pygame.transform.scale(table_bg, (screen_width, screen_height))
    except:
        # Fallback if image doesn't load
        table_bg = None

    pygame.display.flip()
    screen_width, screen_height = SCREEN.get_size()

    bet_amount = 5
    player_hand = []
    dealer_hand = []
    game_over = True
    result_text = "Press SPACE to Start"
    result_color = WHITE

    # Button sizes and positions - ensure they're properly spaced
    button_width, button_height = 150, 60
    button_y = screen_height - 120  # Move buttons up to avoid overlay with instructions
    hit_button = pygame.Rect(screen_width//2 - 160, button_y, button_width, button_height)
    stand_button = pygame.Rect(screen_width//2 + 10, button_y, button_width, button_height)

    running = True
    while running:
        # Draw background
        if table_bg:
            SCREEN.blit(table_bg, (0, 0))
        else:
            SCREEN.fill(DARK_GREEN)


        # Draw money and bet info in a stylized box with fixed width
        money_box = pygame.Rect(20, 20, 280, 80)
        draw_rounded_rect(SCREEN, money_box, (0, 0, 0, 150), border_width=2)

        # Ensure text fits within the box
        money_text = f"Money: ${game_data.money}"
        bet_text = f"Bet: ${bet_amount} (Up/Down to adjust)"
        bet_text = f"Bet: ${bet_amount} (Up/Down to adjust)"

        draw_text(SCREEN, money_text, 36, money_box.x + 140, money_box.y + 20, color=GOLD, max_width=money_box.width - 40)
        draw_text(SCREEN, bet_text, 28, money_box.x + 140, money_box.y + 55, max_width=money_box.width - 40)

        # Calculate better sizes for dealer and player areas based on screen size
        area_width = min(500, screen_width - 100)  # Limit width on smaller screens
        area_height = 150
        area_x = (screen_width - area_width) // 2

        dealer_area = pygame.Rect(area_x, 100, area_width, area_height)
        player_area = pygame.Rect(area_x, 280, area_width, area_height)  # Lower the player area

        # Draw dealer's section with title bar
        draw_rounded_rect(SCREEN, dealer_area, (0, 0, 0, 100), border_width=2)
        draw_text(SCREEN, "Dealer's Hand", 30, dealer_area.x + 20, dealer_area.y - 15)

        # Draw player's section with title bar
        draw_rounded_rect(SCREEN, player_area, (0, 0, 0, 100), border_width=2)
        draw_text(SCREEN, "Your Hand", 30, player_area.x + 20, player_area.y - 15)

        # Draw dealer's cards - centered in the dealer area
        if dealer_hand:
            cards_x = dealer_area.x + 20
            cards_y = dealer_area.y + 50
            draw_hand(SCREEN, dealer_hand, cards_x, cards_y, not game_over)

            if game_over:
                dealer_value = calculate_hand_value(dealer_hand)
                draw_text(SCREEN, f"Value: {dealer_value}", 28,
                          dealer_area.right - 80, dealer_area.bottom - 30)
        else:
            draw_text(SCREEN, "No cards dealt", 30, dealer_area.centerx, dealer_area.centery + 20, center=True)

        # Draw player's cards - centered in the player area
        if player_hand:
            cards_x = player_area.x + 20
            cards_y = player_area.y + 50
            draw_hand(SCREEN, player_hand, cards_x, cards_y)

            player_value = calculate_hand_value(player_hand)
            draw_text(SCREEN, f"Value: {player_value}", 28,
                      player_area.right - 80, player_area.bottom - 30)
        else:
            draw_text(SCREEN, "No cards dealt", 30, player_area.centerx, player_area.centery + 20, center=True)

        # Draw result message
        if result_text and game_over:
            # Create a semi-transparent background for the result text
            text_width = min(len(result_text) * 20 + 40, screen_width - 100)
            text_height = 60
            text_bg_rect = pygame.Rect(
                screen_width//2 - text_width//2,
                screen_height//2 - text_height//2 + 100,
                text_width,
                text_height
            )
            draw_rounded_rect(SCREEN, text_bg_rect, BLACK, border_width=2)
            draw_text(SCREEN, result_text, 48, screen_width//2, screen_height//2 + 100,
                      result_color, center=True, max_width=text_width - 20)

        # Draw action buttons
        if not game_over:
            # Draw Hit button
            draw_rounded_rect(SCREEN, hit_button, (50, 50, 50), border_width=2)
            draw_text(SCREEN, "HIT", 40, hit_button.centerx, hit_button.centery, WHITE, center=True)

            # Draw Stand button
            draw_rounded_rect(SCREEN, stand_button, (50, 50, 50), border_width=2)
            draw_text(SCREEN, "STAND", 40, stand_button.centerx, stand_button.centery, WHITE, center=True)


        # Draw instructions at the very bottom with proper spacing
        instruction_y = screen_height - 30
        instruction_bg = pygame.Rect(0, instruction_y - 15, screen_width, 30)
        draw_rounded_rect(SCREEN, instruction_bg, (0, 0, 0, 150))

        if game_over:
            draw_text(SCREEN, "Press SPACE to play or ESC to exit", 25,
                      screen_width//2, instruction_y, center=True)
        else:
            draw_text(SCREEN, "Press H to Hit | Press S to Stand", 25,
                      screen_width//2, instruction_y, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return

                # Adjust bet before game starts
                if game_over:
                    if event.key == pygame.K_UP and bet_amount + 5 <= game_data.money:
                        bet_amount += 5
                    elif event.key == pygame.K_DOWN and bet_amount > 5:
                        bet_amount -= 5
                    elif event.key == pygame.K_SPACE:
                        if game_data.money < bet_amount:
                            result_text = "Not enough money!"
                            result_color = RED
                        else:
                            game_data.money -= bet_amount
                            game_data.save_money(game_data.money)
                            player_hand = [deal_card(), deal_card()]
                            dealer_hand = [deal_card(), deal_card()]
                            game_over = False
                            result_text = ""

                # Gameplay controls after starting
                elif not game_over:
                    if event.key == pygame.K_h:  # Hit
                        player_hand.append(deal_card())
                        if calculate_hand_value(player_hand) > 21:
                            result_text = "BUST! You lose."
                            result_color = RED
                            game_over = True
                    elif event.key == pygame.K_s:  # Stand
                        while calculate_hand_value(dealer_hand) < 17:
                            dealer_hand.append(deal_card())

                        player_value = calculate_hand_value(player_hand)
                        dealer_value = calculate_hand_value(dealer_hand)

                        if dealer_value > 21:
                            winnings = int(bet_amount * 2)
                            game_data.money += winnings
                            result_text = f"Dealer busts! You win ${winnings}!"
                            result_color = GOLD
                        elif player_value > dealer_value:
                            winnings = int(bet_amount * 2)
                            game_data.money += winnings
                            result_text = f"You win ${winnings}!"
                            result_color = GOLD
                        elif player_value == dealer_value:
                            game_data.money += bet_amount
                            result_text = "Push! Bet returned."
                            result_color = WHITE
                        else:
                            result_text = "Dealer wins! You lose."
                            result_color = RED

                        game_over = True
                        game_data.save_money(game_data.money)

            # Handle mouse clicks for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Check if Play button was clicked
                    play_button = pygame.Rect(screen_width//2 - 75, screen_height//2 + 50, 150, 60)
                    if play_button.collidepoint(event.pos):
                        if game_data.money < bet_amount:
                            result_text = "Not enough money!"
                            result_color = RED
                        else:
                            game_data.money -= bet_amount
                            game_data.save_money(game_data.money)
                            player_hand = [deal_card(), deal_card()]
                            dealer_hand = [deal_card(), deal_card()]
                            game_over = False
                            result_text = ""
                else:
                    # Check if Hit button was clicked
                    if hit_button.collidepoint(event.pos):
                        player_hand.append(deal_card())
                        if calculate_hand_value(player_hand) > 21:
                            result_text = "BUST! You lose."
                            result_color = RED
                            game_over = True

                    # Check if Stand button was clicked
                    elif stand_button.collidepoint(event.pos):
                        while calculate_hand_value(dealer_hand) < 17:
                            dealer_hand.append(deal_card())

                        player_value = calculate_hand_value(player_hand)
                        dealer_value = calculate_hand_value(dealer_hand)

                        if dealer_value > 21:
                            winnings = int(bet_amount * 2)
                            game_data.money += winnings
                            result_text = f"Dealer busts! You win ${winnings}!"
                            result_color = GOLD
                        elif player_value > dealer_value:
                            winnings = int(bet_amount * 2)
                            game_data.money += winnings
                            result_text = f"You win ${winnings}!"
                            result_color = GOLD
                        elif player_value == dealer_value:
                            game_data.money += bet_amount
                            result_text = "Push! Bet returned."
                            result_color = WHITE
                        else:
                            result_text = "Dealer wins! You lose."
                            result_color = RED

                        game_over = True
                        game_data.save_money(game_data.money)
