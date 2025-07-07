#!/usr/bin/env python3
# add_camps.py
"""
Script pour ajouter facilement des camps de réfugiés
"""

import argparse
import sys
from src.camp_manager import CampManager
from src.config import *

def add_single_camp(manager: CampManager, args):
    """Ajouter un seul camp"""
    print(f"➕ Ajout du camp '{args.name}'...")
    
    success = manager.add_camp(
        name=args.name,
        latitude=args.lat,
        longitude=args.lon,
        population=args.pop or "N/A",
        radar=args.radar,
        icon_type=args.icon
    )
    
    if success:
        # Sauvegarder automatiquement
        manager.save_to_json()
        print("💾 Données sauvegardées automatiquement")
        return True
    return False

def add_from_csv(manager: CampManager, csv_file: str):
    """Ajouter des camps depuis un fichier CSV"""
    print(f"📂 Chargement des camps depuis {csv_file}...")
    
    if manager.load_from_csv(csv_file):
        # Sauvegarder automatiquement
        manager.save_to_json()
        print("💾 Données sauvegardées automatiquement")
        return True
    return False

def interactive_mode(manager: CampManager):
    """Mode interactif pour ajouter des camps"""
    print("\n🎯 Mode interactif - Ajout de camp")
    print("=" * 40)
    
    try:
        # Informations de base
        name = input("📍 Nom du camp: ").strip()
        if not name:
            print("❌ Le nom du camp est requis")
            return False
        
        # Coordonnées
        try:
            lat = float(input("🌍 Latitude: "))
            lon = float(input("🌍 Longitude: "))
        except ValueError:
            print("❌ Coordonnées invalides")
            return False
        
        # Population (optionnel)
        pop = input("👥 Population (optionnel): ").strip()
        if not pop:
            pop = "N/A"
        
        # Type de radar
        print(f"📡 Types de radar disponibles: {', '.join(RADAR_TYPES)}")
        radar = input(f"📡 Type de radar (défaut: VH): ").strip().upper()
        if radar not in RADAR_TYPES:
            radar = "VH"
        
        # Type d'icône
        print(f"🏠 Types d'icônes disponibles:")
        for icon_type, config in ICON_CONFIG.items():
            print(f"   • {icon_type}: {config['description']}")
        
        icon = input("🏠 Type d'icône (défaut: blue): ").strip().lower()
        if icon not in ICON_CONFIG:
            icon = "blue"
        
        # Confirmation
        print(f"\n📋 Résumé:")
        print(f"   Nom: {name}")
        print(f"   Coordonnées: {lat}, {lon}")
        print(f"   Population: {pop}")
        print(f"   Radar: {radar}")
        print(f"   Icône: {icon}")
        
        confirm = input("\n✅ Confirmer l'ajout ? (o/N): ").strip().lower()
        if confirm in ['o', 'oui', 'y', 'yes']:
            success = manager.add_camp(name, lat, lon, pop, radar, icon)
            if success:
                manager.save_to_json()
                print("💾 Camp ajouté et sauvegardé !")
                return True
        else:
            print("❌ Ajout annulé")
            return False
            
    except KeyboardInterrupt:
        print("\n❌ Ajout annulé")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def list_camps_command(manager: CampManager):
    """Afficher la liste des camps"""
    manager.load_from_json()
    manager.list_camps()

def remove_camp_command(manager: CampManager, camp_name: str):
    """Supprimer un camp"""
    manager.load_from_json()
    if manager.remove_camp(camp_name):
        manager.save_to_json()
        print("💾 Données sauvegardées")

def create_template_command(manager: CampManager):
    """Créer un template CSV"""
    if manager.create_csv_template():
        print(f"📝 Vous pouvez maintenant éditer le fichier: {CAMPS_TEMPLATE_CSV}")
        print(f"📂 Puis charger les camps avec: python add_camps.py --from-csv {CAMPS_TEMPLATE_CSV}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Ajouter des camps de réfugiés à la carte",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Ajouter un camp simple
  python add_camps.py --name "Nouveau_Camp" --lat 12.345 --lon 67.890 --pop "15000"
  
  # Ajouter depuis un fichier CSV
  python add_camps.py --from-csv data/camps_template.csv
  
  # Mode interactif
  python add_camps.py --interactive
  
  # Créer un template CSV
  python add_camps.py --create-template
  
  # Lister tous les camps
  python add_camps.py --list
  
  # Supprimer un camp
  python add_camps.py --remove "Nom_Du_Camp"
        """
    )
    
    # Groupe pour l'ajout d'un camp
    camp_group = parser.add_argument_group('Ajout d\'un camp')
    camp_group.add_argument('--name', help='Nom du camp')
    camp_group.add_argument('--lat', type=float, help='Latitude')
    camp_group.add_argument('--lon', type=float, help='Longitude')
    camp_group.add_argument('--pop', help='Population (optionnel)')
    camp_group.add_argument('--radar', choices=RADAR_TYPES, default='VH', help='Type de radar')
    camp_group.add_argument('--icon', choices=list(ICON_CONFIG.keys()), default='blue', help='Type d\'icône')
    
    # Autres options
    parser.add_argument('--from-csv', help='Charger des camps depuis un fichier CSV')
    parser.add_argument('--interactive', action='store_true', help='Mode interactif')
    parser.add_argument('--create-template', action='store_true', help='Créer un template CSV')
    parser.add_argument('--list', action='store_true', help='Lister tous les camps')
    parser.add_argument('--remove', help='Supprimer un camp par son nom')
    
    args = parser.parse_args()
    
    # Créer le gestionnaire
    manager = CampManager()
    
    try:
        # Traitement des commandes
        if args.create_template:
            return 0 if create_template_command(manager) else 1
        
        elif args.list:
            list_camps_command(manager)
            return 0
        
        elif args.remove:
            remove_camp_command(manager, args.remove)
            return 0
        
        elif args.interactive:
            manager.load_from_json()
            return 0 if interactive_mode(manager) else 1
        
        elif args.from_csv:
            manager.load_from_json()
            return 0 if add_from_csv(manager, args.from_csv) else 1
        
        elif args.name and args.lat is not None and args.lon is not None:
            manager.load_from_json()
            return 0 if add_single_camp(manager, args) else 1
        
        else:
            # Aucune commande spécifiée, afficher l'aide
            parser.print_help()
            print(f"\n💡 Conseil: Utilisez --interactive pour un mode guidé")
            return 0
            
    except KeyboardInterrupt:
        print("\n⚠️ Opération annulée par l'utilisateur")
        return 1
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())