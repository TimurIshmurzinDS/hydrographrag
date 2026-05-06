python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for the lake and river observations (WKT coordinates are not provided in the context)
       entities = [{'name': 'Lake Ulken Almaty', 'type': 'Observation'}, {'name': '1.1 km above Lake Ulken Almaty', 'type': 'Observation'}]

       # Save the final map
       m.save("15.html")