import folium

# Карта с местом сбора образца ила
m = folium.Map(location=[43.21, 76.85], zoom_start=12)

folium.Marker(location=[43.21, 76.85], popup="Место сбора образца ила").add_to(m)
m.save("260.html")

# Моделирование процесса компостирования (упрощенная версия)
def composting(material):
    nutrients = material["initial_nutrients"]
    temperature = 50  # Цель: поддерживать температуру в диапазоне 50-60°C

    for i in range(1, 180): # Моделирование за 6 месяцев (180 дней)
        temperature += 0.5 if temperature < 55 else -0.5  # Упрощенное моделирование температуры

        nutrients["nitrogen"] *= 0.95 # Потеря питательных веществ со временем
        nutrients["phosphorus"] *= 0.98
        nutrients["potassium"] *= 0.96

    return nutrients

initial_nutrients = {"nitrogen": 10, "phosphorus": 5, "potassium": 2}
final_nutrients = composting(initial_nutrients)

print("Final nutrient content:", final_nutrients)