import json
import os

SAVE_FILE = "save_data.json"

def load_progress():
    """Cargar el nivel máximo desbloqueado"""
    if not os.path.exists(SAVE_FILE):
        return 1
    
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("max_unlocked_level", 1)
    except:
        return 1

def save_progress(level):
    """Guardar el progreso si el nivel completado es mayor al actual"""
    current_max = load_progress()
    
    if level > current_max:
        data = {"max_unlocked_level": level}
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f)
            return True
        except:
            return False
    return False
