import folium

# Координаты реки Киши Осек (примерные)
kishi_oshek_coords = [42.8516, 74.5930]

# Создание карты с центром в месте реки Киши Осек
m = folium.Map(location=kishi_oshek_coords, zoom_start=12)

# Добавление маркера для реки Киши Осек
folium.Marker(
    location=kishi_oshek_coords,
    popup="Река Киши Осек",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("261.html")

# Простая симуляция процесса кислородного консервирования овощей

def simulate_fermentation(days):
    """
    Симулирует процесс ферментации овощей на протяжении заданного количества дней.
    
    :param days: Количество дней, в течение которых происходит ферментация
    :return: Состояние продукта после ферментации
    """
    initial_acidity = 0.0  # Начальная кислотность (в pH)
    target_acidity = 4.5   # Целевая кислотность для консервирования
    
    for day in range(1, days + 1):
        # Увеличение кислотности каждый день
        initial_acidity += 0.2
        
        if initial_acidity >= target_acidity:
            print(f"Процесс ферментации завершен на {day}-й день.")
            break
    
    if initial_acidity < target_acidity:
        print("Процесс ферментации не завершен за заданный период времени.")
    
    return initial_acidity

# Запуск симуляции на 10 дней
final_acidity = simulate_fermentation(10)
print(f"Конечная кислотность продукта: {final_acidity:.2f} pH")