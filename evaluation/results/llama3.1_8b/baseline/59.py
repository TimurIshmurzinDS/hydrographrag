import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA
from folium import Map, Marker

# Загрузка данных о реке Шилик и климатических условиях
data_shilik = pd.read_csv('shilik_data.csv')
data_climate = pd.read_csv('climate_data.csv')

# Преобразование геометрии реки в проекцию UTM
from pyproj import Transformer
transformer = Transformer.from_crs(4326, 32640)
geometry_shilik = data_shilik['geometry'].apply(transformer.transform)

# Объединение данных о наблюдениях и метеорологических условиях
data_combined = pd.merge(data_shilik, data_climate, on='date')

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data_combined.drop('water_flow', axis=1), data_combined['water_flow'], test_size=0.2, random_state=42)

# Создание модели ARIMA для прогнозирования расхода воды
model_arima = ARIMA(y_train, order=(5,1,0))
model_arima_fit = model_arima.fit()

# Создание регрессионной модели для учитывания влияния климатических факторов
model_rf = RandomForestRegressor(n_estimators=100)
model_rf.fit(X_train, y_train)

# Предсказание расхода воды на следующее десятилетие
forecast = model_arima_fit.forecast(steps=10*12)[0]

# Создание карты с прогнозами расхода воды
m = Map(location=[data_shilik['geometry'].centroid.y.mean(), data_shilik['geometry'].centroid.x.mean()], zoom_start=8)
for i in range(10):
    marker = Marker([data_shilik['geometry'].centroid.y.mean(), data_shilik['geometry'].centroid.x.mean()], popup=f'Прогноз расхода воды на {i+1} год: {forecast[i]}')
    m.add_child(marker)

# Сохранение карты
m.save('59.html')