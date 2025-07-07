#!/usr/bin/env python3
# main.py
"""
Script principal pour générer la carte des camps de réfugiés
"""

import sys
import os
from src.camp_manager import CampManager
from src.map_generator import MapGenerator
from src.config import *

def load_existing_camps(manager: CampManager):
    """Charger les camps existants depuis votre code original"""
    existing_camps = [
    ]
    
    print("🔄 Chargement des camps existants...")
    for camp_data in existing_camps:
        manager.add_camp(
            name=camp_data["name"],
            latitude=camp_data["coords"][0],
            longitude=camp_data["coords"][1],
            population=camp_data["population"],
            radar=camp_data["radar"],
            icon_type=camp_data["icon_type"]
        )

def main():
    """Fonction principale"""
    print("🏕️ Générateur de Carte des Camps de Réfugiés")
    print("=" * 50)
    
    # Créer le gestionnaire de camps
    manager = CampManager()
    
    # Essayer de charger depuis le fichier JSON, sinon charger les camps existants
    if not manager.load_from_json():
        print("📂 Aucun fichier de données trouvé, chargement des camps par défaut...")
        load_existing_camps(manager)
        # Sauvegarder pour la prochaine fois
        manager.save_to_json()
    
    # Afficher les statistiques
    print(f"\n📊 Statistiques:")
    print(f"   • Total des camps: {manager.get_camps_count()}")
    for icon_type in ICON_CONFIG.keys():
        count = len(manager.get_camps_by_icon_type(icon_type))
        if count > 0:
            description = ICON_CONFIG[icon_type]['description']
            print(f"   • {description}: {count}")
    
    # Créer le générateur de carte
    generator = MapGenerator(manager)
    
    # Générer la carte
    print(f"\n🗺️ Génération de la carte...")
    if generator.generate_map():
        print(f"✅ Carte générée avec succès !")
        print(f"📂 Fichier: {OUTPUT_HTML}")
        print(f"🌐 Ouvrez le fichier dans votre navigateur pour voir la carte")
    else:
        print("❌ Erreur lors de la génération de la carte")
        return 1
    
    # Options supplémentaires
    print(f"\n💡 Pour ajouter de nouveaux camps:")
    print(f"   python add_camps.py --name 'Nouveau_Camp' --lat 12.345 --lon 67.890")
    print(f"   python add_camps.py --from-csv data/camps_template.csv")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️ Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)