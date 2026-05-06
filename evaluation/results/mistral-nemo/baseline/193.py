import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# 1. Подготовка данных
data = pd.read_csv('токыраун_стоки.csv') # Замените 'токыраун_стоки.csv' на путь к вашему файлу данных
data = data.dropna() # Удаление пропущенных значений
data['date'] = pd.to_datetime(data['date']) # Преобразование столбца даты в формат datetime

# 2. Выбор независимых переменных
X = data[['температура', 'осадки', 'площадь_водосбора']] # Замените на факторы, которые вы хотите использовать
y = data['сток']

# 3. Создание модели регрессии
model = LinearRegression()
model.fit(X, y)

# 4. Прогнозирование потребности в воде
future_data = pd.read_csv('будущие_факторы.csv') # Замените 'будущие_факторы.csv' на путь к вашему файлу будущих факторов
predictions = model.predict(future_data)

# 5. Визуализация результатов
m = folium.Map(location=[43.2, 76.9], zoom_start=8) # Замените координаты и масштаб на те, которые соответствуют бассейну реки Токыраун

for i in range(len(predictions)):
    lat = future_data.iloc[i]['latitude'] # Замените 'latitude' на фактический столбец с широтой
    lon = future_data.iloc[i]['longitude'] # Замените 'longitude' на фактический столбец с долготой
    consumption = predictions[i]
    folium.CircleMarker(location=[lat, lon], radius=consumption/1000, fill=True).add_to(m)

m.save("токыраун_потребность.html")