python
         import geopandas as gpd
         import folium
         # Load river data
         sarykan = gpd.read_file('sarykan_river.shp')
         temirlik = gpd.read_file('temirlik_river.shp')
         # Define irrigation boundaries (example: buffer 500m from river)
         sarykan['irrigation'] = sarykan.buffer(500)
         temirlik['irrigation'] = temirlik.buffer(500)
         # Calculate available water volume (example: constant value for simplicity)
         sarykan['water_volume'] = 1000000 # m3
         temirlik['water_volume'] = 800000 # m3
         # Combine results
         total_water_volume = sarykan['water_volume'].sum() + temirlik['water_volume'].sum()
         print(f'Total available water volume for irrigation: {total_water_volume} m3')
         # Visualize on map
         m = folium.Map(location=[42, 71], zoom_start=8)
         folium.GeoJson(sarykan['irrigation']).add_to(m)
         folium.GeoJson(temirlik['irrigation']).add_to(m)
         m.save('118.html')