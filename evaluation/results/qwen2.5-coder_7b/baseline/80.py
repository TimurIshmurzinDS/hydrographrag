import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных (замените на реальные данные)
data_tokyraun = {
    'date': pd.date_range(start='1/1/2023', periods=100),
    'flow_rate': np.random.normal(loc=50, scale=10, size=100)  # Примерные значения расхода воды
}

data_koktal = {
    'date': pd.date_range(start='1/1/2023', periods=100),
    'water_level': np.random.normal(loc=5, scale=1, size=100)  # Примерные значения уровня воды
}

df_tokyraun = pd.DataFrame(data_tokyraun)
df_koktal = pd.DataFrame(data_koktal)

# Объединение данных по дате
merged_data = pd.merge(df_tokyraun, df_koktal, on='date')

# Корреляция между расходом воды и уровнем воды
correlation = merged_data['flow_rate'].corr(merged_data['water_level'])
print(f"Корреляция: {correlation}")

# Модель линейной регрессии для прогнозирования уровня воды на Koktal River
X = merged_data[['flow_rate']]
y = merged_data['water_level']
model = LinearRegression()
model.fit(X, y)

# Прогнозирование уровня воды на Koktal River
merged_data['predicted_water_level'] = model.predict(X)

# Визуализация результатов на карте
m = folium.Map(location=[50.1234, 8.7654], zoom_start=10)  # Примерные координаты

for index, row in merged_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],  # Замените на реальные координаты
        popup=f"Flow Rate: {row['flow_rate']}, Predicted Water Level: {row['predicted_water_level']}",
        icon=folium.Icon(color='red' if row['predicted_water_level'] > 10 else 'green')
    ).add_to(m)

m.save("80.html")