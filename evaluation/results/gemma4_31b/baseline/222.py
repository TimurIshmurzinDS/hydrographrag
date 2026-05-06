import folium
import random

def get_pasta_recipe():
    """Возвращает инструкцию по приготовлению пасты."""
    recipe = (
        "\n--- 🍝 ИНСТРУКЦИЯ ПО ПРИГОТОВЛЕНИЮ ПАСТЫ (Протокол Аномалии) ---\n"
        "1. Вскипятите большое количество воды в кастрюле.\n"
        "2. Добавьте щепотку соли (соль должна быть как морская вода).\n"
        "3. Поместите пасту в кипящую воду и варите согласно инструкции на упаковке (обычно 8-12 мин).\n"
        "4. Для состояния 'Al Dente' выключите огонь за 1-2 минуты до готовности.\n"
        "5. Слейте воду, оставив немного для соуса.\n"
        "6. Смешайте с любимым соусом (Песто, Болоньезе или просто с маслом и сыром).\n"
        "7. Приятного аппетита! Аномалия на реке Каратал больше не вызывает тревоги.\n"
        "------------------------------------------------------------------"
    )
    return recipe

def main():
    # Координаты датчиков вдоль реки Каратал (примерные точки)
    sensors_data = [
        {"id": "SN-01", "lat": 42.65, "lon": 78.10, "value": 0},
        {"id": "SN-02", "lat": 42.72, "lon": 78.35, "value": 0},
        {"id": "SN-03", "lat": 42.80, "lon": 78.60, "value": 0},
        {"id": "SN-04", "lat": 42.88, "lon": 78.85, "value": 0},
        {"id": "SN-05", "lat": 42.95, "lon": 79.10, "value": 0},
    ]

    # Порог аномалии
    THRESHOLD = 80
    anomaly_found = False

    # Симуляция показаний датчиков
    for sensor in sensors_data:
        sensor["value"] = random.randint(20, 100)
        if sensor["value"] > THRESHOLD:
            sensor["status"] = "Anomaly"
            anomaly_found = True
        else:
            sensor["status"] = "Normal"

    # Проверка условия: если есть аномалия -> готовим пасту
    if anomaly_found:
        print("⚠️ ОБНАРУЖЕНА АНОМАЛИЯ НА ДАТЧИКАХ РЕКИ КАРАТАЛ!")
        print(get_pasta_recipe())
    else:
        print("✅ Все датчики в норме. Паста сегодня не предусмотрена.")

    # Визуализация на карте
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[42.8, 78.6], zoom_start=8)

    for sensor in sensors_data:
        color = "red" if sensor["status"] == "Anomaly" else "green"
        folium.CircleMarker(
            location=[sensor["lat"], sensor["lon"]],
            radius=8,
            popup=f"Sensor: {sensor['id']}<br>Value: {sensor['value']}<br>Status: {sensor['status']}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

    # Сохранение карты строго в файл 222.html
    m.save("222.html")
    print("\nКарта с состоянием датчиков сохранена в файл '222.html'.")

if __name__ == "__main__":
    main()