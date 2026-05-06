python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile and convert to CRS 'EPSG:4326'
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map using folium.GeoJson
       folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries containing the coordinates (WKT)
       points = [{'name': 'Ice Extraction Point', 'coordinates': wkt.loads('POINT (69.5874 53.1205)')}]

       # Add each point to the map as a folium.Marker
       for point in points:
           folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

       # Save the final map
       m.save("267.html")