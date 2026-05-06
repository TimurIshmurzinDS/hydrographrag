import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

def calculate_volatility(data):
    """Вычисляет коэффициент вариации (CV) для ряда данных."""
    mean = np.mean(data)
    std_dev = np.std(data)
    cv = (std_dev / mean) * 100 if mean != 0 else 0
    return mean, std_dev, cv

def generate_river_data(river_name, base_flow, volatility_factor, years=10):
    """
    Генерирует синтетические данные стока с учетом сезонности.
    volatility_factor: множитель для имитации разной изменчивости.
    """
    np.random.seed(42 if river_name == "Kishi Almaty" else 7)
    days = years * 365
    time = np.arange(days)
    
    # Создаем сезонный цикл (синусоида) + случайный шум
    seasonal_pattern = np.sin(2 * np.pi * time / 365) * (base_flow * 0.5)
    noise = np.random.normal(0, base_flow * volatility_factor, days)
    
    flow = base_flow + seasonal_pattern + noise
    # Сток не может быть отрицательным
    flow = np.maximum(flow, 0.1) 
    
    return flow

# 1. Подготовка данных
rivers_config = {
    "Bayankol River": {"coords": [43.2, 78.5], "base_flow": 15.0, "vol_factor": 0.6},
    "Kishi Almaty River": {"coords": [43.1, 77.1], "base_flow": 25.0, "vol_factor": 0.3}
}

results = {}

for river, config in rivers_config.items():
    # Генерируем данные за 10 лет
    data = generate_river_data(river, config["base_flow"], config["vol_factor"])
    mean, std, cv = calculate_volatility(data)
    results[river] = {"mean": mean, "std": std, "cv": cv, "coords": config["coords"]}

# 2. Определение, где волатильность выше
bayankol_cv = results["Bayankol River"]["cv"]
kishi_almaty_cv = results["Kishi Almaty River"]["cv"]

if bayankol_cv > kishi_almaty_cv:
    conclusion = f"Волатильность стока в Bayankol River выше ({bayankol_cv:.2f}%) чем в Kishi Almaty River ({kishi_almaty_cv:.2f}%)."
else:
    conclusion = f"Волатильность стока в Kishi Almaty River выше ({kishi_almaty_cv:.2f}%) чем в Bayankol River ({bayankol_cv:.2f}%)."

print(conclusion)

# 3. Визуализация на карте
# Центрируем карту между двумя реками
m = folium.Map(location=[43.15, 77.8], zoom_start=7, tiles="CartoDB positron")

for river, res in results.items():
    popup_text = (
        f"<b>{river}</b><br>"
        f"Средний сток: {res['mean']:.2f} м³/с<br>"
        f"Станд. отклонение: {res['std']:.2f}<br>"
        f"Коэф. вариации (CV): {res['cv']:.2f}%"
    )
    
    folium.Marker(
        location=res["coords"],
        popup=popup_text,
        tooltip=river,
        icon=folium.Icon(color="blue" if "Bayankol" in river else "green", icon="info-sign")
    ).add_to(m)

# Добавляем текстовое заключение на карту в виде всплывающего окна или просто сохраняем
# Для простоты добавим вывод в консоль, а на карту - маркеры с данными.
m.save("134.html")