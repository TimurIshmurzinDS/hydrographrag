import folium
import pandas as pd
import numpy as np

def solve_sharyn_inflation():
    # 1. Setup: Coordinates for points along the Sharyn River/Canyon (Approximate)
    # Sharyn River is located in Kazakhstan
    data = {
        'station_name': ['Upper Reach', 'Canyon Entrance', 'Valley of Castles', 'Middle Gorge', 'Lower Basin'],
        'lat': [44.35, 44.28, 44.22, 44.15, 44.08],
        'lon': [79.30, 79.45, 79.60, 79.75, 79.90],
        'width_t1': [15.2, 45.5, 120.3, 30.1, 55.8], # Width in meters at Time 1
        'width_t2': [15.8, 48.2, 135.7, 31.5, 58.2]  # Width in meters at Time 2
    }

    df = pd.DataFrame(data)

    # 2. Calculate "Inflation Rate" (Morphological Expansion Rate)
    df['inflation_rate'] = ((df['width_t2'] - df['width_t1']) / df['width_t1']) * 100

    # 3. Initialize Folium Map centered around Sharyn Canyon
    m = folium.Map(location=[44.2, 79.6], zoom_start=9, tiles='OpenStreetMap')

    # 4. Define a function to map inflation rate to color
    def get_color(rate):
        if rate > 10:
            return 'red'    # High expansion
        elif rate > 2:
            return 'orange' # Moderate expansion
        else:
            return 'green'  # Stable

    # 5. Add points to the map
    for index, row in df.iterrows():
        color = get_color(row['inflation_rate'])
        
        popup_text = (
            f"Station: {row['station_name']}<br>"
            f"Width T1: {row['width_t1']}m<br>"
            f"Width T2: {row['width_t2']}m<br>"
            f"<b>Expansion Rate: {row['inflation_rate']:.2f}%</b>"
        )
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=folium.Popup(popup_text, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

    # Add a legend using a simple HTML string
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Expansion Rate</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High (>10%)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Moderate (2-10%)<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Stable (<2%)
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 6. Save the map strictly as 272.html
    m.save("272.html")
    print("Success: Map has been saved as 272.html")

if __name__ == "__main__":
    solve_sharyn_inflation()