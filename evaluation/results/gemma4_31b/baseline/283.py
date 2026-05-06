import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from sklearn.metrics import mean_squared_error

def compare_time_series(ts1, ts2, name1="Station A", name2="Station B"):
    """
    Функция для сравнения двух временных рядов.
    ts1, ts2: Pandas Series с DatetimeIndex.
    """
    # 1. Синхронизация индексов (объединение по общему времени)
    df = pd.concat([ts1, ts2], axis=1)
    df.columns = [name1, name2]
    df = df.dropna() # Удаляем пропуски для корректного расчета

    # 2. Расчет метрик
    correlation = df[name1].corr(df[name2])
    rmse = np.sqrt(mean_squared_error(df[name1], df[name2]))
    mean_diff = (df[name1] - df[name2]).mean()

    print(f"--- Сравнение: {name1} vs {name2} ---")
    print(f"Корреляция Пирсона: {correlation:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Средняя разность: {mean_diff:.4f}\n")

    # 3. Визуализация графиков
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[name1], label=name1, color='blue')
    plt.plot(df.index, df[name2], label=name2, color='red')
    plt.title(f"Сравнение временных рядов: {name1} и {name2}")
    plt.xlabel("Дата")
    plt.ylabel("Значение")
    plt.legend()
    plt.grid(True)
    plt.show()

    return {"correlation": correlation, "rmse": rmse, "mean_diff": mean_diff}

# ==========================================
# Имитация данных (Геопространственный контекст)
# ==========================================

# Создаем временной интервал (30 дней)
dates = pd.date_range(start="2023-01-01", periods=30, freq='D')

# Имитируем данные температуры для двух городов (например, Москва и Санкт-Петербург)
# Москва: более высокая амплитуда
np.random.seed(42)
moscow_temp = pd.Series(np.random.normal(loc=-5, scale=3, size=30), index=dates)
# СПб: более стабильная температура, коррелирует с Москвой, но со смещением
spb_temp = moscow_temp * 0.7 + np.random.normal(loc=2, scale=1, size=30)
spb_temp = pd.Series(spb_temp, index=dates)

# Координаты станций
coords = {
    "Moscow": [55.7558, 37.6173],
    "St. Petersburg": [59.9342, 30.3351]
}

# Вызов функции сравнения
metrics = compare_time_series(moscow_temp, spb_temp, "Moscow", "St. Petersburg")

# ==========================================
# Визуализация на карте (Folium)
# ==========================================

# Создаем карту, центрированную между городами
m = folium.Map(location=[57.8, 34.0], zoom_start=5)

# Добавляем маркеры станций
for city, coord in coords.items():
    folium.Marker(
        location=coord,
        popup=f"{city} Station",
        icon=folium.Icon(color='blue' if city == "Moscow" else 'red')
    ).add_to(m)

# Добавляем линию между станциями для визуализации связи
folium.PolyLine(
    locations=[coords["Moscow"], coords["St. Petersburg"]],
    color="gray",
    weight=2,
    dash_array='5, 5',
    tooltip="Comparison Link"
).add_to(m)

# Сохранение карты
m.save("283.html")
print("Карта сохранена в файл 283.html")