import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import folium

# 1. Подготовка данных
dem_path = 'path/to/dem.tif'
hydro_path = 'path/to/hydro.shp'
climate_path = 'path/to/climate.csv'

with rasterio.open(dem_path) as src:
    dem = src.read(1)
    transform = src.transform

hydro_gdf = gpd.read_file(hydro_path)

# 2. Определение зон риска
watershed_model = WatershedModel(dem, hydro_gdf)
risk_zones = watershed_model.run()

# 3. Оценка угрозы
climate_data = pd.read_csv(climate_path)
risk_score = evaluate_risk(risk_zones, climate_data)

# 4. Визуализация результатов
m = folium.Map(location=[43.26, 71.30], zoom_start=8) # Координаты и масштаб карты

for idx, row in risk_zones.iterrows():
    folium.GeoJson(
        data=row['geometry'],
        style_function=lambda x: {'fillColor': 'green' if row['risk_score'] <= 0.5 else 'red'},
        highlight=True,
        tooltip=folium.GeoJsonTooltip(fields=['name', 'risk_score'], labels=True)
    ).add_to(m)

m.save("156.html")