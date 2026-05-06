import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# 1. Подготовка данных
data_lepsy = pd.read_csv('lespy_river_data.csv')
data_dos = pd.read_csv('dos_river_data.csv')

# 2. Преобразование данных
data_lepsy['date'] = pd.to_datetime(data_lepsy['date'])
data_lespy_std = (data_lepsy['water_level'] - data_lepsy['water_level'].mean()) / data_lepsy['water_level'].std()

# 3. Анализ данных и прогнозирование
X_lespy = pd.DataFrame({'year': data_lepsy['date'].dt.year, 'month': data_lepsy['date'].dt.month})
y_lespy = data_lespy_std['water_level']
model = LinearRegression()
model.fit(X_lespy, y_lespy)

# 4. Прогнозирование для реки Dos River
X_dos = pd.DataFrame({'year': [2023], 'month': range(1, 13)})
y_dos_pred = model.predict(X_dos)

# 5. Картографическое представление
m = folium.Map(location=[data_lepsy['latitude'].mean(), data_lespy['longitude'].mean()])

for i in range(len(data_lespy)):
    folium.CircleMarker(
        location=[data_lespy.iloc[i]['latitude'], data_lespy.iloc[i]['longitude']],
        radius=data_lespy.iloc[i]['water_level'],
        color='blue',
        fill=True
    ).add_to(m)

folium.LayerControl().add_to(m)
m.save("128.html")