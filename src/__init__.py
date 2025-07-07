# src/__init__.py
"""
Package pour la gestion des camps de réfugiés et la génération de cartes interactives
"""

__version__ = "1.0.0"
__author__ = "Thomas ESCOBAR"
__description__ = "Système de gestion et cartographie des camps de réfugiés"

from .camp_manager import Camp, CampManager
from .map_generator import MapGenerator
from . import config

__all__ = [
    'Camp',
    'CampManager', 
    'MapGenerator',
    'config'
]