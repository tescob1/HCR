# src/map_generator.py
"""
Générateur de carte interactive pour les camps de réfugiés
"""

import folium
from typing import List
from .camp_manager import Camp, CampManager
from .config import *

class MapGenerator:
    """Générateur de carte interactive"""
    
    def __init__(self, camp_manager: CampManager):
        self.camp_manager = camp_manager
    
    def _create_popup_html(self, camp: Camp, modal_id: str) -> str:
        """Créer le HTML de la popup pour un camp"""
        return f'''
        <div style="font-family: {POPUP_STYLE['font_family']}; 
                    text-align: {POPUP_STYLE['text_align']}; 
                    display: inline-block; 
                    padding: {POPUP_STYLE['padding']};
                    min-width: 200px;">
            <h3 style="color: {POPUP_STYLE['title_color']}; margin: 0 0 10px 0;"><strong>{camp.name}</strong></h3>
            <p style="font-size: {POPUP_STYLE['font_size']}; color: {POPUP_STYLE['text_color']}; margin: 5px 0;">
                Population: <strong>{camp.population}</strong> à la fin de 2023
            </p>
            <p style="font-size: {POPUP_STYLE['font_size']}; color: {POPUP_STYLE['text_color']}; margin: 5px 0;">
                Latitude: <strong>{camp.latitude:.6f}</strong>
            </p>
            <p style="font-size: {POPUP_STYLE['font_size']}; color: {POPUP_STYLE['text_color']}; margin: 5px 0;">
                Longitude: <strong>{camp.longitude:.6f}</strong>
            </p>
            <div style="text-align: center; margin: 15px 0;">
                <a href="#" onclick="openModal('{modal_id}');">
                    <img src="../{get_gif_path(camp.name)}" 
                         style="width: auto; height: auto; max-width: 100%; cursor: pointer; border: 1px solid #ddd;"
                         alt="Aperçu {camp.name}">
                </a>    
            </div>
            
            <div style="text-align: center; margin: 15px 0;">
                <div style="margin-bottom: 8px;">
                    <a href="#" onclick="openModal('{modal_id}_results');" 
                       style="font-size: {POPUP_STYLE['font_size']}; color: white; 
                              text-decoration: none; background: #e74c3c; 
                              padding: 8px 15px; border-radius: 4px; 
                              display: inline-block; width: 150px; text-align: center;">
                        📊 Voir les résultats
                    </a>
                </div>
                <div>
                    <a href=../{get_tif_path(camp.name, camp.radar)}
                       download 
                       style="font-size: {POPUP_STYLE['font_size']}; color: white; 
                              text-decoration: none; background: #3498db; 
                              padding: 8px 15px; border-radius: 4px;
                              display: inline-block; width: 150px; text-align: center;">
                        📥 Télécharger le .tif
                    </a>
                </div>
            </div>
        </div>
        '''
    
    def _create_modal_html(self, camp: Camp, modal_id: str) -> str:
        """Créer le HTML du modal pour un camp"""
        return f'''
        <div id="{modal_id}" style="display:none; position:fixed; top:0; left:0; 
                                   width:100%; height:100%; background-color: rgba(0,0,0,0.8); 
                                   z-index: 9999; cursor: pointer;" 
             onclick="closeModal('{modal_id}');">
            <span onclick="closeModal('{modal_id}');" 
                  style="position:absolute; top:20px; right:30px; color:white; 
                         font-size:40px; cursor:pointer; z-index: 10000;">&times;</span>
            <div style="display:flex; align-items:center; justify-content:center; 
                        height:100%; padding:20px;">
                <div style="text-align:center; max-width:90%; max-height:90%;">
                    <img src="../{get_gif_path(camp.name)}" 
                         style="max-width:100%; max-height:80vh; object-fit:contain;"
                         alt="{camp.name}">
                    <h2 style="color:white; margin-top:20px;">{camp.name}</h2>
                    <p style="color:white;">Population: {camp.population} | Radar: {camp.radar}</p>
                </div>
            </div>
        </div>
        '''

    def _create_results_modal_html(self, camp: Camp, modal_id: str) -> str:
        """Créer le HTML du modal pour les résultats"""
        return f'''
        <div id="{modal_id}" style="display:none; position:fixed; top:0; left:0; 
                                   width:100%; height:100%; background-color: rgba(0,0,0,0.8); 
                                   z-index: 9999; cursor: pointer;" 
             onclick="closeModal('{modal_id}');">
            <span onclick="closeModal('{modal_id}');" 
                  style="position:absolute; top:20px; right:30px; color:white; 
                         font-size:40px; cursor:pointer; z-index: 10000;">&times;</span>
            <div style="display:flex; align-items:center; justify-content:center; 
                        height:100%; padding:20px;">
                <div style="text-align:center; max-width:90%; max-height:90%;">
                    <img src="../assets/results/{camp.name}_results.png" 
                         style="max-width:100%; max-height:80vh; object-fit:contain;"
                         alt="Résultats {camp.name}">
                    <h2 style="color:white; margin-top:20px;">Résultats d'analyse - {camp.name}</h2>
                    <p style="color:white;">Population: {camp.population} | Radar: {camp.radar}</p>
                </div>
            </div>
        </div>
        '''
        """Créer le HTML du modal pour un camp"""
        return f'''
        <div id="{modal_id}" style="display:none; position:fixed; top:0; left:0; 
                                   width:100%; height:100%; background-color: rgba(0,0,0,0.8); 
                                   z-index: 9999; cursor: pointer;" 
             onclick="closeModal('{modal_id}');">
            <span onclick="closeModal('{modal_id}');" 
                  style="position:absolute; top:20px; right:30px; color:white; 
                         font-size:40px; cursor:pointer; z-index: 10000;">&times;</span>
            <div style="display:flex; align-items:center; justify-content:center; 
                        height:100%; padding:20px;">
                <div style="text-align:center; max-width:90%; max-height:90%;">
                    <img src=../"{get_gif_path(camp.name)}" 
                         style="max-width:100%; max-height:80vh; object-fit:contain;"
                         alt="{camp.name}">
                    <h2 style="color:white; margin-top:20px;">{camp.name}</h2>
                    <p style="color:white;">Population: {camp.population} | Radar: {camp.radar}</p>
                </div>
            </div>
        </div>
        '''
    
    def _create_legend_html(self) -> str:
        """Créer le HTML de la légende"""
        legend_items = ""
        for icon_type, config in ICON_CONFIG.items():
            legend_items += f'''
            <div style="margin: 5px 0;">
                <img src=../{get_icon_path(icon_type)}
                     style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px;">
                {config['description']}
            </div>
            '''
        
        return f'''
        <div style="position: {LEGEND_STYLE['position']}; 
                    bottom: {LEGEND_STYLE['bottom']}; 
                    left: {LEGEND_STYLE['left']}; 
                    width: {LEGEND_STYLE['width']}; 
                    height: {LEGEND_STYLE['height']};
                    background-color: {LEGEND_STYLE['background_color']}; 
                    border: {LEGEND_STYLE['border']}; 
                    z-index: {LEGEND_STYLE['z_index']};
                    font-size: {LEGEND_STYLE['font_size']}; 
                    padding: {LEGEND_STYLE['padding']};
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
            <h4 style="margin: 0 0 10px 0; color: #2C3E50;">🗺️ Légende</h4>
            {legend_items}
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #ddd;">
                <p style="margin: 5px 0; font-size: 12px;">
                    <strong>Sources:</strong><br>
                    <a href="{DATA_SOURCES['unhcr']}" target="_blank" style="color: #3498db;">UNHCR</a> | 
                    <a href="{DATA_SOURCES['copernicus']}" target="_blank" style="color: #3498db;">Copernicus</a>
                </p>
            </div>
        </div>
        '''
    
    def _create_javascript_functions(self) -> str:
        """Créer les fonctions JavaScript pour les modals"""
        return '''
        <script>
        function openModal(modalId) {
            document.getElementById(modalId).style.display = "block";
            document.body.style.overflow = "hidden"; // Empêcher le scroll
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = "none";
            document.body.style.overflow = "auto"; // Rétablir le scroll
        }
        
        // Fermer le modal en cliquant en dehors de l'image
        document.addEventListener('click', function(event) {
            if (event.target.id && event.target.id.startsWith('modal_')) {
                closeModal(event.target.id);
            }
        });
        
        // Fermer le modal avec la touche Échap
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                var modals = document.querySelectorAll('[id^="modal_"]');
                modals.forEach(function(modal) {
                    if (modal.style.display === 'block') {
                        closeModal(modal.id);
                    }
                });
            }
        });
        </script>
        '''
    
    def _add_statistics_panel(self, map_obj: folium.Map) -> None:
        """Ajouter un panneau de statistiques"""
        total_camps = len(self.camp_manager.camps)
        stats_by_icon = {}
        
        for icon_type in ICON_CONFIG.keys():
            count = len(self.camp_manager.get_camps_by_icon_type(icon_type))
            if count > 0:
                stats_by_icon[icon_type] = count
        
        stats_html = f'''
        <div style="position: fixed; 
                    top: 10px; right: 10px; 
                    background-color: white; 
                    border: 2px solid #3498db; 
                    border-radius: 8px;
                    padding: 15px; 
                    z-index: 9999;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                    font-family: Arial;
                    font-size: 14px;">
            <h4 style="margin: 0 0 10px 0; color: #2C3E50;">📊 Statistiques</h4>
            <p style="margin: 5px 0;"><strong>Total des camps:</strong> {total_camps}</p>
            <hr style="border: 1px solid #ddd; margin: 10px 0;">
        '''
        
        for icon_type, count in stats_by_icon.items():
            description = ICON_CONFIG[icon_type]['description']
            stats_html += f'<p style="margin: 3px 0;">• {description}: {count}</p>'
        
        stats_html += '</div>'
        
        map_obj.get_root().html.add_child(folium.Element(stats_html))
    
    def generate_map(self, output_file: str = None, include_statistics: bool = True) -> bool:
        """Générer la carte interactive"""
        if output_file is None:
            output_file = OUTPUT_HTML
        
        if not self.camp_manager.camps:
            print(MESSAGES["info"]["no_camps"])
            return False
        
        try:
            # Créer la carte
            map_obj = folium.Map(
                location=MAP_CONFIG["center_location"],
                zoom_start=MAP_CONFIG["zoom_start"],
                tiles='OpenStreetMap'
            )
            
            # Ajouter les camps
            for index, camp in enumerate(self.camp_manager.camps):
                modal_id = f"modal_{index}"
                
                # Créer la popup
                popup_html = self._create_popup_html(camp, modal_id)
                
                # Créer le modal
                modal_html = self._create_modal_html(camp, modal_id)
                
                # Ajouter le marker
                try:
                    folium.Marker(
                        location=[camp.latitude, camp.longitude],
                        popup=folium.Popup(popup_html, max_width=MAP_CONFIG["popup_max_width"]),
                        tooltip=f"<div style='font-size: 16px; font-weight: bold;'>{camp.name}</div>",
                        icon=folium.CustomIcon(
                            icon_image=get_icon_path(camp.icon_type), 
                            icon_size=(ICON_CONFIG[camp.icon_type]["size"], ICON_CONFIG[camp.icon_type]["size"])
                        )
                    ).add_to(map_obj)
                    
                    # Ajouter le modal principal (GIF) à la carte
                    map_obj.get_root().html.add_child(folium.Element(modal_html))
                    
                    # Ajouter le modal des résultats
                    results_modal_html = self._create_results_modal_html(camp, f"{modal_id}_results")
                    map_obj.get_root().html.add_child(folium.Element(results_modal_html))
                    
                except Exception as e:
                    print(f"⚠️ Erreur lors de l'ajout du camp {camp.name}: {e}")
                    continue
                    
                except Exception as e:
                    print(f"⚠️ Erreur lors de l'ajout du camp {camp.name}: {e}")
                    continue
            
            # Ajouter les fonctions JavaScript
            js_functions = self._create_javascript_functions()
            map_obj.get_root().html.add_child(folium.Element(js_functions))
            
            # Ajouter la légende
            legend_html = self._create_legend_html()
            map_obj.get_root().html.add_child(folium.Element(legend_html))
            
            # Ajouter les statistiques si demandé
            if include_statistics:
                self._add_statistics_panel(map_obj)
            
            # Sauvegarder la carte
            ensure_directories()
            map_obj.save(output_file)
            
            print(MESSAGES["success"]["map_generated"].format(file=output_file))
            print(f"🌍 Carte générée avec {len(self.camp_manager.camps)} camps")
            return True
            
        except Exception as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False
    
    def generate_custom_map(self, center_lat: float, center_lon: float, zoom: int, 
                          filter_icon_type: str = None, output_file: str = None) -> bool:
        """Générer une carte personnalisée avec des paramètres spécifiques"""
        if output_file is None:
            output_file = OUTPUT_HTML.replace('.html', '_custom.html')
        
        # Filtrer les camps si nécessaire
        camps_to_display = self.camp_manager.camps
        if filter_icon_type:
            camps_to_display = self.camp_manager.get_camps_by_icon_type(filter_icon_type)
        
        if not camps_to_display:
            print(f"❌ Aucun camp à afficher pour le filtre '{filter_icon_type}'")
            return False
        
        try:
            # Créer la carte avec les paramètres personnalisés
            map_obj = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=zoom,
                tiles='OpenStreetMap'
            )
            
            # Temporairement remplacer les camps du manager
            original_camps = self.camp_manager.camps
            self.camp_manager.camps = camps_to_display
            
            # Générer la carte
            result = self.generate_map(output_file, include_statistics=True)
            
            # Restaurer les camps originaux
            self.camp_manager.camps = original_camps
            
            return result
            
        except Exception as e:
            print(MESSAGES["error"]["general_error"].format(error=str(e)))
            return False