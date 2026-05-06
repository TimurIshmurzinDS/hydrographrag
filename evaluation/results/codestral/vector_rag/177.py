python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile
       basins = gpd.read_file(r"data/basin_data.shp")
       basins = basins.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basins['geometry'].centroid.y.mean(), basins['geometry'].centroid.x.mean()], tiles='CartoDB positron')

       # Add basins to the map
       for _, r in basins.iterrows():
           sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
           geo_j = sim_geo.to_json()
           geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2})
           m.add_child(geo_j)

       # Hardcoded list of dictionaries for observations (if available)
       observations = [{'name': 'Observation 1', 'geometry': wkt.loads('POINT (x y)')}]

       # Add observations to the map
       for obs in observations:
           folium.Marker(location=[obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

       # Save the final map
       m.save("177.html")