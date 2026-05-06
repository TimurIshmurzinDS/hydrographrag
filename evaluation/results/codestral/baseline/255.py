python
         import rasterio
         import numpy as np
         from sklearn.cluster import KMeans
         import folium

         # Load the DEM data
         with rasterio.open('path_to_dem_data.tif') as src:
             dem = src.read(1)

         # Preprocess the DEM data (e.g., normalize, fill missing values)

         # Classify texture using K-means clustering
         kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters as needed
         dem_flat = dem.flatten().reshape(-1, 1)
         labels = kmeans.fit_predict(dem_flat)

         # Create a recipe for each texture class
         recipes = {
             0: "Soft bread with a light crumb",
             1: "Medium-textured bread with a slightly dense crumb",
             # Add more recipes as needed
         }

         # Visualize the results on a map
         m = folium.Map(location=[src.bounds[1], src.bounds[0]], zoom_start=10)

         # Assign colors to each texture class
         colors = ['blue', 'green', 'yellow', 'orange', 'red']  # Adjust the number of colors as needed

         # Add a GeoJson layer for each texture class
         for label in np.unique(labels):
             mask = labels == label
             geojson = rasterio.features.shapes(dem, transform=src.transform)
             geojson_filtered = [(geom, properties) for geom, val in zip(*geojson) if val == label]
             folium.GeoJson(geojson_filtered, style_function=lambda x: {'fillColor': colors[label], 'color': 'black', 'weight': 1}).add_to(m)

         # Add a legend to the map
         legend_html = '<div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 180px; background-color: white; z-index:9999; font-size:14px;">'
         for label, color in enumerate(colors):
             legend_html += f'<i style="background:{color}"></i> {recipes[label]}<br>'
         legend_html += '</div>'
         m.get_root().html.add_child(folium.Element(legend_html))

         # Save the map
         m.save("255.html")