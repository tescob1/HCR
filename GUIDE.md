# 🏕️ Tutoriel Complet - Gestion des Camps de Réfugiés

Guide exhaustif pour gérer votre système de cartographie des camps de réfugiés.

---

## 📋 Table des Matières

1. [Installation et Configuration](#-installation-et-configuration)
2. [Gestion des Camps](#-gestion-des-camps)
3. [Génération de Cartes](#-génération-de-cartes)
4. [Gestion des Assets](#-gestion-des-assets)
5. [Commandes Avancées](#-commandes-avancées)
6. [Dépannage](#-dépannage)
7. [Structure des Fichiers](#-structure-des-fichiers)

---

## 🛠️ Installation et Configuration

### Installation initiale
```bash
# Aller dans le dossier du projet
cd refugee_camps_map

# Installer les dépendances de base
pip install folium pandas

# Vérifier que Python fonctionne
python --version
```

### Structure des dossiers nécessaires
```
refugee_camps_map/
├── 📁 data/
├── 📁 src/
├── 📁 assets/
│   ├── 📁 icons/
│   ├── 📁 img_TIF/           # GIFs des camps
│   ├── 📁 TIF/               # Fichiers .tif téléchargeables
│   └── 📁 results/           # Images de résultats
├── 📁 output/
├── main.py
├── add_camps.py
└── requirements.txt
```

---

## 🏕️ Gestion des Camps

### 1. Ajouter des Camps

#### **Ajout d'un camp simple**
```bash
python add_camps.py --name "Nouveau_Camp" --lat 12.345 --lon 67.890 --pop "15000"
```

**Paramètres obligatoires :**
- `--name` : Nom du camp (sans espaces, utilisez des _ )
- `--lat` : Latitude (format décimal : 12.345678)
- `--lon` : Longitude (format décimal : -5.123456)

**Paramètres optionnels :**
- `--pop` : Population (ex: "15000" ou "N/A")
- `--radar` : Type radar VH ou VV (défaut: VH)
- `--icon` : Type d'icône blue/green/grey (défaut: blue)

#### **Exemples concrets**
```bash
# Camp basique
python add_camps.py --name "Mbera" --lat 15.833333 --lon -5.800000

# Camp complet
python add_camps.py --name "Bidibidi" --lat 3.478382 --lon 31.373434 --pop "197535" --radar "VH" --icon "blue"

# Camp sans données de population
python add_camps.py --name "Camp_Test" --lat 10.123 --lon 20.456 --pop "N/A" --icon "grey"
```

#### **Mode interactif (plus facile)**
```bash
python add_camps.py --interactive
```
Le système vous demandera chaque information une par une.

#### **Ajout en masse via CSV**
```bash
# 1. Créer un template CSV
python add_camps.py --create-template

# 2. Éditer le fichier data/camps_template.csv avec Excel/LibreOffice
# 3. Charger tous les camps d'un coup
python add_camps.py --from-csv data/camps_template.csv
```

**Format du CSV :**
```csv
name,latitude,longitude,population,radar,icon_type
Mbera,15.833333,-5.800000,100807,VH,blue
Bidibidi,3.478382,31.373434,197535,VH,blue
Kyangwali,1.179656,30.763555,133265,VH,blue
```

### 2. Consulter les Camps

#### **Voir tous les camps enregistrés**
```bash
python add_camps.py --list
```

#### **Compter les camps**
```bash
python -c "
from src.camp_manager import CampManager
m = CampManager()
m.load_from_json()
print(f'Nombre de camps: {len(m.camps)}')
"
```

### 3. Modifier des Camps

#### **Supprimer un camp**
```bash
python add_camps.py --remove "Nom_Du_Camp"
```

#### **Modifier un camp** 
Il n'y a pas de commande directe, il faut :
1. Supprimer l'ancien : `python add_camps.py --remove "Ancien_Nom"`
2. Recréer avec les bonnes infos : `python add_camps.py --name "Nouveau_Nom" --lat X --lon Y`

### 4. Types de Données

#### **Types d'icônes**
- **`blue`** : Site mapping data (données de cartographie) - BLEU
- **`green`** : OpenStreetMap data (données OpenStreetMap) - VERT  
- **`grey`** : No data (pas de données disponibles) - GRIS

#### **Types de radar**
- **`VH`** : Vertical-Horizontal (défaut)
- **`VV`** : Vertical-Vertical

---

## 🗺️ Génération de Cartes

### 1. Génération de Base

#### **Générer la carte principale**
```bash
python main.py
```
Génère le fichier `output/carte_camps.html`

### 2. Personnalisation

#### **Modifier les paramètres dans src/config.py**
```python
# Centre de la carte
MAP_CONFIG = {
    "center_location": [0, 20],  # [latitude, longitude]
    "zoom_start": 4,             # Niveau de zoom initial
    "popup_max_width": 250       # Largeur max des popups
}

# Taille des icônes
ICON_CONFIG = {
    "blue": {"size": 30},    # Taille en pixels
    "green": {"size": 30},
    "grey": {"size": 30}
}
```

---

## 🎨 Gestion des Assets

### 1. Structure des Assets

```
assets/
├── icons/                 # Icônes des camps (PNG 30x30px)
│   ├── blue_house.png
│   ├── green_house.png
│   └── grey_house.png
├── img_TIF/              # GIFs animés des camps
│   ├── Mbera.gif
│   ├── Bidibidi.gif
│   └── ...
├── TIF/                  # Fichiers .tif téléchargeables
│   ├── FBRcollectionMonthlyVH_Mbera.tif
│   ├── FBRcollectionMonthlyVH_Bidibidi.tif
│   └── ...
└── results/              # Images de résultats
    ├── Mbera_results.png
    ├── Bidibidi_results.png
    └── ...
```

### 2. Ajouter des GIFs

**Pour chaque camp, ajoutez un GIF :**
```bash
# Le fichier doit être nommé exactement comme le camp
# Exemple pour le camp "Mbera" :
assets/img_TIF/Mbera.gif

# Exemple pour le camp "Nouveau_Camp" :
assets/img_TIF/Nouveau_Camp.gif
```

### 3. Ajouter des Fichiers TIF

**Convention de nommage :**
```bash
# Format : FBRcollectionMonthly{RADAR}_{NOM_CAMP}.tif
# Exemples :
assets/TIF/FBRcollectionMonthlyVH_Mbera.tif
assets/TIF/FBRcollectionMonthlyVV_Kyaka_II.tif
```

### 4. Ajouter des Images de Résultats

**Pour le bouton "Voir les résultats" :**
```bash
# Format : {NOM_CAMP}_results.png
# Exemples :
assets/results/Mbera_results.png
assets/results/Bidibidi_results.png
```

---

## ⚙️ Commandes Avancées

### 1. Sauvegarde et Restauration

#### **Sauvegarder les camps**
```bash
# Les camps sont automatiquement sauvés dans data/camps.json
# Pour faire une copie de sauvegarde :
cp data/camps.json data/camps_backup_$(date +%Y%m%d).json
```

#### **Restaurer depuis une sauvegarde**
```bash
cp data/camps_backup_20241201.json data/camps.json
```

### 2. Nettoyage

#### **Nettoyer les fichiers temporaires**
```bash
# Supprimer les fichiers temporaires
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

#### **Vérifier l'intégrité des assets**
```bash
python -c "
from src.camp_manager import CampManager
from pathlib import Path

m = CampManager()
m.load_from_json()

print('Vérification des assets...')
for camp in m.camps:
    gif_path = Path(f'assets/img_TIF/{camp.name}.gif')
    tif_path = Path(f'assets/TIF/FBRcollectionMonthly{camp.radar}_{camp.name}.tif')
    results_path = Path(f'assets/results/{camp.name}_results.png')
    
    print(f'{camp.name}:')
    print(f'  GIF: {\"✅\" if gif_path.exists() else \"❌\"} {gif_path}')
    print(f'  TIF: {\"✅\" if tif_path.exists() else \"❌\"} {tif_path}')
    print(f'  Results: {\"✅\" if results_path.exists() else \"❌\"} {results_path}')
"
```

### 3. Import/Export

#### **Exporter la liste des camps en CSV**
```bash
python -c "
from src.camp_manager import CampManager
import csv

m = CampManager()
m.load_from_json()

with open('export_camps.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'latitude', 'longitude', 'population', 'radar', 'icon_type'])
    for camp in m.camps:
        writer.writerow([camp.name, camp.latitude, camp.longitude, camp.population, camp.radar, camp.icon_type])

print('Export terminé: export_camps.csv')
"
```

---

## 🔧 Dépannage

### 1. Problèmes Courants

#### **"Module not found"**
```bash
# Vérifier que vous êtes dans le bon dossier
pwd
ls -la  # Vous devez voir main.py, add_camps.py, etc.

# Installer les dépendances manquantes
pip install folium pandas
```

#### **"Aucun camp enregistré"**
```bash
# Vérifier si le fichier existe
ls -la data/camps.json

# Si le fichier n'existe pas, ajouter des camps
python add_camps.py --interactive
```

#### **"Erreur lors de la génération de la carte"**
```bash
# Vérifier les permissions
ls -la output/

# Créer le dossier s'il n'existe pas
mkdir -p output

# Vérifier qu'il y a des camps
python add_camps.py --list
```

#### **GIF ou images non affichés**
```bash
# Vérifier que les fichiers existent
ls -la assets/img_TIF/
ls -la assets/results/

# Les noms doivent correspondre exactement
# Camp "Mbera" → assets/img_TIF/Mbera.gif
# Camp "Nouveau_Camp" → assets/img_TIF/Nouveau_Camp.gif
```

### 2. Vérifications Système

#### **Tester Python et les imports**
```bash
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import folium
    print('✅ folium OK')
except:
    print('❌ folium manquant: pip install folium')

try:
    import pandas
    print('✅ pandas OK')  
except:
    print('❌ pandas manquant: pip install pandas')
"
```

#### **Tester la génération basique**
```bash
python -c "
import folium
m = folium.Map(location=[0, 20], zoom_start=4)
m.save('test_carte.html')
print('✅ Test carte OK: test_carte.html')
"
```

---

## 📁 Structure des Fichiers

### 1. Fichiers Principaux

| Fichier | Description | Usage |
|---------|-------------|--------|
| `main.py` | Script principal | `python main.py` |
| `add_camps.py` | Gestion des camps | `python add_camps.py --help` |
| `src/camp_manager.py` | Logique des camps | Import automatique |
| `src/map_generator.py` | Génération carte | Import automatique |
| `src/config.py` | Configuration | Modifier les paramètres |

### 2. Fichiers de Données

| Fichier | Description | Format |
|---------|-------------|--------|
| `data/camps.json` | Base des camps | JSON auto-généré |
| `data/camps_template.csv` | Template import | CSV éditable |

### 3. Assets Requis

| Type | Emplacement | Nommage | Obligatoire |
|------|-------------|---------|-------------|
| Icônes | `assets/icons/` | `blue_house.png` | ✅ |
| GIFs | `assets/img_TIF/` | `{camp_name}.gif` | ✅ |
| TIFs | `assets/TIF/` | `FBRcollectionMonthly{radar}_{camp_name}.tif` | ✅ |
| Résultats | `assets/results/` | `{camp_name}_results.png` | ⚠️ Optionnel |

---

## 🚀 Workflow Complet

### 1. Premier Usage
```bash
# 1. Installation
pip install folium pandas

# 2. Ajouter des camps
python add_camps.py --interactive

# 3. Ajouter les assets (GIFs, TIFs, images)
# Copier vos fichiers dans assets/

# 4. Générer la carte
python main.py

# 5. Ouvrir dans le navigateur
open output/carte_camps.html
```

### 2. Ajout d'un Nouveau Camp
```bash
# 1. Ajouter le camp
python add_camps.py --name "Nouveau_Camp" --lat 10.123 --lon 20.456 --pop "5000"

# 2. Ajouter les assets
# - assets/img_TIF/Nouveau_Camp.gif
# - assets/TIF/FBRcollectionMonthlyVH_Nouveau_Camp.tif  
# - assets/results/Nouveau_Camp_results.png (optionnel)

# 3. Régénérer la carte
python main.py
```

### 3. Maintenance Régulière
```bash
# Vérifier l'état
python add_camps.py --list

# Sauvegarder
cp data/camps.json data/camps_backup_$(date +%Y%m%d).json

# Régénérer la carte
python main.py
```

---

## ❓ Aide et Support

### Commandes d'Aide
```bash
# Aide générale sur la gestion des camps
python add_camps.py --help

# Liste des commandes disponibles
python add_camps.py --help | grep -E "^\s+--"
```

### Ressources
- **Documentation folium** : https://python-visualization.github.io/folium/
- **Format GeoJSON** : https://geojson.org/
- **Coordonnées GPS** : https://www.gps-coordinates.net/

---

*Dernière mise à jour : 2025 - Version 1.0*