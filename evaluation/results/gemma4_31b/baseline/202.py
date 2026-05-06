import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# 1. Симуляция ретроспективных данных о стоке (м3/год)
# В реальном сценарии здесь будет загрузка из CSV или базы данных
np.random.seed(42)
years = np.arange(2000, 2021)

# Эмуляция данных: Emel (более стабильная), Turgen (более изменчивая)
# Средний сток Emel: 50 млн м3, std: 10 млн м3
emel_discharge = np.random.normal(loc=50, scale=10, size=len(years))
# Средний сток Turgen: 30 млн м3, std: 15 млн м3
turgen_discharge = np.random.normal(loc=30, scale=15, size=len(years))

df = pd.DataFrame({
    'Year': years,
    'Emel_River': emel_discharge,
    'Turgen_River': turgen_discharge
})

# 2. Статистический анализ
def calculate_variability(data):
    mean = np.mean(data)
    std = np.std(data)
    cv = (std / mean) * 100 if mean != 0 else 0
    return mean, std, cv

mean_e, std_e, cv_e = calculate_variability(df['Emel_River'])
mean_t, std_t, cv_t = calculate_variability(df['Turgen_River'])

print(f"Emel River: Mean={mean_e:.2f}, Std={std_e:.2f}, CV={cv_e:.2f}%")
print(f"Turgen River: Mean={mean_t:.2f}, Std={std_t:.2f}, CV={cv_t:.2f}%")

# Определение реки с большей изменчивостью
more_variable = "Emel River" if cv_e > cv_t else "Turgen River"
print(f"\nРезультат: Более значительную межгодовую изменчивость демонстрирует {more_variable}.")

# 3. Визуализация временных рядов
plt.figure(figsize=(12, 6))
plt.plot(df['Year'], df['Emel_River'], label='Emel River', marker='o', color='blue')
plt.plot(df['Year'], df['Turgen_River'], label='Turgen River', marker='s', color='green')
plt.title('Interannual Discharge Variability')
plt.xlabel('Year')
plt.ylabel('Discharge Volume (million m3)')
plt.legend()
plt.grid(True)
plt.savefig("discharge_analysis.png")
plt.show()

# 4. Геопространственная визуализация (Folium)
# Координаты (примерные для демонстрации расположения в регионе Казахстана)
locations = {
    "Emel River": [43.5, 78.5],
    "Turgen River": [43.2, 77.2]
}

# Создание карты
m = folium.Map(location=[43.3, 77.8], zoom_start=7)

for river, coords in locations.items():
    # Добавляем маркер с информацией о CV
    cv_val = cv_e if river == "Emel River" else cv_t
    folium.Marker(
        location=coords,
        popup=f"{river} (CV: {cv_val:.2f}%)",
        tooltip=river,
        icon=folium.Icon(color='blue' if river == "Emel River" else 'green')
    ).add_to(m)

# Сохранение карты строго под именем 202.html
m.save("202.html")
print("\nMap has been saved as 202.html")