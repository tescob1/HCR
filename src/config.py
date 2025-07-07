# src/config.py
"""
Configuration centralisée pour le projet des camps de réfugiés
"""

import os

# ==================== CHEMINS DE FICHIERS ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Fichiers de données
CAMPS_JSON_FILE = os.path.join(DATA_DIR, "camps.json")
CAMPS_TEMPLATE_CSV = os.path.join(DATA_DIR, "camps_template.csv")

# Dossiers des assets
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
IMG_TIF_DIR = os.path.join(ASSETS_DIR, "img_TIF")
TIF_DIR = os.path.join(ASSETS_DIR, "TIF")
RESULTS_DIR = os.path.join(ASSETS_DIR, "results")  # Nouveau dossier pour les images de résultats

# Fichier de sortie
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "carte_camps.html")

# ==================== CONFIGURATION DE LA CARTE ====================
MAP_CONFIG = {
    "center_location": [0, 20],  # Centré sur l'Afrique
    "zoom_start": 4,
    "popup_max_width": 250
}

# ==================== ICÔNES ====================
ICON_CONFIG = {
    "blue": {
        "path": os.path.join(ICONS_DIR, "blue_house.png"),
        "size": 30,
        "description": "Site mapping data"
    },
    "green": {
        "path": os.path.join(ICONS_DIR, "green_house.png"),
        "size": 30,
        "description": "OpenStreetMap data"
    },
    "grey": {
        "path": os.path.join(ICONS_DIR, "grey_house.png"),
        "size": 30,
        "description": "No data"
    }
}

# ==================== TYPES DE RADAR ====================
RADAR_TYPES = ["VH", "VV"]

# ==================== STYLES CSS ====================
POPUP_STYLE = {
    "font_family": "Arial",
    "text_align": "left",
    "padding": "10px",
    "title_color": "#2C3E50",
    "text_color": "#2C3E50",
    "font_size": "14px"
}

LEGEND_STYLE = {
    "position": "fixed",
    "bottom": "10px",
    "left": "10px",
    "width": "250px",
    "height": "200px",
    "background_color": "white",
    "border": "2px solid grey",
    "z_index": "9999",
    "font_size": "14px",
    "padding": "10px"
}

# ==================== SOURCES DE DONNÉES ====================
DATA_SOURCES = {
    "unhcr": "https://im.unhcr.org/apps/sitemapping/#/",
    "copernicus": "https://browser.dataspace.copernicus.eu/"
}

# ==================== VALIDATION ====================
REQUIRED_FIELDS = ["name", "latitude", "longitude"]
OPTIONAL_FIELDS = ["population", "radar", "icon_type"]

# ==================== MESSAGES ====================
MESSAGES = {
    "success": {
        "camp_added": "✅ Camp '{name}' ajouté avec succès !",
        "camps_loaded": "✅ {count} camps chargés depuis {file}",
        "map_generated": "✅ Carte générée : {file}",
        "data_saved": "✅ Données sauvegardées : {file}"
    },
    "error": {
        "file_not_found": "❌ Fichier introuvable : {file}",
        "invalid_coordinates": "❌ Coordonnées invalides pour {name}",
        "missing_field": "❌ Champ manquant : {field}",
        "general_error": "❌ Erreur : {error}"
    },
    "info": {
        "no_camps": "ℹ️ Aucun camp enregistré",
        "camp_removed": "✅ Camp '{name}' supprimé"
    }
}

# ==================== FONCTIONS UTILITAIRES ====================
def ensure_directories():
    """Créer les dossiers nécessaires s'ils n'existent pas"""
    directories = [DATA_DIR, ASSETS_DIR, OUTPUT_DIR, ICONS_DIR, IMG_TIF_DIR, TIF_DIR, RESULTS_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_icon_path(icon_type: str) -> str:
    """Retourner le chemin relatif de l'icône pour la carte HTML"""
    return f"assets/icons/{icon_type}_house.png"

def get_gif_path(camp_name: str) -> str:
    """Retourner le chemin relatif du GIF pour la carte HTML"""
    return f"assets/img_TIF/{camp_name}.gif"

def get_tif_path(camp_name: str, radar: str) -> str:
    """Retourner le chemin relatif du fichier TIF pour la carte HTML"""
    return f"assets/TIF/FBRcollectionMonthly{radar}_{camp_name}.tif"