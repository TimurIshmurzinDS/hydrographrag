python
         import folium
         import geopandas as gpd
         # Load the river data
         river = gpd.read_file('uzyn_kargaly_river.shp')
         # Define a function to calculate cocktail recipe based on water level
         def cocktail_recipe(water_level):
             if water_level < 1:
                 return 'Мохито'
             elif water_level < 2:
                 return 'Дайкири'
             else:
                 return 'Пина Колада'
         # Calculate the cocktail recipe for each segment of the river
         river['cocktail'] = river['water_level'].apply(cocktail_recipe)
         # Create a map centered on the river
         m = folium.Map(location=[river.geometry.centroid.y.mean(), river.geometry.centroid.x.mean()], zoom_start=10)
         # Add the river to the map with different colors based on cocktail recipe
         for _, r in river.iterrows():
             folium.GeoJson(r['geometry'], style_function=lambda x, color=f'#{int(r["water_level"]*50):02x}0000': {'fillColor': color}).add_to(m)
         # Save the map as HTML file
         m.save("219.html")