"""
Diseño del Nivel 1-1
Sección normal de plataformas
"""

from core import Platform

def get_platforms():
    """Devolver lista de plataformas para el Nivel 1-1"""
    platforms = [
        # Plataformas del suelo x, y, ancho, alto, color
        Platform(0, 350, 200, 600, (0, 0, 0)),

        # Plataformas de nivel medio
        Platform(280, 290, 100, 40, (0, 0, 0)),
        Platform(450, 250, 80, 100, (0, 0, 0)),

        Platform(680, 300, 50, 40, (0, 0, 0)),
        
        Platform(800, 350, 200, 600, (0, 0, 0)),
    ]
    return platforms

def get_goal_position():
    """Devolver la posición de la meta (x, y, ancho, alto)"""
    return (980, 0, 40, 600)

def get_player_start():
    """Devolver posición inicial del jugador"""
    return (0, 200)

def get_hint_message():
    """Devolver mensaje de pista para este nivel"""
    return "Usa WASD para moverte y CTRL para activar tu poder."
