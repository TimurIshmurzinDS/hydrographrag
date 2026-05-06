import folium
import geopandas as gpd
from shapely.geometry import LineString

def calculate_water_volume():
    # 1. Исходные данные: Координаты рек (упрощенно для демонстрации)
    # Координаты подобраны приблизительно для региона Казахстана
    rivers_data = {
        "Sarykan River": {
            "coords": [[48.5, 68.2], [48.6, 68.4], [48.7, 68.5]], 
            "flow_rate": 2.5,  # Средний расход м3/с
            "color": "blue"
        },
        "Temirlik River": {
            "coords": [[48.4, 68.1], [48.3, 68.3], [48.2, 68.4]], 
            "flow_rate": 1.8,  # Средний расход м3/с
            "color": "cyan"
        }
    }

    # 2. Параметры поливного сезона
    irrigation_days = 120  # Длительность сезона в днях
    seconds_in_day = 24 * 60 * 60
    total_seconds = irrigation_days * seconds_in_day

    total_volume_all = 0
    river_volumes = {}

    # 3. Расчет объема воды
    for river_name, data in rivers_data.items():
        # Объем = Расход * Время
        volume_m3 = data["flow_rate"] * total_seconds
        volume_mln_m3 = volume_m3 / 1_000_000  # Перевод в млн м3
        
        river_volumes[river_name] = volume_mln_m3
        total_volume_all += volume_mln_m3

    print(f"Расчетный объем воды для полива за {irrigation_days} дней:")
    for river, vol in river_volumes.items():
        print(f"- {river}: {vol:.2f} млн м3")
    print(f"ИТОГО: {total_volume_all:.2f} млн м3")

    # 4. Визуализация на карте
    # Центрируем карту в районе рек
    m = folium.Map(location=[48.45, 68.3], zoom_start=9, tiles="CartoDB positron")

    for river_name, data in rivers_data.items():
        # Добавление линии реки
        folium.PolyLine(
            locations=data["coords"], 
            color=data["color"], 
            weight=5, 
            opacity=0.8, 
            tooltip=f"{river_name}: {river_volumes[river_name]:.2f} млн м3"
        ).add_to(m)
        
        # Добавление маркера в начале реки
        folium.Marker(
            location=data["coords"][0], 
            popup=f"<b>{river_name}</b><br>Объем: {river_volumes[river_name]:.2f} млн м3",
            icon=folium.Icon(color="blue" if data["color"] == "blue" else "cadetblue")
        ).add_to(m)

    # Сохранение карты
    m.save("118.html")
    print("\nКарта успешно сохранена в файл 118.html")

if __name__ == "__main__":
    calculate_water_volume()