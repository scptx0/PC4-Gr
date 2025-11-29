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

def get_spikes():
    """Devolver lista de definiciones de pinchos (x, y, ancho, alto)"""
    # Ejemplo: Poner pinchos en la plataforma pequeña de la derecha (680, 300)
    # La plataforma mide 50 de ancho.
    return [
        (200, 550, 50, 60),
        (260, 550, 50, 60), 
        (320, 550, 50, 60),
        (380, 550, 50, 60),
        (440, 550, 50, 60),
        (500, 550, 50, 60),
        (560, 550, 50, 60),
        (620, 550, 50, 60),
        (680, 550, 50, 60),
        (740, 550, 50, 60)
    ]

def get_goal_position():
    """Devolver la posición de la meta (x, y, ancho, alto)"""
    return (980, 0, 40, 600)

def get_player_start():
    """Devolver posición inicial del jugador"""
    return (0, 200)

def get_hint_message():
    """Devolver mensaje de pista para este nivel"""
    return "Usa WASD para moverte y CTRL para activar tu poder."
