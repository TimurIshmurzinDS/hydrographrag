import psycopg2
import folium

# Connect to the database
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)

cur = conn.cursor()

# Query the database for sensor data from all rivers
cur.execute("SELECT river_name, latitude, longitude, status FROM sensors")
rows = cur.fetchall()

# Initialize a map centered on the average location of all sensors
avg_lat = sum([row[1] for row in rows]) / len(rows)
avg_lon = sum([row[2] for row in rows]) / len(rows)
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4)

# Add markers to the map for each sensor
for row in rows:
    river_name, lat, lon, status = row

    # Create a custom icon based on the sensor's status
    if status == 'working':
        icon = folium.features.CustomIcon('https://via.placeholder.com/30', icon_size=(20, 20))
    else:
        icon = folium.features.CustomIcon('https://via.placeholder.com/30?text=X', icon_size=(20, 20))

    # Add the marker to the map
    folium.Marker([lat, lon], popup=f"{river_name}: {status}", icon=icon).add_to(m)

# Save the final map as "145.html"
m.save("145.html")

# Close the database connection
cur.close()
conn.close()