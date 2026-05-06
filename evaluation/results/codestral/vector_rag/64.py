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

       # If coordinates are available, they can be added to the map as follows:
       # coordinates = ['WKT_STRING1', 'WKT_STRING2', ...]
       # for coord in coordinates:
       #     point = wkt.loads(coord)
       #     folium.CircleMarker(location=[point.y, point.x], radius=5).add_to(m)

       # Save the final map
       m.save("64.html")