import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinner Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
          (255, 255, 0), (255, 165, 0), (128, 0, 128)]

# Font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Spinner variables
center = (WIDTH // 2, HEIGHT // 2)
radius = 200  
angle = 0
spinning = False
spin_speed = 0
total_money = 0  

# Section labels
labels = ["1", "2", "3", "4", "5", "6"]

# Money values for sections
money_values = {
    "1": 10,
    "2": 20,
    "3": 50,
    "4": 100,
    "5": 200,
    "6": 500
}

# Frame rate control
clock = pygame.time.Clock()

def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + (width // 2 - text_surf.get_width() // 2), 
                            y + (height // 2 - text_surf.get_height() // 2)))
    return pygame.Rect(x, y, width, height)

def draw_spinner(angle, total_money):
    screen.fill(WHITE)  
    
    # Title
    title_font = pygame.font.Font(None, 50)
    title_text = title_font.render("Spinner Game", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    
    # Spinner
    pygame.draw.circle(screen, BLACK, center, radius, 3)
    
    for i in range(6):
        section_angle = math.radians(i * 60)
        x = center[0] + radius * math.cos(section_angle)
        y = center[1] + radius * math.sin(section_angle)
        pygame.draw.line(screen, BLACK, center, (x, y), 2)
        
        # Fill sections
        pygame.draw.polygon(screen, COLORS[i], [center, (x, y), 
            (center[0] + radius * math.cos(math.radians((i+1) * 60)), 
             center[1] + radius * math.sin(math.radians((i+1) * 60)))])
        
        # Section numbers
        text_x = center[0] + (radius // 1.5) * math.cos(math.radians(i * 60 + 30))
        text_y = center[1] + (radius // 1.5) * math.sin(math.radians(i * 60 + 30))
        text_surface = font.render(labels[i], True, BLACK)
        screen.blit(text_surface, (text_x - 10, text_y - 10))
    
    # Spinner arrow
    arrow_x = center[0] + (radius - 30) * math.cos(math.radians(angle))
    arrow_y = center[1] + (radius - 30) * math.sin(math.radians(angle))
    pygame.draw.line(screen, RED, center, (arrow_x, arrow_y), 5)
    
    # 💰 Money Display (Moved Up)
    money_text = font.render(f"Total Money: ${total_money}", True, BLACK)
    screen.blit(money_text, (WIDTH // 2 - money_text.get_width() // 2, HEIGHT - 100))

    # Buttons
    return_button = draw_button("Return", 50, HEIGHT - 50, 100, 40, GREEN)
    exit_button = draw_button("Exit", 350, HEIGHT - 50, 100, 40, RED)
    
    pygame.display.flip()
    return return_button, exit_button

# Game loop
running = True
while running:
    return_button, exit_button = draw_spinner(angle, total_money)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # ✅ Fully Reset Everything when Return button is clicked
            if return_button.collidepoint(mouse_pos):
                angle = 0  # Reset spinner position
                spinning = False  # Stop spinning
                spin_speed = 0  # Reset speed
                total_money = 0  # Reset money
                draw_spinner(angle, total_money)  # 🚀 Instantly update display
            
            # Exit game on Exit button click
            if exit_button.collidepoint(mouse_pos):
                running = False
            
            # Start spinning if not already spinning
            elif not spinning:
                spinning = True
                spin_speed = random.randint(20, 50)  
    
    if spinning:
        angle += spin_speed
        spin_speed = max(0, spin_speed - 1)
        if spin_speed == 0:
            spinning = False  
            
            # 🏆 Determine section landed on
            landed_section = int(((angle % 360) // 60) + 1)  
            money_won = money_values[str(landed_section)]  
            total_money += money_won  

            print(f"Landed on {landed_section}, Won ${money_won}, Total: ${total_money}")  

    clock.tick(60)  

pygame.quit()

