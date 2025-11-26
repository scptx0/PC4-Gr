import pygame

class Platform:
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        """Dibujar la plataforma"""
        pygame.draw.rect(screen, self.color, self.rect)
