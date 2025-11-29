import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 37
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = 14
        self.gravity = 0.8
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.color = (0, 0, 0)  # Jugador negro
        self.projectiles = []
        self.shoot_cooldown = 0
        self.facing_direction = 1  # 1 = derecha, -1 = izquierda, 0 = centro
        self.eye_offset = 0.0  # Posición actual de los ojos (animación suave)
        self.target_eye_offset = 0.0  # Posición objetivo de los ojos
        self.eye_speed = 0.1  # Velocidad de movimiento de los ojos (0-1, mayor = más rápido)
        
        # Animación de aplastamiento y estiramiento
        self.base_width = 40
        self.base_height = 37
        self.squash_amount = 0.0  # Cantidad actual de aplastamiento/estiramiento
        self.target_squash = 0.0  # Cantidad objetivo de aplastamiento
        self.squash_speed = 0.35  # Velocidad de animación de aplastamiento
        self.squash_speed = 0.35  # Velocidad de animación de aplastamiento
        self.was_on_ground = False  # Rastrear estado anterior en el suelo
        
        # Sistema de habilidades
        self.abilities = []  # Lista de habilidades habilitadas (ej: ["shoot"])
    
    def handle_input(self, keys):
        """Manejar entrada de movimiento del jugador"""
        self.vel_x = 0
        
        # Movimiento horizontal
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_direction = -1  # Mirando a la izquierda
            self.target_eye_offset = -8.0  # Posición objetivo para los ojos
        elif keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_direction = 1  # Mirando a la derecha
            self.target_eye_offset = 8.0  # Posición objetivo para los ojos
        else:
            self.facing_direction = 0  # Mirando al centro
            self.target_eye_offset = 0.0  # Posición objetivo para los ojos
            
        # Saltar
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False
            # La animación se maneja en update() basado en vel_y
    
    def shoot(self):
        """Disparar un proyectil"""
        if "shoot" not in self.abilities:
            return False
            
        if self.shoot_cooldown <= 0:
            # Puedes ajustar el tamaño del proyectil aquí
            projectile_width = 20
            projectile_height = 10
            projectile = Projectile(self.x + self.width, self.y + self.height // 2, projectile_width, projectile_height)
            self.projectiles.append(projectile)
            self.shoot_cooldown = 20  # Frames de enfriamiento
            return True
        return False
    
    def update(self, platforms, screen_width, screen_height):
        """Actualizar posición y física del jugador"""
        # Actualizar enfriamiento
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Aplicar gravedad
        self.vel_y += self.gravity
        
        # Guardar posición anterior
        prev_x = self.x
        prev_y = self.y
        
        # Actualizar posición horizontal
        self.x += self.vel_x
        
        # Verificar colisiones horizontales
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Golpe desde el lado izquierdo
                if self.vel_x > 0:
                    self.x = platform.rect.left - self.width
                # Golpe desde el lado derecho
                elif self.vel_x < 0:
                    self.x = platform.rect.right
                player_rect.x = self.x
        
        # Actualizar posición vertical
        self.y += self.vel_y
        
        # Verificar colisiones verticales
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Aterrizar encima (cayendo)
                if self.vel_y > 0 and prev_y + self.height <= platform.rect.top + 5:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Golpear desde abajo (saltando hacia arriba)
                elif self.vel_y < 0 and prev_y >= platform.rect.bottom - 5:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
        
        # Límites de la pantalla
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width
        
        # Colisión con el suelo (fondo de la pantalla)
        if self.y + self.height >= screen_height:
            self.y = screen_height - self.height
            self.vel_y = 0
            self.on_ground = True
        
        # Actualizar proyectiles
        self.projectiles = [p for p in self.projectiles if p.update(screen_width)]
        
        # Animación suave de ojos - interpolar hacia el objetivo
        if abs(self.eye_offset - self.target_eye_offset) > 0.1:
            self.eye_offset += (self.target_eye_offset - self.eye_offset) * self.eye_speed
        else:
            self.eye_offset = self.target_eye_offset
        
        # Animación de aplastamiento y estiramiento
        
        # Lógica basada en velocidad vertical
        if self.vel_y < 0:
            # Subiendo: Estirarse
            self.target_squash = 0.6
        else:
            # Cayendo o en el suelo: Volver a la normalidad
            self.target_squash = 0.0
        
        # Animación suave de aplastamiento
        # Interpolación suave para que el cambio sea gradual ("poco a poco")
        if abs(self.squash_amount - self.target_squash) > 0.01:
            self.squash_amount += (self.target_squash - self.squash_amount) * 0.1
        else:
            self.squash_amount = self.target_squash
        
        # Guardar posición del centro inferior antes de redimensionar
        old_bottom = self.y + self.height
        old_center_x = self.x + self.width // 2
        
        # Actualizar dimensiones basadas en aplastamiento
        # El usuario pidió "estirar (solo hacia arriba)", así que mantenemos el ancho base.
        self.width = self.base_width
        self.height = int(self.base_height * (1 + self.squash_amount))
        
        # Restaurar posición basada en el nuevo tamaño (mantener los pies en el suelo)
        self.y = old_bottom - self.height
        self.x = old_center_x - self.width // 2
        
        # Actualizar estado del suelo para el siguiente frame
        self.was_on_ground = self.on_ground
    
    def draw(self, screen):
        """Dibujar al jugador"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Dibujar ojos que miran en la dirección del movimiento
        eye_color = (255, 255, 255)  # Ojos blancos en jugador negro
        
        # Dibujar ojos con desplazamiento suave (centrado para ancho de 40px)
        left_eye_x = int(self.x + 12 + self.eye_offset)  # Ajustado para ancho de 40px
        right_eye_x = int(self.x + 28 + self.eye_offset)  # Ajustado para ancho de 40px
        eye_y = int(self.y + 15)
        eye_radius = 4  # Tamaño del ojo
        
        pygame.draw.circle(screen, eye_color, (left_eye_x, eye_y), eye_radius)
        pygame.draw.circle(screen, eye_color, (right_eye_x, eye_y), eye_radius)
        
        # Dibujar proyectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
    
    def draw_health(self, screen):
        """Dibujar barra de salud"""
        bar_width = 100
        bar_height = 10
        bar_x = 10
        bar_y = 10
        
        # Fondo
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Salud
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = (0, 255, 0) if self.health > 50 else (255, 255, 0) if self.health > 25 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
    
    def take_damage(self, damage):
        """Recibir daño"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def reset(self, x, y):
        """Reiniciar estado del jugador"""
        self.x = x
        self.y = y
        self.health = self.max_health
        self.vel_x = 0
        self.vel_y = 0
        self.projectiles = []
        self.shoot_cooldown = 0
        self.facing_direction = 1
        self.squash_amount = 0.0
        self.target_squash = 0.0
        
    def is_alive(self):
        """Verificar si el jugador está vivo"""
        return self.health > 0
    
    def get_rect(self):
        """Obtener rectángulo del jugador para detección de colisiones"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Projectile:
    def __init__(self, x, y, width=10, height=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.color = (0, 0, 0)  # Proyectil negro
    
    def update(self, screen_width):
        """Actualizar posición del proyectil"""
        self.x += self.speed
        return self.x < screen_width  # Devolver False si está fuera de la pantalla
    
    def draw(self, screen):
        """Dibujar el proyectil"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """Obtener rectángulo del proyectil para detección de colisiones"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
