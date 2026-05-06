import folium
from folium.plugins import MarkerCluster, AntPath
import random

def generate_karaoy_gis_model():
    # Координаты примерного расположения реки Караой (Центральная Азия/Казахстан регион)
    # Для демонстрации создаем синтетический массив координат русла реки
    river_coords = [
        [48.50, 67.10], [48.52, 67.15], [48.55, 67.18], 
        [48.58, 67.20], [48.62, 67.22], [48.65, 67.25],
        [48.68, 67.28], [48.72, 67.30], [48.75, 67.35]
    ]

    # 1. Создание базовой карты
    m = folium.Map(location=[48.62, 67.22], zoom_start=11, tiles='OpenStreetMap')

    # 2. Визуализация русла реки Караой
    folium.PolyLine(river_coords, color='blue', weight=5, opacity=0.8, tooltip="Река Караой").add_to(m)

    # 3. Моделирование точек сбора ила (Silt Extraction Points)
    # Ил собирается в изгибах реки (имитируем точки вдоль русла)
    extraction_points = []
    for i in range(len(river_coords) - 1):
        # Создаем точку с небольшим смещением от центра русла (береговая линия)
        lat = (river_coords[i][0] + river_coords[i+1][0]) / 2 + random.uniform(-0.01, 0.01)
        lon = (river_coords[i][1] + river_coords[i+1][1]) / 2 + random.uniform(-0.01, 0.01)
        extraction_points.append([lat, lon])

    # 4. Центр переработки удобрений (Processing Plant)
    processing_plant = [48.60, 67.32]
    folium.Marker(
        location=processing_plant,
        popup="Завод по производству органических удобрений",
        icon=folium.Icon(color='red', icon='industry', prefix='fa')
    ).add_to(m)

    # 5. Визуализация логистики и точек сбора
    marker_cluster = MarkerCluster().add_to(m)
    
    for idx, pt in enumerate(extraction_points):
        # Маркер точки сбора
        folium.Marker(
            location=pt,
            popup=f"Точка сбора ила №{idx+1}",
            icon=folium.Icon(color='green', icon='leaf')
        ).add_to(marker_cluster)

        # Путь от точки сбора до завода (логистическая модель)
        AntPath(
            locations=[pt, processing_plant],
            dash_array=[1, 10],
            color='gray',
            weight=2,
            opacity=0.6,
            tooltip=f"Транспортировка ила из точки {idx+1}"
        ).add_to(m)

    # 6. Зоны применения удобрений (Agricultural Zones)
    # Имитируем поля вокруг завода и реки
    agri_zones = [
        [48.55, 67.25], [48.65, 67.35], [48.70, 67.20], [48.58, 67.38]
    ]
    for zone in agri_zones:
        folium.Circle(
            location=zone,
            radius=2000,
            color='orange',
            fill=True,
            fill_color='yellow',
            fill_opacity=0.4,
            popup="Зона внесения удобрений"
        ).add_to(m)

    # Сохранение карты
    m.save("260.html")
    print("GIS model has been generated and saved as 260.html")

if __name__ == "__main__":
    generate_karaoy_gis_model()