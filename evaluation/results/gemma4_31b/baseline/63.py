import folium
import pandas as pd
import random

def get_byzhy_river_data():
    """
    Имитация получения данных из API гидропостов.
    В реальном сценарии здесь будет запрос к базе данных или REST API.
    """
    # Пример данных: Название поста, Широта, Долгота, Текущий уровень (м)
    # Координаты подобраны условно для демонстрации работы GIS-инструмента
    data = [
        {"station": "Byzhy-Upper", "lat": 54.1234, "lon": 35.4567, "level": 1.2},
        {"station": "Byzhy-Middle", "lat": 54.1567, "lon": 35.5678, "level": 2.5},
        {"station": "Byzhy-Lower", "lat": 54.1890, "lon": 35.6789, "level": 0.8},
        {"station": "Byzhy-Delta", "lat": 54.2100, "lon": 35.7800, "level": 3.1},
    ]
    return pd.DataFrame(data)

def get_color(level):
    """Определение цвета маркера в зависимости от уровня воды"""
    if level > 2.5:
        return 'red'    # Критический уровень
    elif level > 1.5:
        return 'orange' # Повышенный уровень
    else:
        return 'blue'   # Нормальный уровень

def main():
    # 1. Получение данных
    df = get_byzhy_river_data()
    
    # 2. Инициализация карты
    # Центрируем карту по средним координатам всех постов
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='OpenStreetMap')
    
    # 3. Добавление гидропостов на карту
    for index, row in df.iterrows():
        color = get_color(row['level'])
        
        popup_text = f"<b>Пост:</b> {row['station']}<br><b>Уровень воды:</b> {row['level']} м"
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=popup_text,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
    
    # 4. Сохранение результата
    m.save("63.html")
    print("Карта успешно создана и сохранена в файл 63.html")
    print("\nТекущие уровни воды на реке Byzhy River:")
    print(df[['station', 'level']].to_string(index=False))

if __name__ == "__main__":
    main()