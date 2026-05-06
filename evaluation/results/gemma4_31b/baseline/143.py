import pandas as pd
import folium
from folium.plugins import MarkerCluster

# 1. Simulation of geospatial data for hydrometric posts
# In a real scenario, this data would be loaded from a Shapefile, GeoJSON or Database
data = {
    'post_id': [101, 102, 103, 104, 201, 202, 203, 204],
    'river': ['Karatal', 'Karatal', 'Karatal', 'Karatal', 'Lepsy', 'Lepsy', 'Lepsy', 'Lepsy'],
    'lat': [43.21, 43.35, 43.48, 43.60, 43.80, 43.95, 44.10, 44.25],
    'lon': [78.10, 78.25, 78.40, 78.55, 80.10, 80.25, 80.40, 80.55],
    'status': ['Working', 'Not Working', 'Working', 'Working', 'Working', 'Not Working', 'Not Working', 'Working']
}

df = pd.DataFrame(data)

# 2. Comparative Analysis
def analyze_status(river_name):
    river_df = df[df['river'] == river_name]
    total = len(river_df)
    working = len(river_df[river_df['status'] == 'Working'])
    percentage = (working / total) * 100 if total > 0 else 0
    return total, working, percentage

karatal_stats = analyze_status('Karatal')
lepsy_stats = analyze_status('Lepsy')

print(f"Analysis for Karatal: Total={karatal_stats[0]}, Working={karatal_stats[1]}, Efficiency={karatal_stats[2]:.2f}%")
print(f"Analysis for Lepsy: Total={lepsy_stats[0]}, Working={lepsy_stats[1]}, Efficiency={lepsy_stats[2]:.2f}%")

# 3. Geospatial Visualization
# Center the map between the two river basins
m = folium.Map(location=[43.7, 79.3], zoom_start=7, tiles='CartoDB positron')

# Color mapping for statuses
color_map = {
    'Working': 'green',
    'Not Working': 'red',
    'Needs Repair': 'orange'
}

# Add markers to the map
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"Post ID: {row['post_id']}<br>River: {row['river']}<br>Status: {row['status']}",
        color=color_map.get(row['status'], 'gray'),
        fill=True,
        fill_color=color_map.get(row['status'], 'gray'),
        fill_opacity=0.7
    ).add_to(m)

# Add a legend using HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Status Legend</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Working<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Not Working<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Needs Repair
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map strictly as 143.html
m.save("143.html")

print("Map has been saved as 143.html")