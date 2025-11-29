import pygame
import random


class Level:
    """Clase base para niveles"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.platforms = []
        self.player = None
        self.completed = False
        self.hint_message = ""
        self.show_hint = True
        self.hint_timer = 180  # Mostrar pista por 3 segundos
        
        # Efecto de sacudida de pantalla
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.shake_intensity = 1
        self.shake_duration = 0
        self.shake_timer = 100  # Intervalo aleatorio entre sacudidas (3-7 segundos)
        
    def reset(self):
        """Reiniciar nivel - para ser sobrescrito"""
        self.completed = False
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.shake_intensity = 1
        self.shake_duration = 0
        self.shake_timer = 100
        
    def update(self):
        """Actualizar nivel - para ser sobrescrito"""
        if self.hint_timer > 0:
            self.hint_timer -= 1
            if self.hint_timer == 0:
                self.show_hint = False
        
        # Actualizar sacudida de pantalla
        self.shake_timer -= 1
        if self.shake_timer <= 0:
            # Iniciar una nueva sacudida
            self.start_shake(intensity=8, duration=20)
            self.shake_timer = 100  # Próxima sacudida en 3-7 segundos
        
        # Aplicar efecto de sacudida
        if self.shake_duration > 0:
            self.shake_duration -= 1
            # Sacudir solo hacia abajo (Y positivo solamente, sin movimiento en X)
            intensity = int(self.shake_intensity)
            if intensity > 0:
                self.shake_offset_x = 0  # Sin sacudida horizontal
                self.shake_offset_y = random.randint(0, intensity)  # Solo hacia abajo
            else:
                self.shake_offset_x = 0
                self.shake_offset_y = 0
            # Reducir intensidad con el tiempo
            self.shake_intensity = max(0, self.shake_intensity - 0.5)
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
    
    def start_shake(self, intensity=10, duration=30):
        """Iniciar un efecto de sacudida de pantalla"""
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def get_shake_offset(self):
        """Obtener desplazamiento actual de sacudida para dibujar"""
        return (self.shake_offset_x, self.shake_offset_y)
        
    def draw(self, screen):
        """Dibujar nivel - para ser sobrescrito"""
        # Dibujar mensaje de pista
        if self.show_hint and self.hint_message:
            self.draw_hint(screen)
    
    def draw_hint(self, screen):
        """Dibujar mensaje de pista en la parte superior de la pantalla"""
        font = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 22)
        text = font.render(self.hint_message, True, (0, 0, 0))  # Texto negro
        text_rect = text.get_rect(center=(self.screen_width // 2, 40))
        
        screen.blit(text, text_rect)
