import pandas as pd
import folium
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)

cur = conn.cursor()

# Execute SQL query
query = "SELECT * FROM posts_on_koktal_river"
cur.execute(query)
rows = cur.fetchall()

# Load data into a pandas DataFrame
columns = ['post_id', 'latitude', 'longitude', 'water_level']
df = pd.DataFrame(rows, columns=columns)

# Create a map centered on Koktal River
m = folium.Map(location=[50.7493, 68.1237], zoom_start=10)  # Approximate coordinates of Koktal River

# Add markers to the map for each post with their water level as labels
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Пост ID: {row['post_id']}\nУровень воды: {row['water_level']} м").add_to(m)

# Save the map as HTML file
m.save("88.html")

# Close database connection
cur.close()
conn.close()