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

center = (WIDTH // 2, HEIGHT // 2)
radius = 150
angle = 0
spinning = False
spin_speed = 0

def draw_spinner(angle):
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, center, radius, 3)
    
    
    for i in range(6):
        section_angle = math.radians(i * 60)
        x = center[0] + radius * math.cos(section_angle)
        y = center[1] + radius * math.sin(section_angle)
        pygame.draw.line(screen, BLACK, center, (x, y), 2)
    
    
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
