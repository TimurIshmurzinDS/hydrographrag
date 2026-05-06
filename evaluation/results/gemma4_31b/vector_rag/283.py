import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
import numpy as np

def compare_time_series(df1, df2, value_col='Date_water_level_Value', time_col='resultTime'):
    """
    Функция для профессионального сравнения двух временных рядов уровней воды.
    """
    # Преобразование временных меток в формат datetime
    df1[time_col] = pd.to_datetime(df1[time_col])
    df2[time_col] = pd.to_datetime(df2[time_col])
    
    # Установка индекса для выравнивания
    df1 = df1.set_index(time_col)
    df2 = df2.set_index(time_col)
    
    # Объединение данных по общему времени (Inner Join)
    combined = df1[[value_col]].join(df2[[value_col]], lsuffix='_s1', rsuffix='_s2')
    
    # Расчет метрик
    correlation = combined.corr().iloc[0, 1]
    rmse = np.sqrt(((combined.iloc[:, 0] - combined.iloc[:, 1]) ** 2).mean())
    mae = (combined.iloc[:, 0] - combined.iloc[:, 1]).abs().mean()
    
    return {
        "correlation": correlation,
        "rmse": rmse,
        "mae": mae,
        "aligned_data": combined
    }

# --- GIS Section ---
# Load the basin boundary shapefile using a raw string
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate centroid for map initialization
centroid = basin_gdf.geometry.centroid.iloc[0]

# Initialize folium map
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Save the final map strictly as 283.html
m.save("283.html")

# --- Example Usage of the comparison function ---
if __name__ == "__main__":
    # Mock data simulating the entities resultTime and Date_water_level_Value
    data1 = {
        'resultTime': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'Date_water_level_Value': [1.2, 1.3, 1.5, 1.4, 1.6]
    }
    data2 = {
        'resultTime': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'Date_water_level_Value': [1.1, 1.4, 1.4, 1.5, 1.7]
    }
    
    df_obs1 = pd.DataFrame(data1)
    df_obs2 = pd.DataFrame(data2)
    
    results = compare_time_series(df_obs1, df_obs2)
    print(f"Correlation: {results['correlation']:.4f}")
    print(f"RMSE: {results['rmse']:.4f}")
    print(f"MAE: {results['mae']:.4f}")