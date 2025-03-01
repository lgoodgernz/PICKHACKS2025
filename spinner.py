# spinner.py
import pygame
import random
import math

def spinner_game(SCREEN):
    WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    COLORS = [(255, 105, 180), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]

    font = pygame.font.Font(None, 36)

    # Define spinner properties
    center = (WIDTH // 2, HEIGHT // 2)
    radius = 200
    angle = 0
    spinning = False
    spin_speed = 0

    # Spinner sections labels
    labels = ["1", "2", "3", "4", "5", "6"]

    # Exit button (to return to the main menu)
    exit_button = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)

    clock = pygame.time.Clock()

    def draw_button(text, rect, color):
        pygame.draw.rect(SCREEN, color, rect)
        text_surf = font.render(text, True, BLACK)
        SCREEN.blit(text_surf, (rect.x + (rect.width // 2 - text_surf.get_width() // 2),
                               rect.y + (rect.height // 2 - text_surf.get_height() // 2)))

    def draw_spinner(angle):
        SCREEN.fill(WHITE)

        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Spinner Game", True, RED)
        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        # Draw spinner circle
        pygame.draw.circle(SCREEN, BLACK, center, radius, 3)

        # Draw sections and labels
        for i in range(6):
            section_angle = math.radians(i * 60)
            x = center[0] + radius * math.cos(section_angle)
            y = center[1] + radius * math.sin(section_angle)
            pygame.draw.line(SCREEN, BLACK, center, (x, y), 2)

            pygame.draw.polygon(SCREEN, COLORS[i], [center, (x, y), (center[0] + radius * math.cos(math.radians((i+1) * 60)),
            center[1] + radius * math.sin(math.radians((i+1) * 60)))])

            # Draw section labels
            text_x = center[0] + (radius // 1.5) * math.cos(math.radians(i * 60 + 30))
            text_y = center[1] + (radius // 1.5) * math.sin(math.radians(i * 60 + 30))
            text_surface = font.render(labels[i], True, BLACK)
            SCREEN.blit(text_surface, (text_x - 10, text_y - 10))

        # Draw arrow indicating current selection
        arrow_x = center[0] + (radius - 30) * math.cos(math.radians(angle))
        arrow_y = center[1] + (radius - 30) * math.sin(math.radians(angle))
        pygame.draw.line(SCREEN, RED, center, (arrow_x, arrow_y), 5)

        # Draw Exit Button
        draw_button("Exit", exit_button, RED)

        pygame.display.flip()

    running = True
    clicked = False  # Track if the exit button is clicked

    while running:
        draw_spinner(angle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the exit button is clicked
                if exit_button.collidepoint(mouse_pos):
                    print("Exit button clicked!")  # Debugging
                    running = False  # Exit the game loop
                    break  # Exit the event loop

                elif not spinning:
                    spinning = True
                    spin_speed = random.randint(20, 50)  # Start spinning with random speed

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("ESC pressed, exiting.")  # Debugging
                running = False

        if spinning:
            angle += spin_speed
            spin_speed = max(0, spin_speed - 1)  # Gradually slow down the spin
            if spin_speed == 0:
                spinning = False  # Stop spinning when speed reaches 0

        clock.tick(60)  # Limit to 60 frames per second

  # Ensure this is called after the main game loop ends
