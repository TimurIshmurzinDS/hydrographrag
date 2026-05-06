import folium

# 1. Подготовка данных
# В реальном сценарии данные могут быть загружены из CSV или API
# Координаты указаны приблизительно для демонстрации GIS-логики
rivers_data = [
    {
        "name": "Karaoy River",
        "coords": [43.25, 77.12], 
        "current_level": 5.8, 
        "threshold": 4.5, 
        "unit": "m"
    },
    {
        "name": "Temirlik River",
        "coords": [43.30, 77.25], 
        "current_level": 2.1, 
        "threshold": 3.0, 
        "unit": "m"
    },
    {
        "name": "Turgen River",
        "coords": [43.15, 77.40], 
        "current_level": 6.2, 
        "threshold": 4.0, 
        "unit": "m"
    }
]

def analyze_flood_risk(data):
    """
    Анализирует уровень воды и определяет наличие опасного роста.
    """
    results = []
    for river in data:
        is_dangerous = river['current_level'] > river['threshold']
        status = "ОПАСНО" if is_dangerous else "Норма"
        results.append({
            **river,
            "status": status,
            "is_dangerous": is_dangerous
        })
    return results

# 2. Выполнение анализа
analyzed_rivers = analyze_flood_risk(rivers_data)

# 3. Визуализация на карте
# Создаем карту, центрированную в районе исследуемых рек
m = folium.Map(location=[43.22, 77.25], zoom_start=9, tiles='OpenStreetMap')

for river in analyzed_rivers:
    # Определяем цвет маркера в зависимости от статуса
    color = 'red' if river['is_dangerous'] else 'green'
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Река:</b> {river['name']}<br>"
        f"<b>Уровень:</b> {river['current_level']} {river['unit']}<br>"
        f"<b>Порог:</b> {river['threshold']} {river['unit']}<br>"
        f"<b>Статус:</b> {river['status']}"
    )
    
    # Добавление маркера на карту
    folium.Marker(
        location=river['coords'],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# 4. Сохранение результата
m.save("86.html")

# Вывод текстового отчета в консоль
print("Анализ завершен. Результаты:")
for r in analyzed_rivers:
    print(f"Река {r['name']}: {r['status']} (Уровень: {r['current_level']}, Порог: {r['threshold']})")
print("\nКарта сохранена в файл 86.html")