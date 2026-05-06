python
         import geopandas as gpd
         import rasterio
         from rasterstats import zonal_stats
         import folium
         # Load vector data
         basin = gpd.read_file('basin.shp')
         irrigation_areas = gpd.read_file('irrigation_areas.shp')
         # Load raster data
         with rasterio.open('water_usage.tif') as src:
             water_usage = src.read(1)
         # Intersect basin and irrigation areas
         intersected = gpd.overlay(basin, irrigation_areas, how='intersection')
         # Calculate water usage for each irrigated area
         stats = zonal_stats(intersected, water_usage, stats=['sum'], nodata=-9999)
         intersected['water_usage'] = [s['sum'] for s in stats]
         # Visualize results on map
         m = folium.Map(location=[basin.geometry.centroid.y.mean(), basin.geometry.centroid.x.mean()], zoom_start=10)
         folium.GeoJson(intersected[['geometry', 'water_usage']].to_json()).add_to(m)
         m.save("39.html")