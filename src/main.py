import pygame
import sys
from levels.level1 import Level1_1, Level1_2
from utils import save_manager

# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Secuencia de niveles
LEVEL_SEQUENCE = [Level1_1, Level1_2]

# Grupos de niveles (Capítulos)
# Nivel 1 tiene dos partes: 1.1 y 1.2
LEVEL_GROUPS = [
    [Level1_1, Level1_2],
    # Aquí iría el Nivel 2: [Level2_1, ...]
]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Meta-Puzzle Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, LEVEL_SELECT, PLAYING, TRANSITION, GAME_OVER
        self.current_level = None
        self.current_group_index = 0
        self.current_level_index_in_group = 0
        self.transition_timer = 0
        self.transition_message = ""
        
        # Cargar progreso
        self.max_unlocked_level = save_manager.load_progress()
        
    def start_level_group(self, group_index):
        """Iniciar un grupo de niveles (Capítulo)"""
        if 0 <= group_index < len(LEVEL_GROUPS):
            self.current_group_index = group_index
            self.current_level_index_in_group = 0
            self.load_current_level()
            self.state = "PLAYING"
            
    def load_current_level(self):
        """Cargar el nivel actual dentro del grupo"""
        group = LEVEL_GROUPS[self.current_group_index]
        if self.current_level_index_in_group < len(group):
            level_class = group[self.current_level_index_in_group]
            self.current_level = level_class(SCREEN_WIDTH, SCREEN_HEIGHT)
        else:
            # Grupo completado
            self.complete_level_group()

    def complete_level_group(self):
        """Manejar la finalización de un grupo de niveles"""
        # Desbloquear siguiente nivel
        next_level = self.current_group_index + 2 # +1 por índice 0, +1 para el siguiente
        save_manager.save_progress(next_level)
        self.max_unlocked_level = save_manager.load_progress()
        
        self.state = "LEVEL_SELECT"
    
    def show_transition(self, message, duration=120):
        """Mostrar pantalla de transición"""
        self.state = "TRANSITION"
        self.transition_message = message
        self.transition_timer = duration
    
    def handle_events(self):
        """Manejar eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.state == "MENU":
                    # Botón JUGAR
                    play_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
                    if play_rect.collidepoint(mouse_pos):
                        self.state = "LEVEL_SELECT"
                
                elif self.state == "LEVEL_SELECT":
                    # Botones de niveles (Grid)
                    cols = 4
                    btn_size = 80
                    gap = 20
                    
                    # Calcular inicio X para centrar
                    total_width = cols * btn_size + (cols - 1) * gap
                    start_x = (SCREEN_WIDTH - total_width) // 2
                    start_y = 250
                    
                    # Mostrar 12 niveles en el grid (3 filas de 4)
                    for i in range(12):
                        row = i // cols
                        col = i % cols
                        
                        x = start_x + col * (btn_size + gap)
                        y = start_y + row * (btn_size + gap)
                        
                        btn_rect = pygame.Rect(x, y, btn_size, btn_size)
                        
                        if btn_rect.collidepoint(mouse_pos):
                            # Solo permitir click si está desbloqueado y existe
                            if i + 1 <= self.max_unlocked_level and i < len(LEVEL_GROUPS):
                                self.start_level_group(i)
            
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        self.state = "LEVEL_SELECT"
                
                elif self.state == "LEVEL_SELECT":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                
                elif self.state == "PLAYING":
                    # Disparar con tecla CTRL
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        if self.current_level and self.current_level.player:
                            self.current_level.player.shoot()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU" # Pausa / Salir al menú
                
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:
                        # Reiniciar nivel actual dentro del grupo
                        if self.current_level:
                            self.current_level.reset()
                            self.state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "LEVEL_SELECT"
                

    
    def update(self):
        """Actualizar estado del juego"""
        if self.state == "PLAYING":
            if self.current_level:
                # Obtener estado del teclado para entrada continua
                keys = pygame.key.get_pressed()
                if self.current_level.player:
                    self.current_level.player.handle_input(keys)
                
                self.current_level.update()
                
                if self.current_level.completed:
                    # Obtener mensaje personalizado del nivel
                    msg = self.current_level.get_transition_message()
                    
                    # Avanzar al siguiente nivel dentro del grupo
                    self.current_level_index_in_group += 1
                    
                    # Mostrar transición siempre
                    self.show_transition(msg, 120)
                
                # Verificar muerte del jugador
                if hasattr(self.current_level, 'player') and not self.current_level.player.is_alive():
                    self.state = "GAME_OVER"
        
        elif self.state == "TRANSITION":
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                # Verificar si quedan niveles en el grupo
                group = LEVEL_GROUPS[self.current_group_index]
                if self.current_level_index_in_group < len(group):
                    self.load_current_level()
                    self.state = "PLAYING"
                else:
                    # Grupo completado
                    self.complete_level_group()
    
    def draw(self):
        """Dibujar juego"""
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "LEVEL_SELECT":
            self.draw_level_select()
        elif self.state == "PLAYING":
            if self.current_level:
                self.current_level.draw(self.screen)
        elif self.state == "TRANSITION":
            self.draw_transition()
        elif self.state == "GAME_OVER":
            self.draw_game_over()

        
        pygame.display.flip()
    
    def draw_menu(self):
        """Dibujar menú principal"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        
        # Título
        font_title = pygame.font.Font('assets/fonts/TurretRoad-ExtraBold.ttf', 64)
        title = font_title.render("Break the pattern", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        font_subtitle = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 36)
        
        # Botón JUGAR
        play_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
        mouse_pos = pygame.mouse.get_pos()
        
        # Hover effect
        color = (0, 0, 0) if play_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(self.screen, color, play_rect)
        
        play_text = font_subtitle.render("JUGAR", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=play_rect.center)
        self.screen.blit(play_text, play_text_rect)
        
        # Controles
        font_small = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 20)
        controls = "WASD: Mover/Saltar | CTRL: Habilidad (solo si está disponible)"
        controls_text = font_small.render(controls, True, (150, 150, 150))
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(controls_text, controls_rect)

    def draw_level_select(self):
        """Dibujar pantalla de selección de niveles"""
        self.screen.fill((20, 20, 20))  # Fondo oscuro
        
        font_title = pygame.font.Font('assets/fonts/TurretRoad-ExtraBold.ttf', 48)
        title = font_title.render("SELECCIONAR NIVEL", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        font_num = pygame.font.Font('assets/fonts/TurretRoad-ExtraBold.ttf', 32)
        
        # Configuración del Grid
        cols = 4
        btn_size = 80
        gap = 20
        
        # Calcular inicio X para centrar
        total_width = cols * btn_size + (cols - 1) * gap
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = 250
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Mostrar 12 niveles en el grid (placeholder para futuros niveles)
        for i in range(12):
            level_num = i + 1
            row = i // cols
            col = i % cols
            
            x = start_x + col * (btn_size + gap)
            y = start_y + row * (btn_size + gap)
            
            btn_rect = pygame.Rect(x, y, btn_size, btn_size)
            
            is_unlocked = level_num <= self.max_unlocked_level
            is_existing = i < len(LEVEL_GROUPS)
            
            # Lógica de colores
            if is_unlocked:
                if is_existing:
                    # Nivel desbloqueado y jugable
                    if btn_rect.collidepoint(mouse_pos):
                        color = (255, 255, 255)
                        text_color = (0, 0, 0)
                    else:
                        color = (50, 50, 50)
                        text_color = (255, 255, 255)
                    border_color = (255, 255, 255)
                else:
                    # Nivel desbloqueado pero no implementado (placeholder)
                    color = (30, 30, 30)
                    text_color = (100, 100, 100)
                    border_color = (50, 50, 50)
            else:
                # Nivel bloqueado
                color = (10, 10, 10)
                text_color = (40, 40, 40)
                border_color = (30, 30, 30)
            
            # Dibujar botón
            pygame.draw.rect(self.screen, color, btn_rect)
            pygame.draw.rect(self.screen, border_color, btn_rect, 2)
            
            # Dibujar número
            text = font_num.render(str(level_num), True, text_color)
            text_rect = text.get_rect(center=btn_rect.center)
            self.screen.blit(text, text_rect)
            
        # Volver
        font_small = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 20)
        back_text = font_small.render("ESC - Volver al Menú", True, (150, 150, 150))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
    
    def draw_transition(self):
        """Dibujar pantalla de transición"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        
        font = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 42)
        text = font.render(self.transition_message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def draw_game_over(self):
        """Dibujar pantalla de Game Over"""
        # Dibujar nivel actual en el fondo (atenuado)
        if self.current_level:
            self.current_level.draw(self.screen)
        
        # Superposición semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((255, 255, 255))
        self.screen.blit(overlay, (0, 0))
        
        # Texto de Game Over
        font_large = pygame.font.Font('assets/fonts/TurretRoad-ExtraBold.ttf', 72)
        text = font_large.render("GAME OVER", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Instrucciones
        font_small = pygame.font.Font('assets/fonts/TurretRoad-Medium.ttf', 32)
        restart_text = font_small.render("ENTER - Reintentar", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = font_small.render("ESC - Menu", True, (0, 0, 0))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(menu_text, menu_rect)
    

    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
