import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import folium

# 1. Генерация синтетических данных для анализа (имитация гидрологических наблюдений)
# В реальном сценарии здесь будет загрузка CSV или запрос к API гидропостов
np.random.seed(42)
dates = pd.date_range(start="2000-01-01", end="2023-12-31", freq='M')
n_months = len(dates)

def generate_water_levels(trend_slope, noise_level=0.5):
    # Сезонность (синусоида) + Линейный тренд + Случайный шум
    seasonality = 2 * np.sin(2 * np.pi * np.arange(n_months) / 12)
    trend = trend_slope * np.arange(n_months)
    noise = np.random.normal(0, noise_level, n_months)
    return 5 + seasonality + trend + noise

# Река Лепсы: умеренный нисходящий тренд (например, из-за изменения климата/отбора воды)
lepsy_levels = generate_water_levels(-0.005) 
# Река Турген: небольшой восходящий тренд (например, из-за таяния ледников)
turgen_levels = generate_water_levels(0.008)

df = pd.DataFrame({
    'Date': dates,
    'Lepsy': lepsy_levels,
    'Turgen': turgen_levels
})

# 2. Анализ трендов с помощью линейной регрессии
def analyze_trend(series):
    x = np.arange(len(series))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, series)
    return slope, p_value

lepsy_slope, lepsy_p = analyze_trend(df['Lepsy'])
turgen_slope, turgen_p = analyze_trend(df['Turgen'])

print(f"Lepsy River: Slope={lepsy_slope:.4f}, p-value={lepsy_p:.4f}")
print(f"Turgen River: Slope={turgen_slope:.4f}, p-value={turgen_p:.4f}")

# 3. Визуализация временных рядов
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Lepsy'], label='Lepsy River', color='blue', alpha=0.6)
plt.plot(df['Date'], df['Turgen'], label='Turgen River', color='green', alpha=0.6)

# Добавление линий тренда
def add_trendline(x, y, color, label):
    z = np.polyfit(range(len(x)), y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(range(len(x))), color=color, linewidth=3, label=f"{label} Trend")

add_trendline(df['Date'], df['Lepsy'], 'darkblue', 'Lepsy')
add_trendline(df['Date'], df['Turgen'], 'darkgreen', 'Turgen')

plt.title("Long-term Water Level Trends in Lepsy and Turgen Basins")
plt.xlabel("Year")
plt.ylabel("Water Level (m)")
plt.legend()
plt.grid(True)
plt.show()

# 4. Геопространственная визуализация (Folium)
# Координаты (приблизительные для демонстрации)
locations = {
    "Lepsy River": [43.2, 78.5, lepsy_slope],
    "Turgen River": [43.1, 77.5, turgen_slope]
}

m = folium.Map(location=[43.15, 78.0], zoom_start=8, tiles='OpenStreetMap')

for river, data in locations.items():
    slope = data[2]
    trend_text = "Increasing" if slope > 0 else "Decreasing"
    color = 'green' if slope > 0 else 'red'
    
    folium.Marker(
        location=[data[0], data[1]],
        popup=f"<b>{river}</b><br>Trend: {trend_text}<br>Slope: {slope:.4f}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Сохранение карты строго под именем 198.html
m.save("198.html")
print("Map has been saved as 198.html")