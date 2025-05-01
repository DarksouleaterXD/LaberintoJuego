import pygame
import types

class Button:
    def __init__(self, x, y, width, height, text="", color=(255, 255, 255), action=None, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)
        self.image = image

    def draw(self, screen):
        
        if self.image:
            # Centra la imagen en el botón
            image_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, image_rect)
        else:
            # Si no hay imagen, muestra el texto
            pygame.draw.rect(screen, self.color, self.rect)
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if callable(self.action):
                self.action()
