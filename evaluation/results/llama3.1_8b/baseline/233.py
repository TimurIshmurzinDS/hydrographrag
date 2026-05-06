import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from folium import Map, Marker
import numpy as np

# Сбор данных о паводке реки Кумбель (предположим, что данные хранятся в файле 'kumbel_data.csv')
data = pd.read_csv('kumbel_data.csv')

# Анализ данных для определения закономерностей и тенденций
print(data.describe())

# Разделение данных на обучающую и проверочную выборки
X = data[['date', 'water_level']]
y = data['pavodok']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели для предсказания уровня воды в реке
model = LinearRegression()
model.fit(X_train, y_train)

# Генерация NFT на основе модели
np.random.seed(42)
nft_data = np.random.rand(100, 2)  # генерируем случайные данные для NFT

# Создание карты с маркерами для каждого NFT
m = Map(location=[55.7558, 37.6173], zoom_start=10)
for i in range(nft_data.shape[0]):
    marker = Marker([nft_data[i, 0], nft_data[i, 1]], popup=f'NFT {i+1}')
    m.add_child(marker)

# Сохранение карты в файл
m.save("233.html")