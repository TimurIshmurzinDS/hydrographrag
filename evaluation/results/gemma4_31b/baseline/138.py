import folium
import pandas as pd

def get_water_levels():
    """
    Имитация получения данных с гидрологических постов.
    В реальном сценарии здесь будет запрос к API или парсинг данных.
    """
    # Данные: Название реки, Широта, Долгота, Текущий уровень (м)
    data = {
        'river': ['Лепсы', 'Бутак'],
        'lat': [43.4521, 43.3115], 
        'lon': [79.5123, 79.2456],
        'level': [2.45, 1.82]  # Текущие уровни воды в метрах
    }
    return pd.DataFrame(data)

def analyze_levels(df):
    """
    Проведение сравнительного анализа уровней воды.
    """
    lepsy_val = df[df['river'] == 'Лепсы']['level'].values[0]
    butak_val = df[df['river'] == 'Бутак']['level'].values[0]
    
    diff = abs(lepsy_val - butak_val)
    higher_river = 'Лепсы' if lepsy_val > butak_val else 'Бутак'
    
    print(f"--- Сравнительный анализ ---")
    print(f"Уровень р. Лепсы: {lepsy_val} м")
    print(f"Уровень р. Бутак: {butak_val} м")
    print(f"Разница: {diff:.2f} м")
    print(f"Река с более высоким уровнем: {higher_river}")
    print(f"---------------------------")

def create_map(df):
    """
    Визуализация данных на карте.
    """
    # Центрируем карту между двумя точками
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles='OpenStreetMap')

    for index, row in df.iterrows():
        # Определяем цвет маркера в зависимости от уровня (условно > 2.0м - желтый)
        color = 'orange' if row['level'] > 2.0 else 'blue'
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"Река: {row['river']}<br>Уровень: {row['level']} м",
            tooltip=row['river'],
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    # Сохранение карты строго в файл 138.html
    m.save("138.html")
    print("Карта успешно сохранена в файл 138.html")

if __name__ == "__main__":
    # 1. Получение данных
    water_data = get_water_levels()
    
    # 2. Анализ
    analyze_levels(water_data)
    
    # 3. Визуализация
    create_map(water_data)