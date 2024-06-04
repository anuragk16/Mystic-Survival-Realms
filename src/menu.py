import pygame
import sys


# Function to display the menu screen
def menu_screen():
    # Initialize Pygame
    pygame.init()

    # Set up display
    Width, Height = 800, 600
    win = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Game Menu")

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Define fonts
    font = pygame.font.Font(None, 36)

    
    
    while True:
        # Clear the screen
        win.fill(WHITE)

        # Display menu title
        title_text = font.render("Menu", True, BLACK)
        title_rect = title_text.get_rect(center=(Width // 2, Height // 4))
        win.blit(title_text, title_rect)

        # Create "Start" button
        start_button = pygame.Rect(Width // 4, Height // 2, Width // 4, Height // 8)
        pygame.draw.rect(win, BLACK, start_button)
        start_text = font.render("Start", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button.center)
        win.blit(start_text, start_text_rect)

        # Create "Exit" button
        exit_button = pygame.Rect(Width // 4 * 2, Height // 2, Width // 4, Height // 8)
        pygame.draw.rect(win, BLACK, exit_button)
        exit_text = font.render("Exit", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        win.blit(exit_text, exit_text_rect)

        # Update the display
        pygame.display.flip()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return "start"
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
