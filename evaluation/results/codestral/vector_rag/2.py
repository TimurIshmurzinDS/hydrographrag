python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.geometry.centroid.y.mean(), basin.geometry.centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of rivers and their water levels (replace with actual data)
       rivers = [{'name': 'Karatal River', 'water_level': Water_level_Value}, {'name': 'Koktal River', 'water_level': Water_level_Valuecm}]

       # Add rivers to the map
       for river in rivers:
           folium.Marker(location=[0, 0], popup=f"{river['name']}<br>Water level: {river['water_level']}").add_to(m)

       # Save the final map
       m.save("2.html")