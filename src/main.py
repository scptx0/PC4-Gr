import pygame
import sys
from levels.level1 import Level1_1, Level1_2

# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Meta-Puzzle Platformer - Nivel 1")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, PLAYING, TRANSITION, GAME_OVER, WIN
        self.current_level = None
        self.level_index = 0
        self.transition_timer = 0
        self.transition_message = ""
        
    def start_level(self, level_index):
        """Iniciar un nivel específico"""
        self.level_index = level_index
        
        if level_index == 0:
            self.current_level = Level1_1(SCREEN_WIDTH, SCREEN_HEIGHT)
        elif level_index == 1:
            self.current_level = Level1_2(SCREEN_WIDTH, SCREEN_HEIGHT)
        else:
            self.state = "WIN"
            return
        
        self.state = "PLAYING"
    
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
            
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        self.start_level(0)
                
                elif self.state == "PLAYING":
                    # Disparar con tecla CTRL
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        if self.current_level and self.current_level.player:
                            self.current_level.player.shoot()
                
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:
                        self.start_level(self.level_index)  # Reiniciar nivel actual
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                
                elif self.state == "WIN":
                    if event.key == pygame.K_RETURN:
                        self.state = "MENU"
    
    def update(self):
        """Actualizar estado del juego"""
        if self.state == "PLAYING":
            if self.current_level:
                # Obtener estado del teclado para entrada continua
                keys = pygame.key.get_pressed()
                if self.current_level.player:
                    self.current_level.player.handle_input(keys)
                
                self.current_level.update()
                
                # Verificar finalización del nivel
                if self.current_level.completed:
                    if isinstance(self.current_level, Level1_1):
                        self.show_transition("Si, un jefe en el nivel 1", 120)
                    elif isinstance(self.current_level, Level1_2):
                        self.state = "WIN"
                
                # Verificar muerte del jugador
                if hasattr(self.current_level, 'player') and not self.current_level.player.is_alive():
                    self.state = "GAME_OVER"
        
        elif self.state == "TRANSITION":
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.start_level(self.level_index + 1)
    
    def draw(self):
        """Dibujar juego"""
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "PLAYING":
            if self.current_level:
                self.current_level.draw(self.screen)
        elif self.state == "TRANSITION":
            self.draw_transition()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
        elif self.state == "WIN":
            self.draw_win()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Dibujar menú principal"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        
        # Título
        font_title = pygame.font.Font(None, 64)
        title = font_title.render("Meta-Puzzle Platformer", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        font_subtitle = pygame.font.Font(None, 36)
        subtitle = font_subtitle.render("Nivel 1: El Jefe Gigante", True, (0, 0, 0))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instrucciones
        font_text = pygame.font.Font(None, 28)
        instructions = [
            "Presiona ENTER para comenzar",
            "",
            "Controles:",
            "Flechas o WASD - Mover",
            "Espacio/W/Flecha Arriba - Saltar",
            "CTRL - Disparar",
        ]
        
        y = 300
        for line in instructions:
            text = font_text.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 35
    
    def draw_transition(self):
        """Dibujar pantalla de transición"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        
        font = pygame.font.Font(None, 48)
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
        font_large = pygame.font.Font(None, 72)
        text = font_large.render("GAME OVER", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Instrucciones
        font_small = pygame.font.Font(None, 32)
        restart_text = font_small.render("ENTER - Reintentar", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = font_small.render("ESC - Menú", True, (0, 0, 0))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_win(self):
        """Dibujar pantalla de victoria"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        
        # Texto de victoria
        font_large = pygame.font.Font(None, 72)
        text = font_large.render("¡NIVEL 1 COMPLETADO!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Mensaje
        font_medium = pygame.font.Font(None, 36)
        msg = font_medium.render("Has derrotado al jefe gigante", True, (0, 0, 0))
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(msg, msg_rect)
        
        # Instrucciones
        font_small = pygame.font.Font(None, 28)
        continue_text = font_small.render("ENTER - Volver al menú", True, (0, 0, 0))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(continue_text, continue_rect)
    
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
