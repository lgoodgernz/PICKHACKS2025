import pygame
import random
import math
import game_data

def spinner_game(SCREEN):
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    
    # Enhanced color palette
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)  # Crimson red
    GREEN = (34, 139, 34)  # Forest green
    BLUE = (30, 144, 255)  # Dodger blue
    GOLD = (255, 215, 0)
    PURPLE = (148, 0, 211)
    BACKGROUND_COLOR = (240, 248, 255)  # Light blue background
    
    # Enhanced spinner colors - more vibrant casino-style colors
    COLORS = [
        (220, 20, 60),    # Crimson
        (65, 105, 225),   # Royal Blue
        (255, 215, 0),    # Gold
        (34, 139, 34),    # Forest Green
        (148, 0, 211),    # Purple
        (255, 140, 0)     # Dark Orange
    ]
    
    # Button colors
    BUTTON_COLOR = (70, 130, 180)  # Steel blue
    BUTTON_HOVER_COLOR = (100, 149, 237)  # Cornflower blue
    BUTTON_TEXT_COLOR = WHITE
    
    # Load fancy font if available, otherwise use default
    try:
        title_font = pygame.font.Font("freesansbold.ttf", 42)
        large_font = pygame.font.Font("freesansbold.ttf", 30)
        font = pygame.font.Font("freesansbold.ttf", 20)
        small_font = pygame.font.Font("freesansbold.ttf", 16)
    except:
        title_font = pygame.font.Font(None, 48)
        large_font = pygame.font.Font(None, 36)
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)

    # Spinner variables
    center = (WIDTH // 2, HEIGHT // 2 - 20)  # Moved up slightly
    radius = 180
    arrow_length = radius - 20
    angle = 0
    spinning = False
    spin_speed = 0
    
    # Shadow offset for 3D effect
    shadow_offset = 4

    # Game state variables
    bet_amount = 5
    first_number = None
    second_number = None
    bet_choice = None  # "HIGHER" or "LOWER"
    result_text = ""
    game_state = "CHOOSE_BET"  # States: CHOOSE_BET, FIRST_SPIN, CHOOSE_HIGHER_LOWER, SECOND_SPIN, RESULT
    
    # Button hover state
    hovered_button = None

    # Section labels
    labels = ["1", "2", "3", "4", "5", "6"]

    # Frame rate control
    clock = pygame.time.Clock()
    
    # Helper function to create fancy buttons
    def draw_button(rect, color, text, text_color=WHITE, hover=False):
        # Draw button shadow for 3D effect
        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(SCREEN, (50, 50, 50, 180), shadow_rect, border_radius=12)
        
        # Draw the main button
        pygame.draw.rect(SCREEN, 
                         BUTTON_HOVER_COLOR if hover else color, 
                         rect, 
                         border_radius=12)
        
        # Add a slight inner border
        pygame.draw.rect(SCREEN, 
                         (color[0]-30 if color[0]>30 else 0, 
                          color[1]-30 if color[1]>30 else 0,
                          color[2]-30 if color[2]>30 else 0), 
                         rect, 
                         width=2, 
                         border_radius=12)
        
        # Render text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        SCREEN.blit(text_surface, text_rect)
        
        return rect

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BACKGROUND_COLOR)
        
        # Reset hovered button
        hovered_button = None
        
        # Draw decorative casino elements
        # Top and bottom borders
        pygame.draw.rect(SCREEN, GOLD, (0, 0, WIDTH, 10))
        pygame.draw.rect(SCREEN, GOLD, (0, HEIGHT-10, WIDTH, 10))
        
        # Draw a fancy title background
        pygame.draw.rect(SCREEN, (25, 25, 112), (0, 10, WIDTH, 70))  # Midnight Blue strip
        for i in range(10):
            pygame.draw.circle(SCREEN, GREEN, (50 + i*150, 45), 5)  # Gold dots
            
        # Title with shadow for 3D effect
        title_shadow = title_font.render("🎰 Higher or Lower Spinner 🎰", True, BLACK)
        title_text = title_font.render("🎰 Higher or Lower Spinner 🎰", True, GOLD)
        SCREEN.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 2, 22))
        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        # Game info panel with shadow
        info_panel = pygame.Rect(20, 100, 260, 150)
        pygame.draw.rect(SCREEN, (50, 50, 50, 180), pygame.Rect(info_panel.x+4, info_panel.y+4, info_panel.width, info_panel.height), border_radius=15)
        pygame.draw.rect(SCREEN, (25, 25, 112), info_panel, border_radius=15)
        pygame.draw.rect(SCREEN, GOLD, info_panel, width=2, border_radius=15)
        
        # Display Money and Bet with some glitter
        money_text = large_font.render(f"Money: ${game_data.money}", True, GOLD)
        SCREEN.blit(money_text, (40, 120))
        
        bet_text = large_font.render(f"Bet: ${bet_amount}", True, WHITE)
        SCREEN.blit(bet_text, (40, 165))
        
        # Display current bet choice if made
        if bet_choice:
            choice_color = BLUE if bet_choice == "LOWER" else GREEN
            choice_text = large_font.render(f"Betting: {bet_choice}", True, choice_color)
            SCREEN.blit(choice_text, (40, 210))

        # Spinner with nicer 3D effect
        # Spinner shadow for 3D effect
        pygame.draw.circle(SCREEN, (50, 50, 50, 180), (center[0]+shadow_offset, center[1]+shadow_offset), radius+5)
        
        # Outer ring of the spinner
        pygame.draw.circle(SCREEN, GOLD, center, radius+10, 0)
        pygame.draw.circle(SCREEN, BLACK, center, radius, 0)
        
        # Spinner sections with nicer colors
        for i in range(6):
            start_angle = math.radians(i * 60)
            end_angle = math.radians((i+1) * 60)
            
            # Calculate points for the polygon
            points = [center]
            for j in range(60):
                angle_rad = start_angle + (end_angle - start_angle) * j / 60
                x = center[0] + radius * math.cos(angle_rad)
                y = center[1] + radius * math.sin(angle_rad)
                points.append((x, y))
                
            # Close the polygon
            points.append((center[0] + radius * math.cos(end_angle), 
                          center[1] + radius * math.sin(end_angle)))
            
            # Draw filled section
            pygame.draw.polygon(SCREEN, COLORS[i], points)
            
            # Add a subtle gradient/shading effect (simplified)
            for k in range(5):
                inner_radius = radius - (10 * k)
                if inner_radius <= 0:
                    break
                    
                x1 = center[0] + inner_radius * math.cos(start_angle)
                y1 = center[1] + inner_radius * math.sin(start_angle)
                x2 = center[0] + inner_radius * math.cos(end_angle)
                y2 = center[1] + inner_radius * math.sin(end_angle)
                
                pygame.draw.line(SCREEN, 
                                (min(COLORS[i][0]+20, 255), 
                                 min(COLORS[i][1]+20, 255), 
                                 min(COLORS[i][2]+20, 255)), 
                                (x1, y1), (x2, y2), 1)

        # Section dividing lines
        for i in range(6):
            section_angle = math.radians(i * 60)
            x = center[0] + radius * math.cos(section_angle)
            y = center[1] + radius * math.sin(section_angle)
            pygame.draw.line(SCREEN, WHITE, center, (x, y), 2)

            # Section numbers - make them more visible with background circles
            text_angle = math.radians(i * 60 + 30)
            text_x = center[0] + (radius * 0.7) * math.cos(text_angle)
            text_y = center[1] + (radius * 0.7) * math.sin(text_angle)
            
            # Number background circle
            pygame.draw.circle(SCREEN, WHITE, (int(text_x), int(text_y)), 20)
            
            # Number text
            text_surface = large_font.render(labels[i], True, BLACK)
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            SCREEN.blit(text_surface, text_rect)
        
        # Center hub of spinner
        pygame.draw.circle(SCREEN, GOLD, center, 20)
        pygame.draw.circle(SCREEN, (70, 70, 70), center, 15)

        # Spinner arrow with nicer design
        arrow_angle = math.radians(angle)
        arrow_x = center[0] + arrow_length * math.cos(arrow_angle)
        arrow_y = center[1] + arrow_length * math.sin(arrow_angle)
        
        # Arrow with shadow for 3D effect
        shadow_start = (center[0] + shadow_offset, center[1] + shadow_offset)
        shadow_end = (arrow_x + shadow_offset, arrow_y + shadow_offset)
        
        # Draw arrow shadow
        pygame.draw.line(SCREEN, (50, 50, 50), shadow_start, shadow_end, 8)
        
        # Draw arrow base
        pygame.draw.line(SCREEN, RED, center, (arrow_x, arrow_y), 8)
        
        # Draw arrow head
        head_length = 20
        head_angle1 = arrow_angle + math.radians(150)
        head_angle2 = arrow_angle - math.radians(150)
        
        head_x1 = arrow_x + head_length * math.cos(head_angle1)
        head_y1 = arrow_y + head_length * math.sin(head_angle1)
        head_x2 = arrow_x + head_length * math.cos(head_angle2)
        head_y2 = arrow_y + head_length * math.sin(head_angle2)
        
        pygame.draw.polygon(SCREEN, RED, [(arrow_x, arrow_y), (head_x1, head_y1), (head_x2, head_y2)])
        
        # Control panel area
        control_panel = pygame.Rect(WIDTH // 2 - 350, HEIGHT - 180, 700, 150)
        pygame.draw.rect(SCREEN, (50, 50, 50, 180), pygame.Rect(control_panel.x+4, control_panel.y+4, control_panel.width, control_panel.height), border_radius=15)
        pygame.draw.rect(SCREEN, (25, 25, 112), control_panel, border_radius=15)
        pygame.draw.rect(SCREEN, GOLD, control_panel, width=2, border_radius=15)

        # Instructions and buttons based on game state
        if game_state == "CHOOSE_BET":
            instruction_text = large_font.render("Set your bet amount with UP/DOWN arrow keys", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 150))
            SCREEN.blit(instruction_text, instruction_rect)
            
            # Bet amount buttons
            decrease_btn = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 100, 50, 40)
            increase_btn = pygame.Rect(WIDTH // 2 + 130, HEIGHT - 100, 50, 40)
            
            # Check button hover
            decrease_hover = decrease_btn.collidepoint(mouse_pos)
            increase_hover = increase_btn.collidepoint(mouse_pos)
            
            draw_button(decrease_btn, (180, 40, 40), "-", hover=decrease_hover)
            draw_button(increase_btn, (40, 180, 40), "+", hover=increase_hover)
            
            if decrease_hover: hovered_button = "decrease"
            if increase_hover: hovered_button = "increase"
            
            # Current bet display
            bet_display = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 40)
            pygame.draw.rect(SCREEN, (0, 0, 50), bet_display, border_radius=12)
            pygame.draw.rect(SCREEN, GOLD, bet_display, 2, border_radius=12)
            
            current_bet = large_font.render(f"${bet_amount}", True, WHITE)
            SCREEN.blit(current_bet, current_bet.get_rect(center=bet_display.center))
            
            # Confirm button
            confirm_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 40)
            confirm_hover = confirm_btn.collidepoint(mouse_pos)
            draw_button(confirm_btn, BUTTON_COLOR, "PLACE BET", hover=confirm_hover)
            
            if confirm_hover: hovered_button = "confirm"
            
        elif game_state == "FIRST_SPIN":
            instruction_text = large_font.render("Press SPACE to spin for your first number", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 120))
            SCREEN.blit(instruction_text, instruction_rect)
            
            # Spin button
            spin_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 40)
            spin_hover = spin_btn.collidepoint(mouse_pos)
            draw_button(spin_btn, BUTTON_COLOR, "SPIN", hover=spin_hover)
            
            if spin_hover: hovered_button = "spin"
            
        elif game_state == "CHOOSE_HIGHER_LOWER":
            # Show first number with animation
            first_num_text = large_font.render(f"First number: {first_number}", True, WHITE)
            SCREEN.blit(first_num_text, first_num_text.get_rect(center=(WIDTH // 2, HEIGHT - 160)))
            
            # Question text
            question_text = large_font.render("Will the next number be HIGHER or LOWER?", True, GOLD)
            SCREEN.blit(question_text, question_text.get_rect(center=(WIDTH // 2, HEIGHT - 120)))
            
            # Higher/Lower buttons
            higher_btn = pygame.Rect(WIDTH // 2 - 220, HEIGHT - 70, 200, 40)
            lower_btn = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 70, 200, 40)
            
            higher_hover = higher_btn.collidepoint(mouse_pos)
            lower_hover = lower_btn.collidepoint(mouse_pos)
            
            draw_button(higher_btn, GREEN, "HIGHER ↑", hover=higher_hover)
            draw_button(lower_btn, BLUE, "LOWER ↓", hover=lower_hover)
            
            if higher_hover: hovered_button = "higher"
            if lower_hover: hovered_button = "lower"
            
        elif game_state == "SECOND_SPIN":
            # Show first number and bet choice
            first_text = font.render(f"First Number: {first_number}", True, WHITE)
            SCREEN.blit(first_text, (WIDTH // 2 - 250, HEIGHT - 150))
            
            bet_choice_color = GREEN if bet_choice == "HIGHER" else BLUE
            choice_text = font.render(f"Your Bet: {bet_choice}", True, bet_choice_color)
            SCREEN.blit(choice_text, (WIDTH // 2 + 50, HEIGHT - 150))
            
            # Spin instruction
            spin_text = large_font.render("Press SPACE for final spin!", True, GOLD)
            SCREEN.blit(spin_text, spin_text.get_rect(center=(WIDTH // 2, HEIGHT - 110)))
            
            # Spin button
            spin_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 40)
            spin_hover = spin_btn.collidepoint(mouse_pos)
            draw_button(spin_btn, BUTTON_COLOR, "SPIN", hover=spin_hover)
            
            if spin_hover: hovered_button = "spin"
            
        elif game_state == "RESULT":
            # Show both numbers and result
            result_box = pygame.Rect(WIDTH // 2 - 300, HEIGHT - 170, 600, 100)
            pygame.draw.rect(SCREEN, (0, 0, 50), result_box, border_radius=15)
            pygame.draw.rect(SCREEN, GOLD, result_box, width=2, border_radius=15)
            
            # Format the result text for better display
            if "won" in result_text:
                result_display = large_font.render(result_text, True, GREEN)
                # Add celebratory animation (sparkling effect would go here in a full implementation)
            else:
                result_display = large_font.render(result_text, True, RED)
            
            SCREEN.blit(result_display, result_display.get_rect(center=(WIDTH // 2, HEIGHT - 125)))
            
            # Play again button
            play_again_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)
            again_hover = play_again_btn.collidepoint(mouse_pos)
            draw_button(play_again_btn, BUTTON_COLOR, "PLAY AGAIN", hover=again_hover)
            
            if again_hover: hovered_button = "again"

        # Help text at the bottom
        help_box = pygame.Rect(0, HEIGHT - 30, WIDTH, 30)
        pygame.draw.rect(SCREEN, (25, 25, 112), help_box)
        pygame.draw.rect(SCREEN, GOLD, help_box, 1)
        
        controls_text = small_font.render("UP/DOWN: Adjust Bet | SPACE: Spin | ESC: Return to Menu", True, WHITE)
        SCREEN.blit(controls_text, controls_text.get_rect(center=(WIDTH // 2, HEIGHT - 15)))

        pygame.display.flip()

        # Spin animation
        if spinning:
            angle += spin_speed
            spin_speed *= 0.98  # Slow down gradually

            if spin_speed < 0.5:  # Stop spinning
                spinning = False

                # Calculate which section landed on
                landed_section = int(((angle % 360) // 60))
                landed_number = int(labels[landed_section])

                # If this is the first spin
                if game_state == "FIRST_SPIN":
                    first_number = landed_number
                    result_text = f"First number: {first_number}"
                    game_state = "CHOOSE_HIGHER_LOWER"
                    
                # If this is the second spin
                elif game_state == "SECOND_SPIN":
                    second_number = landed_number
                    
                    # Process bet result
                    if (bet_choice == "HIGHER" and second_number > first_number) or \
                       (bet_choice == "LOWER" and second_number < first_number):
                        game_data.money += bet_amount * 2
                        result_text = f"You won! +${bet_amount * 2} (First: {first_number}, Second: {second_number})"
                        # Play win sound effect would go here
                    else:
                        if second_number == first_number:
                            result_text = f"Same number ({second_number})! You lose."
                        else:
                            result_text = f"You lost! (First: {first_number}, Second: {second_number})"
                        # Play loss sound effect would go here

                    game_state = "RESULT"

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return  # Exit back to menu

                # Handle arrow keys for betting
                if game_state == "CHOOSE_BET":
                    if event.key == pygame.K_UP and bet_amount + 5 <= game_data.money:
                        bet_amount += 5
                    elif event.key == pygame.K_DOWN and bet_amount - 5 >= 5:
                        bet_amount -= 5

                # Space to spin
                if event.key == pygame.K_SPACE and not spinning:
                    if game_state == "FIRST_SPIN":
                        spinning = True
                        spin_speed = random.uniform(25, 40)  # Random initial speed
                    elif game_state == "SECOND_SPIN":
                        spinning = True
                        spin_speed = random.uniform(25, 40)  # Random initial speed

            elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                if game_state == "CHOOSE_BET":
                    # Decrease bet button
                    decrease_btn = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 100, 50, 40)
                    if decrease_btn.collidepoint(event.pos) and bet_amount - 5 >= 5:
                        bet_amount -= 5
                    
                    # Increase bet button
                    increase_btn = pygame.Rect(WIDTH // 2 + 130, HEIGHT - 100, 50, 40)
                    if increase_btn.collidepoint(event.pos) and bet_amount + 5 <= game_data.money:
                        bet_amount += 5
                    
                    # Confirm bet button
                    confirm_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 40)
                    if confirm_btn.collidepoint(event.pos) or pygame.K_SPACE:
                        if bet_amount <= game_data.money:
                            game_data.money -= bet_amount
                            game_state = "FIRST_SPIN"
                        else:
                            result_text = "Not enough money!"
                
                elif game_state == "FIRST_SPIN":
                    # Spin button
                    spin_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 40)
                    if spin_btn.collidepoint(event.pos):
                        spinning = True
                        spin_speed = random.uniform(25, 40)
                
                elif game_state == "CHOOSE_HIGHER_LOWER":
                    # Higher button
                    higher_btn = pygame.Rect(WIDTH // 2 - 220, HEIGHT - 70, 200, 40)
                    if higher_btn.collidepoint(event.pos):
                        bet_choice = "HIGHER"
                        game_state = "SECOND_SPIN"

                    # Lower button
                    lower_btn = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 70, 200, 40)
                    if lower_btn.collidepoint(event.pos):
                        bet_choice = "LOWER"
                        game_state = "SECOND_SPIN"
                
                elif game_state == "SECOND_SPIN":
                    # Spin button
                    spin_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 40)
                    if spin_btn.collidepoint(event.pos) or (pygame.K_SPACE and pygame.KEYDOWN):
                        spinning = True
                        spin_speed = random.uniform(25, 40)
                
                elif game_state == "RESULT":
                    for event in pygame.event.get():
                        # Play again button
                        play_again_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)
                        if play_again_btn.collidepoint(event.pos):
                            # Reset for new game
                            first_number = None
                            second_number = None
                            bet_choice = None
                            result_text = ""
                            game_state = "CHOOSE_BET"
                        elif event.type == pygame.KEYDOWN:
                            if event.type == pygame.KEYDOWN:
                                first_number = None
                                second_number = None
                                bet_choice = None
                                result_text = ""
                                game_state = "CHOOSE_BET"


        clock.tick(60)