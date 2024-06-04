import pygame
import os


class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, win):
        # Draw player's health and mana on the screen
        health_text = self.font.render(f"Health: {self.player.stats['HP']}", True, (255, 255, 255))
        mana_text = self.font.render(f"Mana: {self.player.stats['MP']}", True, (255, 255, 255))
        win.blit(health_text, (10, 10))
        win.blit(mana_text, (10, 40))
        
        

class DialogBox:
    def __init__(self, text, font, duration):
        self.text = text  # Text to display in the dialog box
        self.font = font  # Font for rendering text
        self.duration = duration  # Duration in milliseconds for how long the dialog box stays visible
        self.visible = False  # Flag to track if the dialog box is currently visible
        self.timer = 0  # Timer to track the duration the dialog box has been visible
    
    def show(self):
        # Show the dialog box
        self.visible = True
        self.timer = 0  # Reset the timer
    
    def hide(self):
        # Hide the dialog box
        self.visible = False
        self.timer = 0  # Reset the timer
    
    def update(self):
        # Update the timer and hide the dialog box if the duration has elapsed
        if self.visible:
            self.timer += 1  # Update the timer
            if self.timer >= self.duration:
                self.hide()
    
    def draw(self,text:str, surface, position):
        # Draw the dialog box on the specified surface at the given position
        if self.visible:
            text_surface = self.font.render(text, True, (255, 255, 255))  # Render the text
            text_rect = text_surface.get_rect(midbottom=position)  # Position the text rect
            pygame.draw.rect(surface, (0, 0, 0), text_rect.inflate(10, 10))  # Draw the dialog box background
            surface.blit(text_surface, text_rect.topleft)  # Draw the text on the dialog box background
     

