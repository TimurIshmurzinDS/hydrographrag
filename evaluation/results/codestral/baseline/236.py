python
         import folium
         import geopandas as gpd
         # Load river data
         river_data = gpd.read_file('ayagoz_river.geojson')
         # Perform analysis to determine optimal trading locations based on water availability, infrastructure, and potential demand
         # For the purpose of this example, let's assume we have a DataFrame called `optimal_locations` with columns 'latitude', 'longitude', and 'score'
         # Create map centered around the river
         m = folium.Map(location=[river_data['geometry'].centroid.y.mean(), river_data['geometry'].centroid.x.mean()], zoom_start=10)
         # Add optimal trading locations to the map as markers with a popup showing their score
         for index, row in optimal_locations.iterrows():
             folium.Marker(location=[row['latitude'], row['longitude']], popup=f"Score: {row['score']}").add_to(m)
         # Save the map as HTML
         m.save("236.html")