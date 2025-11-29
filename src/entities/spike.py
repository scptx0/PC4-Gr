import pygame

class Spike:
    def __init__(self, x, y, width, height, duration=60, damage=10, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.duration = duration
        self.damage = damage
        self.color = color
        self.life = duration
        
    def update(self):
        if self.duration != -1:
            self.life -= 1
        
    def draw(self, screen):
        if self.life > 0 or self.duration == -1:
            # Draw a triangle for the spike
            points = [
                (self.rect.left, self.rect.bottom),
                (self.rect.centerx, self.rect.top),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(screen, self.color, points)
            # Dibujar hitbox para debug
            # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
            
    def get_rect(self):
        return self.rect
        
    def is_alive(self):
        return self.life > 0 or self.duration == -1
