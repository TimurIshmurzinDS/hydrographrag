python
         import folium
         import requests
         import json

         # Define coordinates of Ulken Almaty River or nearby hydrological stations
         river_coordinates = [43.2608, 76.9297]  # Example coordinates

         # Fetch water level data from USGS Water Data for the Nation API
         url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=SITE_CODE"
         response = requests.get(url)
         data = json.loads(response.text)

         # Extract water level value from the API response
         water_level = data['value']['timeSeries'][0]['values'][0]['value']['value']

         # Create a map centered at Ulken Almaty River coordinates
         m = folium.Map(location=river_coordinates, zoom_start=12)

         # Add a marker to the map with water level information
         folium.Marker(
             location=river_coordinates,
             popup=f"Current Water Level: {water_level} ft",
             icon=folium.Icon(color='blue')
         ).add_to(m)

         # Save the map as "15.html"
         m.save("15.html")