import folium

# Variable icon personnalisé
blue_house_icon = {"path": "icons/blue_house.png", "size": 30}
green_house_icon = {"path": "icons/green_house.png", "size": 30}
grey_house_icon = {"path": "icons/grey_house.png", "size": 30}

# Liste des camps avec leurs coordonnées et informations
camps = [
    {"name": "Abala", "coords": [14.910382, 3.418554], "icon": blue_house_icon, "population": "21 394", "radar" : "VH"},
    {"name": "Awserd", "coords": [27.626641, -7.872215], "icon": blue_house_icon, "population": "N/A", "radar" : "VH"},
    {"name": "Bambasi", "coords": [9.777854, 34.780491], "icon": blue_house_icon, "population": "20 712", "radar" : "VH"},
    {"name": "Dakhla", "coords": [26.830602, -6.864148], "icon": blue_house_icon, "population": "N/A", "radar" : "VH"},
    {"name": "Mbera", "coords": [15.833333, -5.800000], "icon": blue_house_icon, "population": "100 807", "radar" : "VH"},
    {"name": "Smara", "coords": [27.501643, -7.818791], "icon": blue_house_icon, "population": "N/A", "radar" : "VH"},
    {"name": "Gaga", "coords": [13.763725, 21.447086], "icon": green_house_icon, "population": "36 856", "radar" : "VH"},
    {"name": "Chadakori", "coords": [13.672647, 6.990000], "icon": grey_house_icon, "population": "N/A", "radar" : "VH"},
    {"name": "Bidibidi", "coords": [3.478382, 31.373434], "icon": blue_house_icon, "population": "197 535", "radar" : "VH"},
    {"name": "Kyangwali", "coords": [1.179656, 30.763555], "icon": blue_house_icon, "population": "133 265", "radar" : "VH"},
    {"name": "Kyaka_II", "coords": [0.357999, 31.081311], "icon": blue_house_icon, "population": "125 754", "radar" : "VV"},
    {"name": "Tongogara", "coords": [-20.346946,32.308155], "icon": blue_house_icon, "population": "N/A", "radar" : "VV"},
    {"name": "Kiryandongo", "coords": [1.939906,32.170786], "icon": blue_house_icon, "population": "N/A", "radar" : "VV"},  # Compact mais pas sur toute la zone
    {"name": "Nakivale", "coords": [-0.776389,30.949444], "icon": blue_house_icon, "population": "183 441", "radar" : "VV"},  # Compact mais pas sur toute la zone
    {"name": "Ayilo_1", "coords": [3.291162,31.940242], "icon": blue_house_icon, "population": "N/A", "radar" : "VV"},  # Compact, on voit pas trop de différence en optique
    {"name": "Nyarugusu", "coords": [-4.220900,30.384600], "icon": blue_house_icon, "population": "136 479", "radar" : "VV"},# Compact 
    {"name": "Meri", "coords": [3.848600,30.201860], "icon": blue_house_icon, "population": "25 203", "radar" : "VV"}, 
]

# Créer une carte centrée sur l'Afrique
m = folium.Map(location=[0, 20], zoom_start=4)

# Ajouter les camps à la carte
for index, camp in enumerate(camps):
    # Création de la popup avec modal dynamique
    modal_id = f"modal_{index}"  # Générer un id unique pour chaque modal
    popup_html = f'''
    <div style="font-family: Arial; text-align: left; display: inline-block; padding: 10px;">
        <h3 style="color: #2C3E50; "><strong>{camp['name']}</strong></h3>
        <p style="font-size: 14px;color: #2C3E50;">Population: <strong>{camp['population']}</strong> à la fin de 2023</p>
        <p style="font-size: 14px;color: #2C3E50;">Latidude: <strong>{camp['coords'][0]}</strong></p>
        <p style="font-size: 14px;color: #2C3E50;">Longitude: <strong>{camp['coords'][1]}</strong></p>
        <a href="#" onclick="openModal('{modal_id}');">
            <img src="img_TIF/{camp['name']}.gif" style="width: auto; height: auto; max-width: 100%;">
        </a>    
        <br>
        <a href="TIF/FBRcollectionMonthly{camp['radar']}_{camp['name']}.tif" download style="font-size: 14px;color: #2C3E50;">Cliquez ici pour télécharger le .tif</a>
    </div>
    '''
    
    # Générer les modals pour chaque camp
    modal_html = f'''
    <div id="{modal_id}" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background-color: rgba(0,0,0,0.8); z-index: 9999;">
        <span onclick="closeModal('{modal_id}');" style="position:absolute; top:20px; right:30px; color:white; font-size:40px; cursor:pointer;">&times;</span>
        <img src="img_TIF/{camp['name']}.gif" style="display:block; margin:auto; max-width:90%; max-height:90%;">
    </div>
    '''
    
    # Ajouter le marker pour chaque camp
    try:
        folium.Marker(
            location=camp["coords"],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"<p style=\"font-size: 16px;\"><strong>{camp['name']}</strong></p>",
            icon=folium.CustomIcon(icon_image=camp['icon']['path'], icon_size=(camp['icon']['size'], camp['icon']['size']))
        ).add_to(m)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    
    # Ajouter le modal spécifique à ce camp à la carte
    m.get_root().html.add_child(folium.Element(modal_html))

# Ajouter les fonctions JavaScript pour ouvrir et fermer les modals
js_functions = '''
<script>
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}
</script>
'''

m.get_root().html.add_child(folium.Element(js_functions))
legend_html = '''
     <div style="position: fixed; 
                 bottom: 10px; left: 10px; width: 250px; height: 200px;
                 background-color: white; border: 2px solid grey; z-index: 9999;
                 font-size: 14px; padding: 10px;">
        <strong>Legend</strong><br>
        <img src="./icons/blue_house.png" style="width: 30px; height: 30px; vertical-align: middle;"> Site mapping data<br>
        <img src="icons/green_house.png" style="width: 30px; height: 30px; vertical-align: middle;">OpenStreetMap data<br>
        <img src="icons/grey_house.png" style="width: 30px; height: 30px; vertical-align: middle;">No data<br>
        <p><strong>Sources :</strong> <a href="https://im.unhcr.org/apps/sitemapping/#/">UNHCR</a></p>
        <p style="margin-left: 70px;"><a href="https://browser.dataspace.copernicus.eu/">Copernicus</a>
    </div>
'''

# Ajouter la légende à la carte
m.get_root().html.add_child(folium.Element(legend_html))
# Sauvegarder la carte dans un fichier HTML
m.save("carte_camps.html")