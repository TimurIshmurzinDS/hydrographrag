import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import folium

# 1. Подготовка данных
data_shilik = pd.read_csv('shilik_river_discharge.csv', index_col='date', parse_dates=True)
data_shyzhyn = pd.read_csv('shyzhyn_river_discharge.csv', index_col='date', parse_dates=True)

# 2. Анализ данных
def analyze_seasonality(data):
    data['month'] = data.index.month
    seasonal_mean = data.groupby('month').mean()
    return seasonal_mean

seasonal_shilik = analyze_seasonality(data_shilik)
seasonal_shyzhyn = analyze_seasonality(data_shyzhyn)

# 3. Моделирование
def build_arima_model(data, p, d, q):
    model = ARIMA(data, order=(p,d,q))
    model_fit = model.fit(disp=0)
    return model_fit

model_shilik = build_arima_model(data_shilik['discharge'], 5, 1, 0)
model_shyzhyn = build_arima_model(data_shyzhyn['discharge'], 5, 1, 0)

# 4. Прогнозирование
def predict_seasonal_discharge(model, periods):
    predictions = model.predict(start=len(model), end=len(model)+periods-1)
    return predictions

predictions_shilik = predict_seasonal_discharge(model_shilik, 12)
predictions_shyzhyn = predict_seasonal_discharge(model_shyzhyn, 12)

# 5. Визуализация
m = folium.Map(location=[43.2, 76.9], zoom_start=8) # примерные координаты для карты

folium.Marker([data_shilik.index[0].latitude, data_shilik.index[0].longitude],
              popup='Shilik River\nSeasonal Discharge:\n{}'.format(seasonal_shilik['discharge'].mean())).add_to(m)

folium.Marker([data_shyzhyn.index[0].latitude, data_shyzhyn.index[0].longitude],
              popup='Shyzhyn River\nSeasonal Discharge:\n{}'.format(seasonal_shyzhyn['discharge'].mean())).add_to(m)

m.save("157.html")