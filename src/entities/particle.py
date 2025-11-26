import pygame
import random

class Particle:
    def __init__(self, x, y, color, vel_x_range=(-2, 2), vel_y_range=(-5, -12), gravity=0.4, size_range=(4, 8), decay_range=(3, 8), shape='square'):
        self.x = x
        self.y = y
        self.color = color
        self.shape = shape
        
        self.shape = shape
        
        # Velocidad aleatoria
        self.vel_x = random.uniform(vel_x_range[0], vel_x_range[1])
        self.vel_y = random.uniform(vel_y_range[0], vel_y_range[1])
        
        self.size = random.randint(size_range[0], size_range[1])
        self.gravity = gravity
        self.life = 255  # Alfa/Vida
        self.decay = random.randint(decay_range[0], decay_range[1])
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity  # Aplicar gravedad para que caigan eventualmente
        self.life -= self.decay
        
        # Crecer ondas con el tiempo
        if self.shape == 'wave':
            self.size += 1
        
    def draw(self, screen):
        if self.life > 0:
            if self.shape == 'wave':
                # Dibujar un arco/onda
                # Crear una superficie lo suficientemente grande para la onda
                s = pygame.Surface((self.size * 2, self.size))
                s.set_colorkey((0, 0, 0))  # Hacer negro transparente para el fondo de la superficie
                s.set_alpha(self.life)
                
                # Dibujar la onda (arco)
                rect = pygame.Rect(0, 0, self.size * 2, self.size * 2)
                pygame.draw.arc(s, self.color, rect, 0, 3.14, max(1, self.size // 5))
                
                screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))
            else:
                # Cuadrado por defecto
                s = pygame.Surface((self.size, self.size))
                s.set_alpha(self.life)
                s.fill(self.color)
                screen.blit(s, (int(self.x), int(self.y)))
            
    def is_alive(self):
        return self.life > 0
