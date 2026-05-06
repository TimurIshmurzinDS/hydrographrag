import folium
import pandas as pd

# 1. Подготовка данных
# Координаты являются приблизительными для демонстрации геопространственного моделирования
data = {
    'River': ['Kurty River', 'Urzhar River', 'Byzhy River'],
    'Latitude': [49.45, 49.12, 48.78], 
    'Longitude': [81.10, 82.35, 81.65],
    'Consumption_Value': [15, 42, 68]  # Условные значения водопотребления
}

df = pd.DataFrame(data)

# 2. Функция для определения уровня и цвета
def get_consumption_level(value):
    if value <= 20:
        return 'Low', 'green'
    elif value <= 50:
        return 'Medium', 'orange'
    else:
        return 'High', 'red'

# 3. Создание карты
# Центрируем карту в районе расположения рек (Казахстан)
m = folium.Map(location=[49.1, 81.8], zoom_start=7, control_scale=True)

# 4. Добавление данных на карту
for index, row in df.iterrows():
    level, color = get_consumption_level(row['Consumption_Value'])
    
    # Создаем всплывающее окно с информацией
    popup_text = (
        f"<b>River:</b> {row['River']}<br>"
        f"<b>Consumption:</b> {row['Consumption_Value']} units<br>"
        f"<b>Level:</b> {level}"
    )
    
    # Добавляем маркер на карту
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=10,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 5. Сохранение результата
m.save("112.html")

print("Modeling complete. The map has been saved as 112.html")