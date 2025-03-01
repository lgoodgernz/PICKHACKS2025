import pygame
import random
import math


pygame.init()


WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinner Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]


pygame.font.init()
font = pygame.font.Font(None, 36)


center = (WIDTH // 2, HEIGHT // 2)
radius = 150
angle = 0
spinning = False
spin_speed = 0


labels = ["1", "2", "3", "4", "5", "6"]

def draw_spinner(angle):
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, center, radius, 3)
   
    for i in range(6):
        section_angle = math.radians(i * 60)
        x = center[0] + radius * math.cos(section_angle)
        y = center[1] + radius * math.sin(section_angle)
        pygame.draw.line(screen, BLACK, center, (x, y), 2)
        
      
        pygame.draw.polygon(screen, COLORS[i], [center, (x, y), (center[0] + radius * math.cos(math.radians((i+1) * 60)),
                                                              center[1] + radius * math.sin(math.radians((i+1) * 60)))])
        
       
        text_x = center[0] + (radius // 2) * math.cos(math.radians(i * 60 + 30))
        text_y = center[1] + (radius // 2) * math.sin(math.radians(i * 60 + 30))
        text_surface = font.render(labels[i], True, BLACK)
        screen.blit(text_surface, (text_x - 10, text_y - 10))
    
  
    arrow_x = center[0] + (radius - 20) * math.cos(math.radians(angle))
    arrow_y = center[1] + (radius - 20) * math.sin(math.radians(angle))
    pygame.draw.line(screen, RED, center, (arrow_x, arrow_y), 5)
    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
            spinning = True
            spin_speed = random.randint(50, 100)
    
    if spinning:
        angle += spin_speed
        spin_speed = max(0, spin_speed - 1)  
        if spin_speed == 0:
            spinning = False  
    
    draw_spinner(angle)
    pygame.time.delay(50)

pygame.quit()

