import pygame
import types

class Button:
    def __init__(self, x, y, width, height, text="", color=(255, 255, 255), action=None, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.image = image

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            # (Render text here if needed)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
                return True
        return False
