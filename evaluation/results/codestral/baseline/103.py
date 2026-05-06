python
         import osmnx as ox
         import geopandas as gpd
         import folium
         # Set the place name or address
         place = 'World'
         # Retrieve the street network graph from OpenStreetMap
         G = ox.graph_from_place(place, network_type='all')
         # Convert the graph to a GeoDataFrame
         gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
         # Filter the edges dataframe to include only rivers named Уржар, Дос or Каратал
         rivers = ['Уржар', 'Дос', 'Каратал']
         filtered_rivers = gdf_edges[gdf_edges['name'].isin(rivers)]
         # Extract the coordinates of each point in the filtered dataframe
         coordinates = [list(point.coords) for point in filtered_rivers.geometry]
         print("Coordinates:", coordinates)
         # Visualize the result on a map using folium
         m = folium.Map(location=[filtered_rivers.unary_union.centroid.y, filtered_rivers.unary_union.centroid.x], zoom_start=10)
         for river in filtered_rivers['geometry']:
             folium.GeoJson(river).add_to(m)
         m.save("103.html")