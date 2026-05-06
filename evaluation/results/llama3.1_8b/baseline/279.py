import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.regression.linear_model import RegressionResults
from folium import Map, Marker

# Загрузка данных
prices = pd.read_csv('prices.csv')
coordinates = pd.read_csv('coordinates.csv')

# Обработка данных
prices['price'] = prices['price'].astype(float)
coordinates['latitude'] = coordinates['latitude'].astype(float)
coordinates['longitude'] = coordinates['longitude'].astype(float)

# Регрессионный анализ
model = ols(formula='price ~ latitude + longitude', data=prices).fit()

# Оценка модели
print(model.summary())
print('R-squared:', model.rsquared)
print('MSE:', model.mse_resid)

# Визуализация результатов
m = Map(location=[coordinates['latitude'].mean(), coordinates['longitude'].mean()], zoom_start=10)
for i, row in prices.iterrows():
    marker = Marker([row['latitude'], row['longitude']], popup=f'Цена: {row["price"]}')
    m.add_child(marker)
m.save("279.html")