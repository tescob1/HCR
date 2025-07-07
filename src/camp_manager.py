# src/camp_manager.py
"""
Gestionnaire des camps de réfugiés
Gère l'ajout, la suppression, la sauvegarde et le chargement des camps
"""

import json
import csv
from typing import List, Dict, Optional
from .config import *

class Camp:
    """Représente un camp de réfugiés"""
    
    def __init__(self, name: str, latitude: float, longitude: float, 
                 population: str = "N/A", radar: str = "VH", icon_type: str = "blue"):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.population = population
        self.radar = radar
        self.icon_type = icon_type
        
        # Validation
        self._validate()
    
    def _validate(self):
        """Valider les données du camp"""
        if not self.name or not self.name.strip():
            raise ValueError("Le nom du camp est requis")
        
        if not isinstance(self.latitude, (int, float)) or not isinstance(self.longitude, (int, float)):
            raise ValueError(f"Coordonnées invalides pour {self.name}")
        
        if self.radar not in RADAR_TYPES:
            raise ValueError(f"Type de radar invalide: {self.radar}. Valeurs acceptées: {RADAR_TYPES}")
        
        if self.icon_type not in ICON_CONFIG:
            raise ValueError(f"Type d'icône invalide: {self.icon_type}. Valeurs acceptées: {list(ICON_CONFIG.keys())}")
    
    def to_dict(self) -> Dict:
        """Convertir le camp en dictionnaire"""
        return {
            "name": self.name,
            "coords": [self.latitude, self.longitude],
            "population": self.population,
            "radar": self.radar,
            "icon": {
                "path": get_icon_path(self.icon_type),
                "size": ICON_CONFIG[self.icon_type]["size"]
            },
            "icon_type": self.icon_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Camp':
        """Créer un camp à partir d'un dictionnaire"""
        return cls(
            name=data["name"],
            latitude=data["coords"][0],
            longitude=data["coords"][1],
            population=data.get("population", "N/A"),
            radar=data.get("radar", "VH"),
            icon_type=data.get("icon_type", "blue")
        )
    
    def __str__(self) -> str:
        return f"Camp({self.name}, {self.latitude}, {self.longitude})"


class CampManager:
    """Gestionnaire principal des camps"""
    
    def __init__(self):
        self.camps: List[Camp] = []
        ensure_directories()
    
    def add_camp(self, name: str, latitude: float, longitude: float, 
                 population: str = "N/A", radar: str = "VH", icon_type: str = "blue") -> bool:
        """Ajouter un nouveau camp"""
        try:
            # Vérifier si le camp existe déjà
            if self.get_camp_by_name(name):
                print(f"⚠️ Le camp '{name}' existe déjà. Utilisez update_camp() pour le modifier.")
                return False
            
            camp = Camp(name, latitude, longitude, population, radar, icon_type)
            self.camps.append(camp)
            print(MESSAGES["success"]["camp_added"].format(name=name))
            return True
            
        except ValueError as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False
    
    def get_camp_by_name(self, name: str) -> Optional[Camp]:
        """Trouver un camp par son nom"""
        for camp in self.camps:
            if camp.name == name:
                return camp
        return None
    
    def update_camp(self, name: str, **kwargs) -> bool:
        """Mettre à jour un camp existant"""
        camp = self.get_camp_by_name(name)
        if not camp:
            print(f"❌ Camp '{name}' introuvable")
            return False
        
        try:
            for key, value in kwargs.items():
                if hasattr(camp, key):
                    setattr(camp, key, value)
            
            camp._validate()  # Revalider après modification
            print(f"✅ Camp '{name}' mis à jour")
            return True
            
        except ValueError as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False
    
    def remove_camp(self, name: str) -> bool:
        """Supprimer un camp"""
        camp = self.get_camp_by_name(name)
        if camp:
            self.camps.remove(camp)
            print(MESSAGES["info"]["camp_removed"].format(name=name))
            return True
        else:
            print(f"❌ Camp '{name}' introuvable")
            return False
    
    def list_camps(self) -> None:
        """Afficher la liste des camps"""
        if not self.camps:
            print(MESSAGES["info"]["no_camps"])
            return
        
        print("\n📍 Liste des camps :")
        print("-" * 80)
        print(f"{'#':<3} {'Nom':<20} {'Population':<15} {'Radar':<6} {'Icône':<6} {'Coordonnées':<20}")
        print("-" * 80)
        
        for i, camp in enumerate(self.camps, 1):
            coords = f"{camp.latitude:.3f}, {camp.longitude:.3f}"
            print(f"{i:<3} {camp.name:<20} {camp.population:<15} {camp.radar:<6} {camp.icon_type:<6} {coords:<20}")
    
    def get_camps_count(self) -> int:
        """Retourner le nombre de camps"""
        return len(self.camps)
    
    def get_camps_by_icon_type(self, icon_type: str) -> List[Camp]:
        """Retourner les camps d'un type d'icône donné"""
        return [camp for camp in self.camps if camp.icon_type == icon_type]
    
    def save_to_json(self, filename: str = None) -> bool:
        """Sauvegarder les camps au format JSON"""
        if filename is None:
            filename = CAMPS_JSON_FILE
        
        try:
            data = {
                "camps": [camp.to_dict() for camp in self.camps],
                "metadata": {
                    "total_camps": len(self.camps),
                    "version": "1.0"
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            print(MESSAGES["success"]["data_saved"].format(file=filename))
            return True
            
        except Exception as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False
    
    def load_from_json(self, filename: str = None) -> bool:
        """Charger les camps depuis un fichier JSON"""
        if filename is None:
            filename = CAMPS_JSON_FILE
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.camps = []
            camps_data = data.get("camps", [])
            
            for camp_data in camps_data:
                camp = Camp.from_dict(camp_data)
                self.camps.append(camp)
            
            count = len(self.camps)
            print(MESSAGES["success"]["camps_loaded"].format(count=count, file=filename))
            return True
            
        except FileNotFoundError:
            print(MESSAGES["error"]["file_not_found"].format(file=filename))
            return False
        except Exception as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False
    
    def load_from_csv(self, filename: str) -> bool:
        """Charger les camps depuis un fichier CSV"""
        try:
            added_count = 0
            
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Nettoyer les données
                    name = row.get('name', '').strip()
                    if not name:
                        continue
                    
                    try:
                        latitude = float(row.get('latitude', 0))
                        longitude = float(row.get('longitude', 0))
                        population = row.get('population', 'N/A').strip()
                        radar = row.get('radar', 'VH').strip()
                        icon_type = row.get('icon_type', 'blue').strip()
                        
                        if self.add_camp(name, latitude, longitude, population, radar, icon_type):
                            added_count += 1
                            
                    except (ValueError, TypeError) as e:
                        print(f"⚠️ Erreur ligne {name}: {e}")
                        continue
            
            print(f"✅ {added_count} camps ajoutés depuis {filename}")
            return True
            
        except FileNotFoundError:
            print(MESSAGES["error"]["file_not_found"].format(file=filename))
            return False
        except Exception as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False
    
    def create_csv_template(self, filename: str = None) -> bool:
        """Créer un fichier CSV template"""
        if filename is None:
            filename = CAMPS_TEMPLATE_CSV
        
        try:
            headers = ['name', 'latitude', 'longitude', 'population', 'radar', 'icon_type']
            example_data = [
                ['Exemple_Camp_1', '10.123456', '20.654321', '50000', 'VH', 'blue'],
                ['Exemple_Camp_2', '15.987654', '25.123456', 'N/A', 'VV', 'green'],
                ['Exemple_Camp_3', '5.555555', '15.111111', '25000', 'VH', 'grey']
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(example_data)
            
            print(f"✅ Template CSV créé : {filename}")
            print("📝 Éditez ce fichier et utilisez load_from_csv() pour charger vos camps")
            return True
            
        except Exception as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False