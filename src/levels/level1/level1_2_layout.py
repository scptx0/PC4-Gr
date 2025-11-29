"""
Diseño del Nivel 1-2
Arena de pelea contra el jefe
"""

from core import Platform

def get_platforms():
    """Devolver lista de plataformas para el Nivel 1-2 (arena del jefe)"""
    platforms = [
        # Suelo
        Platform(0, 550, 1000, 50, (0, 0, 0)),

        Platform(120, 460, 100, 30, (0, 0, 0)),
        Platform(260, 390, 60, 30, (0, 0, 0)),
        Platform(80, 320, 80, 30, (0, 0, 0)),
        Platform(360, 300, 70, 20, (0, 0, 0)),
        Platform (240, 210, 60, 30, (0, 0, 0))

    ]
    return platforms

def get_boss_position():
    """Devolver posición inicial del jefe (centrado)"""
    # El ancho de la pantalla es 1000, el ancho del jefe es 500, así que (1000-500)/2 = 250 para el centro
    return (320, 0)

def get_player_start():
    """Devolver posición inicial del jugador"""
    return (50, 500)

def get_hint_message():
    """Devolver mensaje de pista para este nivel"""
    return "El jefe solo puede atacar desde arriba. ¡Pasa por debajo de sus piernas! Usa CTRL para disparar y aturdirlo."
