import pygame
import random
from ..base import Level
from entities import Player, Boss, Particle
import levels.level1.level1_2_layout as level1_2_layout


class Level1_2(Level):
    """Segunda instancia del Nivel 1 - Pelea contra el jefe"""
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.platforms = level1_2_layout.get_platforms()
        player_x, player_y = level1_2_layout.get_player_start()
        self.player = Player(player_x, player_y)
        self.hint_message = level1_2_layout.get_hint_message()
        
        # Jefe
        boss_x, boss_y = level1_2_layout.get_boss_position()
        self.boss = Boss(boss_x, boss_y)
        
        # Desactivar sacudida aleatoria predeterminada para este nivel (coordinaremos con el jefe)
        self.shake_timer = 999999
        self.last_boss_frame = -1
        
        # Configuración de sacudida del jefe
        self.boss_impact_frames = [1, 35, 74, 118, 162, 206, 250]  # Lista de frames donde ocurre el "golpe"
        self.boss_shake_intensity = 30  # Intensidad de la sacudida (mayor = más fuerte)
        self.boss_shake_duration = 15   # Duración de la sacudida en frames
        
        # Partículas
        self.particles = []
        
    def update(self):
        """Actualizar nivel"""
        super().update()
        self.player.update(self.platforms, self.screen_width, self.screen_height)
        
        if self.boss.is_alive():
            self.boss.update(self.player)
            
            # Coordinar sacudida con animación del jefe
            if self.boss.using_animation:
                # Depuración: Imprimir frame actual para ayudar al usuario a encontrar el frame de impacto
                # print(f"Frame del Jefe: {self.boss.current_frame}")
                
                # Activar sacudida en frames de impacto específicos
                if self.boss.current_frame in self.boss_impact_frames and self.last_boss_frame != self.boss.current_frame:
                    self.start_shake(intensity=self.boss_shake_intensity, duration=self.boss_shake_duration)
                    self.spawn_impact_particles()
                self.last_boss_frame = self.boss.current_frame
            
            # Verificar colisiones de ataque de puño del jefe - MUERTE INSTANTÁNEA
            attack_rects = self.boss.get_all_attack_rects()
            for attack_rect in attack_rects:
                if attack_rect.colliderect(self.player.get_rect()):
                    self.player.health = 0  # Muerte instantánea
            
            # Verificar colisiones de proyectiles con el núcleo del jefe
            for projectile in self.player.projectiles[:]:
                if projectile.get_rect().colliderect(self.boss.get_rect()):
                    self.boss.take_damage(10)
                    self.boss.stun(60)  # Aturdir por 1 segundo
                    self.player.projectiles.remove(projectile)
        else:
            # Jefe derrotado
            self.completed = True
        
        # Verificar si el jugador murió
        if not self.player.is_alive():
            self.completed = False  # Activará game over
            
        # Actualizar partículas
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def spawn_impact_particles(self):
        """Generar partículas de tierra desde la parte inferior de la pantalla"""
        # Partículas grandes de tierra (pesadas, oscuras)
        for _ in range(30):
            x = random.randint(0, self.screen_width)
            y = self.screen_height
            color = (0, 0, 0)  # Tierra negra
            self.particles.append(Particle(
                x, y, color,
                size_range=(10, 20)  # Trozos de tierra más grandes
            ))
            
        # Partículas pequeñas de tierra (polvo/escombros)
        for _ in range(50):
            x = random.randint(0, self.screen_width)
            y = self.screen_height
            color = (0, 0, 0)  # Tierra negra
            self.particles.append(Particle(
                x, y, color,
                vel_x_range=(-3, 3),      # Más dispersión
                vel_y_range=(-8, -18),    # Ligeramente más rápido/variado
                gravity=0.3,
                size_range=(3, 6),        # Trozos pequeños
                decay_range=(5, 10)       # Desvanecer más rápido
            ))
    
    def draw(self, screen):
        """Dibujar nivel"""
        # Fondo
        screen.fill((255, 255, 255))  # Fondo blanco
        
        # Obtener desplazamiento de sacudida
        shake_x, shake_y = self.get_shake_offset()
        
        # Dibujar todo normalmente
        if self.boss.is_alive():
            self.boss.draw(screen)

        for platform in self.platforms:
            platform.draw(screen)
            
        if not self.boss.is_alive():
            # Mensaje de victoria
            font = pygame.font.Font(None, 72)
            text = font.render("¡VICTORIA!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text, text_rect)
        
        self.player.draw(screen)
        
        # Dibujar partículas
        for particle in self.particles:
            particle.draw(screen)
        
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
