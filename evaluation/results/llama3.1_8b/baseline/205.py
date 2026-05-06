import pandas as pd
from scipy.stats import pearsonr
import folium

# Сбор и подготовка данных
data = {
    'Дата': ['2020-01-01', '2020-02-01', '2020-03-01'],
    'Срок снеготаяния': [15, 20, 25],
    'Расход воды': [100, 120, 150]
}
df = pd.DataFrame(data)

# Анализ корреляции
corr_coef, _ = pearsonr(df['Срок снеготаяния'], df['Расход воды'])
print(f'Коэффициент корреляции Пирсона: {corr_coef}')

# Моделирование влияния изменений в сроках снеготаяния
def model_influence(snow_melt_dates, water_flow):
    # Простое линейное моделирование (на самом деле это простой пример)
    return 2 * snow_melt_dates + water_flow

# Визуализация результатов
m = folium.Map(location=[55.0, 60.0], zoom_start=10)

for i in range(len(df)):
    folium.Circle(
        location=[df['Дата'].iloc[i].split('-')[1] + '.' + df['Дата'].iloc[i].split('-')[2],
                  float(df['Срок снеготаяния'].iloc[i])],
        radius=df['Расход воды'].iloc[i] * 10,
        color='blue'
    ).add_to(m)

folium.Marker(
    location=[55.0, 60.0],
    popup='Модельное влияние изменений в сроках снеготаяния на динамику стока',
    icon=folium.Icon(color='red')
).add_to(m)

# Моделирование влияния изменений в сроках снеготаяния
for i in range(len(df)):
    folium.Marker(
        location=[df['Дата'].iloc[i].split('-')[1] + '.' + df['Дата'].iloc[i].split('-')[2],
                  float(model_influence(df['Срок снеготаяния'].iloc[i], df['Расход воды'].iloc[i]))],
        popup=f'Модельное влияние на дату {df["Дата"].iloc[i]}',
        icon=folium.Icon(color='green')
    ).add_to(m)

m.save("205.html")