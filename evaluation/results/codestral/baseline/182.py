python
        import geopandas as gpd
        import rasterio
        from rasterstats import zonal_stats
        import folium

        # Load data
        water_resources = rasterio.open('water_resources.tif')
        precipitation = rasterio.open('precipitation.tif')
        evaporation = rasterio.open('evaporation.tif')
        consumption = rasterio.open('consumption.tif')
        groundwater = rasterio.open('groundwater.tif')
        shapefile = gpd.read_file('urjar_basin.shp')

        # Calculate water balance
        balance = precipitation - evaporation - consumption + groundwater

        # Calculate water deficit for agricultural needs
        deficit = water_resources - balance

        # Identify critical zones of water deficit
        shapefile['deficit'] = [zonal_stats(geom, deficit.read(1), stats='mean')[0]['mean'] for geom in shapefile.geometry]
        critical_zones = shapefile[shapefile['deficit'] < 0]

        # Visualize results on a map
        m = folium.Map(location=[critical_zones.geometry.centroid.y.mean(), critical_zones.geometry.centroid.x.mean()], zoom_start=10)
        folium.GeoJson(critical_zones).add_to(m)
        m.save("182.html")