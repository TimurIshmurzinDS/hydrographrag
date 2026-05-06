import numpy as np
import pandas as pd
import folium
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# 1. Настройка данных: Города и их координаты
stations = {
    "Moscow": [55.7558, 37.6173],
    "New York": [40.7128, -74.0060],
    "Tokyo": [35.6895, 139.6917],
    "London": [51.5074, -0.1278],
    "Sydney": [-33.8688, 151.2093],
    "Cairo": [30.0444, 31.2357]
}

def generate_weather_data(days=30):
    """Генерация синтетических данных температуры с сезонностью и шумом"""
    x = np.arange(days).reshape(-1, 1)
    # Базовая температура + синусоида (сезонность) + случайный шум
    temp = 15 + 10 * np.sin(x / 5) + np.random.normal(0, 2, size=(days, 1))
    return x, temp

def historical_forecast(x, y):
    """Имитация исторического метода: простая линейная экстраполяция последних 3 дней"""
    # Берем последние 3 точки для предсказания следующей
    model = LinearRegression()
    model.fit(x[-3:], y[-3:])
    prediction = model.predict([[x[-1][0] + 1]])
    return prediction[0][0]

def modern_forecast(x, y):
    """Имитация современного метода: учет нелинейности и тренда (полином)"""
    # Используем полиномиальную регрессию 2-го порядка для имитации сложности NWP
    p = np.polyfit(x.flatten(), y.flatten(), 2)
    prediction = np.polyval(p, x[-1][0] + 1)
    return prediction

# 2. Основной цикл расчетов
results = []

for city, coords in stations.items():
    x, y = generate_weather_data()
    
    # Реальные значения (для симуляции возьмем следующее значение из сгенерированного ряда)
    # Чтобы сравнить, создадим "истинное" значение, которое мы пытаемся предсказать
    true_val = 15 + 10 * np.sin((x[-1][0] + 1) / 5) + np.random.normal(0, 1)
    
    # Прогнозы
    hist_pred = historical_forecast(x, y)
    mod_pred = modern_forecast(x, y)
    
    # Ошибки
    hist_error = abs(true_val - hist_pred)
    mod_error = abs(true_val - mod_pred)
    
    results.append({
        "city": city,
        "coords": coords,
        "hist_err": round(hist_error, 2),
        "mod_err": round(mod_error, 2),
        "improvement": round(hist_error - mod_error, 2)
    })

# 3. Визуализация на карте
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

for res in results:
    color = "green" if res["improvement"] > 0 else "red"
    
    popup_text = (
        f"<b>City:</b> {res['city']}<br>"
        f"Historical Error: {res['hist_err']}°C<br>"
        f"Modern Error: {res['mod_err']}°C<br>"
        f"<b>Accuracy Gain:</b> {res['improvement']}°C"
    )
    
    folium.CircleMarker(
        location=res["coords"],
        radius=10,
        popup=folium.Popup(popup_text, max_width=200),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("281.html")

print("Modeling complete. The comparison map has been saved as 281.html")