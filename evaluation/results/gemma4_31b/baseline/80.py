import folium
import pandas as pd

def assess_flood_risk(discharge_tokyraun, level_koktal):
    """
    Оценка риска затопления на основе показателей двух рек.
    """
    # Пороговые значения (условные)
    THRESHOLD_DISCHARGE_TOKYRAUN = 150.0  # м3/с
    THRESHOLD_LEVEL_KOKTAL = 5.5         # метры
    
    if discharge_tokyraun > THRESHOLD_DISCHARGE_TOKYRAUN and level_koktal > THRESHOLD_LEVEL_KOKTAL:
        return "High", "red"
    elif discharge_tokyraun > THRESHOLD_DISCHARGE_TOKYRAUN or level_koktal > THRESHOLD_LEVEL_KOKTAL:
        return "Medium", "orange"
    else:
        return "Low", "green"

# 1. Имитация данных гидрологических станций
# Координаты подобраны условно для демонстрации GIS-функционала
data = {
    'river': ['Tokyraun River', 'Koktal River'],
    'lat': [42.5123, 42.5567], 
    'lon': [77.1234, 77.1890],
    'value': [165.5, 5.8], # Расход для Tokyraun, Уровень для Koktal
    'unit': ['m3/s', 'm']
}

df = pd.DataFrame(data)

# Извлекаем значения для анализа
val_tokyraun = df[df['river'] == 'Tokyraun River']['value'].values[0]
val_koktal = df[df['river'] == 'Koktal River']['value'].values[0]

# 2. Оценка риска
risk_level, risk_color = assess_flood_risk(val_tokyraun, val_koktal)

# 3. Визуализация на карте
# Центрируем карту между двумя точками
m = folium.Map(location=[42.5345, 77.1562], zoom_start=12, tiles='OpenStreetMap')

for index, row in df.iterrows():
    # Определяем текст для всплывающего окна
    popup_text = f"River: {row['river']}<br>Value: {row['value']} {row['unit']}<br>Overall Risk: {risk_level}"
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=popup_text,
        tooltip=f"Station: {row['river']}",
        icon=folium.Icon(color=risk_color, icon='info-sign')
    ).add_to(m)

# Добавление общего индикатора риска в заголовок карты
folium.plugins.Tooltip(
    # В folium нет прямого текстового заголовка, поэтому добавим через HTML-элемент или просто в описание
).add_to(m)

# Сохранение карты
m.save("80.html")

print(f"Analysis Complete. Risk Level: {risk_level}. Map saved as 80.html")