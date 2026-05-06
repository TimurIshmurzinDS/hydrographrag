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

# Query all tributaries of Karatal river
cur.execute("""
    SELECT r.id, r.name, r.length
    FROM rivers r
    JOIN river_connections rc ON r.id = rc.tributary_id
    WHERE rc.main_river_id = (SELECT id FROM rivers WHERE name = 'Karatal');
""")

tributaries = cur.fetchall()

# Calculate total length of tributaries
total_length = sum(r[2] for r in tributaries)

print(f"Total length of Karatal's tributaries: {total_length} km")

# Create a map centered on Karatal river
m = folium.Map(location=[43.57, 69.81], zoom_start=8)

# Add tributaries to the map
for trib in tributaries:
    folium.PolyLine(
        locations=[[trib[4], trib[5]], [trib[6], trib[7]]],
        weight=2,
        color='blue'
    ).add_to(m)

# Save the map as html file
m.save("93.html")

# Close database connection
cur.close()
conn.close()