import geopandas as gpd
import rasterio
from rasterio.features import shapes
import folium

# Загружаем данные о стоке реки Турген в формате растра
with rasterio.open('turgen_river_water_level.tif') as src:
    image = src.read(1)
    results = (
        {'properties': {'raster_value': v}, 'geometry': s}
        for i, (s, v) in enumerate(shapes(image, transform=src.transform))
    )

# Создаем GeoDataFrame из результатов анализа растра
gdf = gpd.GeoDataFrame.from_features(list(results))

# Определяем области с высоким и низким уровнем воды на основе данных о стоке реки
high_water_level = gdf[gdf['raster_value'] > 50]
low_water_level = gdf[gdf['raster_value'] <= 50]

# Создаем слой доступности воды для орошения садов на основе анализа данных о стоке реки
water_availability = high_water_level.copy()
water_availability[' Availability'] = 'High'
water_availability = water_availability.append(low_water_level, ignore_index=True)
water_availability['Availability'] = water_availability['Availability'].fillna('Low')

# Создаем карту с использованием библиотеки folium
m = folium.Map(location=[43.2568, 71.0999], zoom_start=12)

# Добавляем слой доступности воды для орошения садов на карту
folium.GeoJson(
    water_availability[['geometry', 'Availability']],
    style_function=lambda x: {
        'fillColor': 'green' if x['properties']['Availability'] == 'High' else 'red',
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    },
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function).add_to(m),
    tooltip=folium.features.GeoJsonTooltip(fields=['Availability'], aliases=['Доступность воды:', 'Availability'])
).add_to(m)

# Сохраняем карту в формате HTML
m.save("183.html")