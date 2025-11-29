import pygame
import random
import math
import os
import glob

class Boss:
    # Constantes de tamaño visual
    VISUAL_WIDTH = 950
    VISUAL_HEIGHT = 475
    
    # Constantes de posición visual
    VISUAL_X = 250
    VISUAL_Y = 60

    # Constantes de hitbox (Ajustables)
    HITBOX_WIDTH = 300
    HITBOX_HEIGHT = 250
    HITBOX_OFFSET_Y = -20

    # Constantes de hitbox de golpe fatal
    KILL_HITBOX_WIDTH = 100
    KILL_HITBOX_HEIGHT = 300
    KILL_HITBOX_OFFSET_X = -325
    KILL_HITBOX_OFFSET_Y = 45

    def __init__(self, x, y):
        # Cargar frames de animación del jefe
        self.x = x
        self.y = y
        
        # Intentar cargar frames de animación
        self.animation_frames = []
        self.using_animation = False
        
        try:
            # Obtener ruta a assets/images/animation_frames desde src/entities/
            entities_dir = os.path.dirname(__file__)
            src_dir = os.path.dirname(entities_dir)
            project_root = os.path.dirname(src_dir)
            frames_folder = os.path.join(project_root, 'assets', 'images', 'animation_frames')
            frame_files = sorted(glob.glob(os.path.join(frames_folder, 'frame_*.png')))
            
            if frame_files:
                print(f"Cargando {len(frame_files)} frames de animación...")
                for frame_file in frame_files:
                    frame = pygame.image.load(frame_file).convert_alpha()
                    # Escalar frames a tamaño más grande (más ancho)
                    scaled_frame = pygame.transform.scale(frame, (self.VISUAL_WIDTH, self.VISUAL_HEIGHT))
                    self.animation_frames.append(scaled_frame)
                
                self.using_animation = True
                self.current_frame = 0
                self.frame_delay = 2  # Cambiar frame cada 2 ticks del juego
                self.frame_counter = 0
                self.image_width = 400
                self.image_height = 300
                print(f"Se cargaron exitosamente {len(self.animation_frames)} frames")
        except Exception as e:
            print(f"No se pudieron cargar los frames de animación: {e}")
            self.using_animation = False
        
        # Usar imagen estática si la animación no está disponible
        if not self.using_animation:
            try:
                # Obtener ruta a assets/images/boss.png desde src/entities/
                entities_dir = os.path.dirname(__file__)
                src_dir = os.path.dirname(entities_dir)
                project_root = os.path.dirname(src_dir)
                boss_image_path = os.path.join(project_root, 'assets', 'images', 'boss.png')
                self.original_image = pygame.image.load(boss_image_path).convert_alpha()
                self.image_width = 150
                self.image_height = 150
                self.image = pygame.transform.scale(self.original_image, (self.image_width, self.image_height))
                self.using_image = True
            except:
                self.using_image = False
                self.image_width = 80
                self.image_height = 80
        
        self.health = 200
        self.max_health = 200
        self.stun_duration = 0
        
        # Animación de flotación
        self.float_offset = 0
        self.float_speed = 0.05
        
        # Frames donde el hitbox de muerte está activo
        self.kill_frames = [35, 118, 206]
        
    def update(self, player):
        """Actualizar IA y comportamiento del jefe"""
        # Actualizar aturdimiento
        if self.stun_duration > 0:
            self.stun_duration -= 1
            return
        
        # Animación de flotación
        self.float_offset += self.float_speed
        
        # Actualizar frame de animación
        if self.using_animation:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
    
    def take_damage(self, damage):
        """Recibir daño de un proyectil"""
        self.health -= damage
        if self.health < 1:
            self.health = 1
    
    def stun(self, duration=60):
        """Aturdir al jefe"""
        self.stun_duration = duration
    
    def is_alive(self):
        """Verificar si el jefe está vivo"""
        return self.health > 0
    
    def draw(self, screen):
        """Dibujar al jefe"""
        # Calcular posición de flotación usando la posición visual base
        float_y = self.VISUAL_Y + math.sin(self.float_offset) * 10
        
        if self.using_animation:
            # Dibujar frame de animación actual
            current_image = self.animation_frames[self.current_frame]
            
            # (Efecto de parpadeo eliminado)
            
            # Dibujar en posición visual absoluta
            image_x = self.VISUAL_X
            image_y = float_y
            screen.blit(current_image, (image_x, image_y))
            
        elif hasattr(self, 'using_image') and self.using_image:
            # Dibujar imagen estática
            boss_image = self.image
            
            # (Efecto de parpadeo eliminado)
            
            image_x = self.VISUAL_X
            image_y = float_y
            screen.blit(boss_image, (image_x, image_y))
        else:
            # Dibujo de respaldo (círculo simple)
            core_center_x = int(self.x + self.image_width // 2)
            core_center_y = int(float_y + self.image_height // 2)
            pygame.draw.circle(screen, (0, 0, 0), (core_center_x, core_center_y), self.image_width // 2)
        
        # Dibujar hitbox
        # hitbox_rect = self.get_rect()
        # pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)
        
        # Dibujar hitbox de muerte (debug)
        # kill_rects = self.get_all_attack_rects()
        # for r in kill_rects:
        #     pygame.draw.rect(screen, (255, 0, 255), r, 2)

        # Dibujar barra de salud
        self.draw_health(screen)
    
    def draw_health(self, screen):
        """Dibujar barra de salud del jefe"""
        screen_width = screen.get_width()
        bar_width = 400
        bar_height = 10
        bar_x = (screen_width - bar_width) // 2
        bar_y = 50
        border_width = 2

        # Dibujar texto "Jefe"
        font = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 24)
        text = font.render("Jefe", True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, bar_y - 15))
        screen.blit(text, text_rect)
        
        # Fondo
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
        
        # Salud (con efecto de gradiente)
        if self.max_health > 0:
            health_width = int((self.health / self.max_health) * bar_width)
        else:
            health_width = 0
            
        # Barra de vida negra
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Borde
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_width)
    
    def get_rect(self):
        """Obtener rectángulo del núcleo del jefe para colisiones"""
        center_x = self.VISUAL_X + self.VISUAL_WIDTH // 2
        center_y = self.VISUAL_Y + self.VISUAL_HEIGHT // 2
        
        hitbox_center_y = center_y + self.HITBOX_OFFSET_Y
        
        rect = pygame.Rect(0, 0, self.HITBOX_WIDTH, self.HITBOX_HEIGHT)
        rect.center = (center_x, hitbox_center_y)
        return rect
    
    def get_all_attack_rects(self):
        """Obtener todos los rectángulos de ataque"""
        if self.using_animation and self.current_frame in self.kill_frames:
            center_x = self.VISUAL_X + self.VISUAL_WIDTH // 2
            center_y = self.VISUAL_Y + self.VISUAL_HEIGHT // 2
            
            kill_center_x = center_x + self.KILL_HITBOX_OFFSET_X
            kill_center_y = center_y + self.KILL_HITBOX_OFFSET_Y
            
            rect = pygame.Rect(0, 0, self.KILL_HITBOX_WIDTH, self.KILL_HITBOX_HEIGHT)
            rect.center = (kill_center_x, kill_center_y)
            return [rect]
            
        return []

