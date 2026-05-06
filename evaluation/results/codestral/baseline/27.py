python
        import pandas as pd
        import geopandas as gpd
        import rasterio
        from rasterio.mask import mask
        import folium

        # Load vector data of Batareyka River
        river = gpd.read_file('batareyka_river.shp')

        # Load raster data of water discharge during spring thaw
        with rasterio.open('water_discharge.tif') as src:
            out_image, out_transform = mask(src, river.geometry, crop=True)
            out_meta = src.meta.copy()

        # Update metadata for the new raster
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        # Save the clipped raster to disk
        with rasterio.open("water_discharge_clipped.tif", "w", **out_meta) as dest:
            dest.write(out_image)

        # Load the clipped raster data
        discharge = rasterio.open('water_discharge_clipped.tif')

        # Extract water discharge values for each segment of the river during spring thaw
        discharge_values = []
        for geom in river.geometry:
            values, _ = rasterio.mask.mask(discharge, [geom], crop=True)
            discharge_values.append(values[0][~np.isnan(values[0])].mean())

        # Add water discharge values to the river dataframe
        river['water_discharge'] = discharge_values

        # Visualize results on a map using folium
        m = folium.Map(location=[river.geometry.centroid.y.mean(), river.geometry.centroid.x.mean()], zoom_start=10)
        folium.GeoJson(river, style_function=lambda x: {'color': 'blue', 'weight': 2},
                       highlight_function=lambda x: {'weight': 3},
                       tooltip=folium.GeoJsonTooltip(fields=['water_discharge'], aliases=["Water Discharge (m³/s)"], labels=True)).add_to(m)
        m.save("27.html")