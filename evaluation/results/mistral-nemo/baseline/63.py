import pandas as pd
import folium
import sqlite3

# 1. Connect to the database
conn = sqlite3.connect('hydro_data.db')
cursor = conn.cursor()

# 2. Write SQL query to fetch current water levels for all hydroposts on Byzhy River
query = "SELECT id, latitude, longitude, water_level FROM hydroposts WHERE river_name='Byzhy River'"

# 3. Read data into DataFrame using pandas
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# 4. Create a map centered on Byzhy River coordinates (assuming average coordinates are available)
m = folium.Map(location=[52.9167, 37.5], zoom_start=8)  # Replace with actual coordinates

# 5. Add markers to the map for each hydropost with current water levels
for index, row in df.iterrows():
    popup_text = f"Hydropost ID: {row['id']}<br>Water Level: {row['water_level']} m"
    folium.Marker([row['latitude'], row['longitude']], popup=folium.Popup(popup_text, max_width=300)).add_to(m)

# 6. Save the map as HTML
m.save("63.html")