import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from scipy.stats import pearsonr
from datetime import datetime, timedelta

# =============================================================================
# 1. Симуляция данных (так как реальные данные гидропостов закрыты)
# =============================================================================
def generate_river_data(river_name, seed):
    np.random.seed(seed)
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
    
    # Симуляция снегозапаса (пик в феврале, спад в апреле-мае)
    snow_depth = 50 * np.exp(-( (dates.dayofyear - 60)**2 ) / 1000) + np.random.normal(0, 2, len(dates))
    snow_depth = np.maximum(0, snow_depth)
    
    # Симуляция расхода воды (паводок следует за таянием с лагом в 10-20 дней)
    # Сдвигаем пик снеготаяния для создания паводка
    discharge = 10 * np.exp(-( (dates.dayofyear - 110)**2 ) / 500) + 5 + np.random.normal(0, 1, len(dates))
    discharge = np.maximum(5, discharge)
    
    return pd.DataFrame({'date': dates, 'snow_depth': snow_depth, 'discharge': discharge, 'river': river_name})

# Создаем данные для двух рек
df_bayankol = generate_river_data("Bayankol", 42)
df_lepsy = generate_river_data("Lepsy", 84)

# =============================================================================
# 2. Анализ корреляции с учетом лага
# =============================================================================
def analyze_correlation(df):
    river = df['river'].iloc[0]
    best_lag = 0
    max_corr = -1
    
    # Ищем оптимальный лаг (от 0 до 30 дней)
    for lag in range(0, 31):
        corr, _ = pearsonr(df['snow_depth'].shift(lag), df['discharge'])
        if abs(corr) > abs(max_corr):
            max_corr = corr
            best_lag = lag
            
    return river, best_lag, max_corr

res_bayankol = analyze_correlation(df_bayankol)
res_lepsy = analyze_correlation(df_lepsy)

print(f"River {res_bayankol[0]}: Lag = {res_bayankol[1]} days, Correlation = {res_bayankol[2]:.2f}")
print(f"River {res_lepsy[0]}: Lag = {res_lepsy[1]} days, Correlation = {res_lepsy[2]:.2f}")

# =============================================================================
# 3. Визуализация временных рядов
# =============================================================================
plt.figure(figsize=(12, 6))
for df, res in [(df_bayankol, res_bayankol), (df_lepsy, res_lepsy)]:
    plt.plot(df['date'], df['discharge'], label=f"{res[0]} Discharge")
    plt.plot(df['date'], df['snow_depth'], linestyle='--', label=f"{res[0]} Snow Depth")

plt.title("Correlation between Snowmelt and River Discharge")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.savefig("correlation_plot.png")
plt.close()

# =============================================================================
# 4. Геопространственная визуализация (Folium)
# =============================================================================
# Координаты рек (приблизительные для региона Жетысу, Казахстан)
locations = {
    "Bayankol River": [44.5, 82.0],
    "Lepsy River": [44.2, 80.5]
}

# Создание карты
m = folium.Map(location=[44.3, 81.2], zoom_start=7, tiles="CartoDB positron")

for river, coords in locations.items():
    # Добавляем маркер для каждой реки
    folium.Marker(
        location=coords,
        popup=f"River: {river}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # Рисуем условную зону водосбора (круг)
    folium.Circle(
        location=coords,
        radius=20000, 
        color="blue",
        fill=True,
        fill_opacity=0.2,
        popup=f"Catchment area of {river}"
    ).add_to(m)

# Сохранение карты строго по условию
m.save("162.html")

print("Analysis complete. Map saved as 162.html and plot as correlation_plot.png")