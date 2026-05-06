import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Сбор данных о расходе воды на реке Турген за различные годы и месяцы.
data = {
    'year': [2015, 2016, 2017, 2018, 2019],
    'month': [1, 2, 3, 4, 5],
    'water_flow': [100, 120, 150, 180, 200]
}
df = pd.DataFrame(data)

# Анализ данных для выявления закономерностей в изменении расхода воды по сезонам.
import matplotlib.pyplot as plt
plt.plot(df['year'], df['water_flow'])
plt.xlabel('Год')
plt.ylabel('Расход воды')
plt.title('Изменение расхода воды на реке Турген')
plt.show()

# Использование моделирования времени серии (Time Series Modeling) для прогнозирования будущих значений расхода воды.
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(df['water_flow'], order=(1,1,1))
model_fit = model.fit()
forecast_steps = 3
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)
print('Прогнозированные значения расхода воды на следующие', forecast_steps, 'месяцев:')
print(forecast)

# Анализ результатов моделирования для определения признаков паводка.
if forecast[-1] > 250:
    print('Признаки паводка обнаружены!')
else:
    print('Признаков паводка не обнаружено.')

# Визуализация результатов на карте с помощью библиотеки folium.
m = folium.Map(location=[43.0, 78.5], zoom_start=10)
folium.Marker([43.0, 78.5], popup='Река Турген').add_to(m)
folium.Marker([43.1, 78.6], popup='Признаки паводка обнаружены!').add_to(m)
m.save("79.html")