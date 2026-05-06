import psycopg2
import folium
import pandas as pd

# Connect to the database
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)

cur = conn.cursor()

# Query the latest water level data for Aksu River and Byzhy River
query = """
SELECT river_name, sensor_id, water_level, timestamp
FROM water_level_data
WHERE river_name IN ('Aksu River', 'Byzhy River')
ORDER BY timestamp DESC;
"""

df = pd.read_sql_query(query, conn)

# Close the database connection
cur.close()
conn.close()

# Set threshold values for water level (you can adjust these)
water_level_thresholds = {
    'Aksu River': {'min': 0.5, 'max': 2.5},
    'Byzhy River': {'min': 1.0, 'max': 3.0}
}

# Function to check if water level is within threshold
def is_within_threshold(river_name, water_level):
    thresholds = water_level_thresholds[river_name]
    return thresholds['min'] <= water_level <= thresholds['max']

# Check for suspicious data and send notifications if necessary
for index, row in df.iterrows():
    river_name = row['river_name']
    sensor_id = row['sensor_id']
    water_level = row['water_level']

    if not is_within_threshold(river_name, water_level):
        print(f"Suspicious data detected on {river_name} at sensor ID {sensor_id}. Water level: {water_level}")

# Create a map using Folium
m = folium.Map(location=[43.2566, 76.9180], zoom_start=8)  # Set the initial location and zoom level

# Add rivers to the map (you'll need to have river shapefiles)
river_shapes = {
    'Aksu River': 'path/to/aksuriver.shp',
    'Byzhy River': 'path/to/byzhyriver.shp'
}

for river_name, shapefile in river_shapes.items():
    folium.choropleth(
        geo_data=shapefile,
        fill_color='blue',
        fill_opacity=0.5,
        line_opacity=0.8,
        highlight_on=True
    ).add_to(m)

# Save the map as HTML file
m.save("65.html")