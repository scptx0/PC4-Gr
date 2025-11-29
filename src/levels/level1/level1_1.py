import pygame
import random
from ..base import Level
from entities import Player, Spike
import levels.level1.level1_1_layout as level1_1_layout


class Level1_1(Level):
    """Primera instancia del Nivel 1 - Plataformero normal"""
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.platforms = level1_1_layout.get_platforms()
        player_x, player_y = level1_1_layout.get_player_start()
        self.player = Player(player_x, player_y)
        self.player.abilities = ["shoot"]  # Habilitar disparo
        self.hint_message = level1_1_layout.get_hint_message()
        
        # Meta
        goal_data = level1_1_layout.get_goal_position()
        self.goal = pygame.Rect(goal_data[0], goal_data[1], goal_data[2], goal_data[3])
        
        # Pinchos estáticos
        self.spikes = []
        spike_data = level1_1_layout.get_spikes()
        for s in spike_data:
            # x, y, width, height
            self.spikes.append(Spike(s[0], s[1], s[2], s[3], duration=-1))
        
        # Configuración de sacudida
        self.shake_interval_min = 60  # Frames mínimos entre sacudidas (5 segundos)
        self.shake_interval_max = 100  # Frames máximos entre sacudidas (10 segundos)
        self.shake_timer = random.randint(self.shake_interval_min, self.shake_interval_max)
        
    def update(self):
        """Actualizar nivel"""
        super().update()
        self.player.update(self.platforms, self.screen_width, self.screen_height)
        
        # Verificar si el jugador alcanzó la meta
        if self.player.get_rect().colliderect(self.goal):
            self.completed = True
            
        # Actualizar pinchos
        for spike in self.spikes:
            spike.update()
            if spike.get_rect().colliderect(self.player.get_rect()):
                self.player.take_damage(spike.damage)
        
        # Reiniciar temporizador de sacudida para la siguiente sacudida (específico del nivel)
        if self.shake_timer <= 0:
            self.shake_timer = random.randint(self.shake_interval_min, self.shake_interval_max)
    
    def draw(self, screen):
        """Dibujar nivel"""
        # Fondo
        screen.fill((255, 255, 255))  # Fondo blanco
        
        # Obtener desplazamiento de sacudida
        shake_x, shake_y = self.get_shake_offset()
        
        # Dibujar todo normalmente
        for platform in self.platforms:
            platform.draw(screen)
        
        self.player.draw(screen)
        
        # Dibujar pinchos
        for spike in self.spikes:
            spike.draw(screen)
        
        # Aplicar sacudida desplazando todo el contenido de la pantalla
        if shake_x != 0 or shake_y != 0:
            # Copiar pantalla actual
            temp = screen.copy()
            # Llenar con blanco
            screen.fill((255, 255, 255))
            # Dibujar desplazado
            screen.blit(temp, (shake_x, shake_y))
        
        # Pista (sin sacudida)
        super().draw(screen)
