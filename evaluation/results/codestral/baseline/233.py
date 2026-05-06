python
         import folium
         import geopandas as gpd
         import rasterio
         from rasterio import features

         # Load the flood data
         with rasterio.open('flood_data.tif') as src:
             image = src.read(1)
             results = (
                 {'properties': {'raster_val': v}, 'geometry': s}
                 for i, (s, v) in enumerate(features.shapes(image, transform=src.transform)))

         # Convert the raster data to vector data
         geoms = list(results)
         gdf = gpd.GeoDataFrame.from_features(geoms)

         # Create a map centered around the flood area
         m = folium.Map(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], zoom_start=10)

         # Add the flood areas to the map
         for _, r in gdf.iterrows():
             sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
             geo_j = sim_geo.to_json()
             geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
             geo_j.add_to(m)

         # Save the map to a file
         m.save("233.html")