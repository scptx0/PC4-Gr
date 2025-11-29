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
        self.shake_duration = 0
        self.shake_timer = 100  # Intervalo aleatorio entre sacudidas (3-7 segundos)
        
        # Color de UI estable para este nivel
        self.ui_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        
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
            
        # Dibujar UI de habilidades
        self.draw_abilities(screen)
    
    def draw_hint(self, screen):
        """Dibujar mensaje de pista en la parte superior de la pantalla"""
        font = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 22)
        text = font.render(self.hint_message, True, (0, 0, 0))  # Texto negro
        text_rect = text.get_rect(center=(self.screen_width // 2, 40))
        
        screen.blit(text, text_rect)

    def draw_abilities(self, screen):
        """Dibujar indicador de habilidades en la esquina inferior derecha"""
        if not self.player:
            return
            
        # Colores
        BLACK = (0, 0, 0)
        
        # Determinar texto de habilidad
        ability_text = "NINGUNA"
        if "shoot" in self.player.abilities:
            ability_text = "DISPARO"
        
        text_str = f"HABILIDAD: {ability_text}"
        
        # Configuración de fuente
        font = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 20)
        text = font.render(text_str, True, self.ui_color)
        
        # Dimensiones y márgenes
        margin_right = 10
        margin_bottom = 10
        padding_x = 15
        padding_y = 10
        icon_size = 20
        icon_padding = 10
        
        # Calcular tamaño total
        total_width = text.get_width() + padding_x * 2
        if "shoot" in self.player.abilities:
            total_width += icon_size + icon_padding
            
        total_height = text.get_height() + padding_y * 2
        
        # Posición del fondo
        bg_rect = pygame.Rect(0, 0, total_width, total_height)
        bg_rect.bottomright = (self.screen_width - margin_right, self.screen_height - margin_bottom)
        
        # Dibujar fondo (negro semitransparente)
        s = pygame.Surface((bg_rect.width, bg_rect.height))
        s.set_alpha(230)
        s.fill(BLACK)
        screen.blit(s, bg_rect.topleft)
        
        # Dibujar borde random
        pygame.draw.rect(screen, self.ui_color, bg_rect, 2)
        
        # Dibujar Icono
        text_x = bg_rect.left + padding_x
        if "shoot" in self.player.abilities:
            # Icono de proyectil (rectángulo random)
            icon_rect = pygame.Rect(bg_rect.left + padding_x, bg_rect.centery - icon_size // 2 + 2, 
                                  icon_size, icon_size // 2)
            pygame.draw.rect(screen, self.ui_color, icon_rect)
            text_x += icon_size + icon_padding
            
        # Dibujar texto
        text_rect = text.get_rect(midleft=(text_x, bg_rect.centery))
        screen.blit(text, text_rect)
