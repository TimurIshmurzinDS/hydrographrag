import folium
import random
import hashlib
import json
from datetime import datetime

def generate_flood_polygons(river_coords, intensity=5):
    """
    Симулирует зоны затопления вокруг русла реки.
    """
    flood_zones = []
    for i in range(len(river_coords) - 1):
        p1 = river_coords[i]
        p2 = river_coords[i+1]
        
        # Создаем случайный полигон вокруг сегмента реки
        offset_x = random.uniform(0.001, intensity / 1000)
        offset_y = random.uniform(0.001, intensity / 1000)
        
        polygon = [
            [p1[0], p1[1]],
            [p1[0] + offset_x, p1[1] + offset_y],
            [p2[0] + offset_x, p2[1] + offset_y],
            [p2[0], p2[1]]
        ]
        flood_zones.append(polygon)
    return flood_zones

def mint_flood_nft(flood_data):
    """
    Создает уникальный NFT на основе геоданных паводка.
    """
    # Создаем строку из координат для хеширования
    data_string = json.dumps(flood_data, sort_keys=True)
    nft_id = hashlib.sha256(data_string.encode()).hexdigest()
    
    nft_metadata = {
        "token_id": nft_id,
        "asset_name": "Kumbel River Flood Event NFT",
        "timestamp": datetime.now().isoformat(),
        "properties": {
            "flood_intensity": "High",
            "region": "Kumbel River Basin",
            "geometry_hash": nft_id[:16]
        },
        "description": "Unique digital asset generated from the geospatial footprint of the Kumbel river flood."
    }
    return nft_metadata

# 1. Координаты русла реки Кумбель (упрощенная аппроксимация для примера)
# В реальном проекте здесь будет загрузка GeoJSON или Shapefile
kumbel_river_line = [
    [47.123, 45.456],
    [47.135, 45.470],
    [47.150, 45.485],
    [47.170, 45.510],
    [47.190, 45.530],
    [47.210, 45.550]
]

# 2. Генерация зон затопления
flood_polygons = generate_flood_polygons(kumbel_river_line, intensity=random.randint(10, 50))

# 3. "Минтинг" NFT
nft_asset = mint_flood_nft(flood_polygons)
print("--- NFT Successfully Minted ---")
print(json.dumps(nft_asset, indent=4))

# 4. Визуализация на карте
# Центрируем карту на среднем значении координат
center_lat = sum([p[0] for p in kumbel_river_line]) / len(kumbel_river_line)
center_lon = sum([p[1] for p in kumbel_river_line]) / len(kumbel_river_line)

m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB dark_matter')

# Отрисовка русла реки
folium.PolyLine(kumbel_river_line, color="cyan", weight=3, opacity=0.8, tooltip="Kumbel River").add_to(m)

# Отрисовка зон затопления
for poly in flood_polygons:
    folium.Polygon(
        locations=poly,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.4,
        popup=f"Flood Zone ID: {nft_asset['token_id'][:8]}"
    ).add_to(m)

# Добавление маркера с информацией об NFT
folium.Marker(
    location=[center_lat, center_lon],
    popup=f"NFT Asset: {nft_asset['token_id'][:12]}...<br>Event: Kumbel Flood",
    icon=folium.Icon(color='gold', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("233.html")
print("\nMap has been saved as 233.html")