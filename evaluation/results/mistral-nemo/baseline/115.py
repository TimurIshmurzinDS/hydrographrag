import geopandas as gpd
import pandas as pd
import folium

# Load data
agricultural_land = gpd.read_file("agricultural_land.shp")
water_consumption = pd.read_csv("water_consumption.csv")
precipitation = pd.read_csv("precipitation.csv")

# Merge datasets on district name
merged_data = pd.merge(agricultural_land, water_consumption, how="inner", on="district_name")
merged_data = pd.merge(merged_data, precipitation, how="inner", on="district_name")

# Calculate water deficit
merged_data["water_deficit"] = merged_data["agri_land_area"] * merged_data["avg_water_consumption"] - merged_data["total_precipitation"]

# Aggregate data by river basin
temirlik_basin = merged_data[merged_data["river_basin"] == "Temirlik River"].groupby("district_name").agg({"water_deficit": "sum"})
byzhy_basin = merged_data[merged_data["river_basin"] == "Byzhy River"].groupby("district_name").agg({"water_deficit": "sum"})

# Create map
m = folium.Map(location=[41.0082, 69.6437], zoom_start=8)

# Add districts to the map with water deficit as a tooltip
for district in temirlik_basin.index:
    folium.GeoJson(
        gpd.read_file(f"districts/{district}.shp"),
        style_function=lambda x: {'fillColor': '#ff0000', 'color': '#ffffff'},
        highlight_function=lambda x: {'fillColor': '#ff5555', 'color': '#ffffff'},
        tooltip=folium.GeoJsonTooltip(fields=["water_deficit"], aliases=["Water Deficit:"], labels=True)
    ).add_to(m)

for district in byzhy_basin.index:
    folium.GeoJson(
        gpd.read_file(f"districts/{district}.shp"),
        style_function=lambda x: {'fillColor': '#00ff00', 'color': '#ffffff'},
        highlight_function=lambda x: {'fillColor': '#55ff55', 'color': '#ffffff'},
        tooltip=folium.GeoJsonTooltip(fields=["water_deficit"], aliases=["Water Deficit:"], labels=True)
    ).add_to(m)

# Save map
m.save("115.html")