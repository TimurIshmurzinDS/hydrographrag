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
       folium.GeoJson(basin).add_to(m)

       # Save the final map
       m.save("22.html")