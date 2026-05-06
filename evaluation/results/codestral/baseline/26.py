python
         import folium
         import requests
         import json

         # Define the coordinates of Osek River segments
         river_segments = [(lat1, lon1), (lat2, lon2), ...]  # Replace with actual coordinates

         # Fetch water level data from USGS Water Services API for flood period
         water_levels = []
         for segment in river_segments:
             lat, lon = segment
             response = requests.get(f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={site_code}&parameterCd=00060")
             data = json.loads(response.text)
             water_level = data['value']['timeSeries'][0]['values'][0]['value']['value']  # Extract water level value
             water_levels.append((lat, lon, water_level))

         # Create a map centered around Osek River
         m = folium.Map(location=[river_segments[0][0], river_segments[0][1]], zoom_start=12)

         # Add markers for each segment with water level information
         for segment in water_levels:
             lat, lon, water_level = segment
             folium.Marker(location=[lat, lon], popup=f"Water Level: {water_level} ft").add_to(m)

         # Save the map as HTML file
         m.save("26.html")