import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import folium

# =============================================================================
# 1. Генерация синтетических данных (имитация исторических данных)
# =============================================================================
# В реальном сценарии здесь будет загрузка из CSV или API (например, ERA5 или гидропосты)
np.random.seed(42)
dates = pd.date_range(start="2000-01-01", end="2023-12-31", freq='M')
n = len(dates)

def generate_river_data(base_precip, correlation_strength=0.7):
    # Осадки: случайные значения с сезонностью
    precip = base_precip + 20 * np.sin(np.linspace(0, 2 * np.pi * (n/12), n)) + np.random.normal(0, 10, n)
    # Сток: зависит от осадков с некоторым шумом и задержкой (лаг 1 месяц)
    discharge = np.roll(precip * correlation_strength, 1) + np.random.normal(0, 5, n)
    return precip, discharge

# Данные для реки Уржар
precip_urzhar, flow_urzhar = generate_river_data(50)
# Данные для реки Быжи
precip_byzhy, flow_byzhy = generate_river_data(40)

df = pd.DataFrame({
    'Date': dates,
    'Precip_Urzhar': precip_urzhar,
    'Flow_Urzhar': flow_urzhar,
    'Precip_Byzhy': precip_byzhy,
    'Flow_Byzhy': flow_byzhy
})

# =============================================================================
# 2. Статистический анализ корреляции
# =============================================================================
corr_urzhar, p_urzhar = pearsonr(df['Precip_Urzhar'], df['Flow_Urzhar'])
corr_byzhy, p_byzhy = pearsonr(df['Precip_Byzhy'], df['Flow_Byzhy'])

print(f"Correlation Urzhar: {corr_urzhar:.3f} (p-value: {p_urzhar:.3f})")
print(f"Correlation Byzhy: {corr_byzhy:.3f} (p-value: {p_byzhy:.3f})")

# =============================================================================
# 3. Визуализация временных рядов
# =============================================================================
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['Precip_Urzhar'], color='blue', label='Precipitation (Urzhar)')
plt.ylabel('Precipitation (mm)')
plt.legend(loc='upper left')
ax1 = plt.gca()
ax2 = ax1.twinx()
ax2.plot(df['Date'], df['Flow_Urzhar'], color='green', label='Discharge (Urzhar)')
ax2.set_ylabel('Discharge (m3/s)')
ax2.legend(loc='upper right')
plt.title('Hydrological Dynamics: Urzhar River')

plt.subplot(2, 1, 2)
plt.plot(df['Date'], df['Precip_Byzhy'], color='blue', label='Precipitation (Byzhy)')
plt.ylabel('Precipitation (mm)')
plt.legend(loc='upper left')
ax3 = plt.gca()
ax4 = ax3.twinx()
ax4.plot(df['Date'], df['Flow_Byzhy'], color='green', label='Discharge (Byzhy)')
ax4.set_ylabel('Discharge (m3/s)')
ax4.legend(loc='upper right')
plt.title('Hydrological Dynamics: Byzhy River')

plt.tight_layout()
plt.savefig("hydrology_analysis.png")
plt.show()

# =============================================================================
# 4. Геопространственная визуализация (Folium)
# =============================================================================
# Примерные координаты рек в Западном Казахстане
locations = {
    "Urzhar River": [51.2, 66.5, corr_urzhar],
    "Byzhy River": [51.0, 67.2, corr_byzhy]
}

m = folium.Map(location=[51.1, 66.8], zoom_start=7, tiles='OpenStreetMap')

for name, data in locations.items():
    folium.Marker(
        location=[data[0], data[1]],
        popup=f"<b>{name}</b><br>Correlation (P vs Q): {data[2]:.3f}",
        tooltip=name,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты строго по требованию
m.save("199.html")

print("Analysis complete. Map saved as 199.html")