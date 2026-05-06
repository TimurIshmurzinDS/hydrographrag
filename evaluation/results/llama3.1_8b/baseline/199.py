import pandas as pd
from folium import Map, Marker
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Подготовка данных
data = pd.read_csv('historical_data.csv')

# Преобразование данных
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

# Создание модели корреляции
X = data[['осадки', 'сток']]
y = data['динамика_стока']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Визуализация результатов
m = Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
for index, row in data.iterrows():
    marker = Marker(location=[row['latitude'], row['longitude']], popup=f'осадки: {row["осадки"]}, сток: {row["сток"]}')
    m.add_child(marker)

# Визуализация корреляции
correlation_matrix = data.corr()
m = Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
for i in range(correlation_matrix.shape[0]):
    for j in range(i+1, correlation_matrix.shape[1]):
        if abs(correlation_matrix.iloc[i, j]) > 0.5:
            marker = Marker(location=[data['latitude'].mean(), data['longitude'].mean()], popup=f'корреляция между {correlation_matrix.columns[i]} и {correlation_matrix.columns[j]}: {correlation_matrix.iloc[i, j]}')
            m.add_child(marker)

# Сохранение карты
m.save("199.html")