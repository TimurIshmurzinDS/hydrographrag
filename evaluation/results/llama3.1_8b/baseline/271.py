import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Загрузка данных о течении реки Баянколь и ценах на биткоин
bayankol_data = pd.read_csv('bayankol_data.csv')
bitcoin_data = pd.read_csv('bitcoin_data.csv')

# Объединение данных по ключевому столбцу 'Дата'
combined_data = pd.merge(bayankol_data, bitcoin_data, on='Дата')

# Подготовка и очистка данных
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
combined_data[['Уровень воды', 'Температура воды']] = scaler.fit_transform(combined_data[['Уровень воды', 'Температура воды']])

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(combined_data.drop('Цена биткоина', axis=1), combined_data['Цена биткоина'], test_size=0.2, random_state=42)

# Обучение случайного леса для прогнозирования цен на биткоин
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Предсказание цен на биткоин с помощью обученной модели
y_pred = rf_model.predict(X_test)

# Визуализация результатов на карте с помощью folium
m = Map(location=[50.0, 90.0], zoom_start=4)
for i in range(len(y_pred)):
    marker = Marker(location=[bayankol_data['Широта'].iloc[i], bayankol_data['Долгота'].iloc[i]], popup=str(y_pred[i]))
    m.add_child(marker)

m.save("271.html")