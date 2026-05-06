import pandas as pd
from folium import Map, Marker, CircleMarker
import numpy as np

# Загрузка исторических данных о уровнях воды на реке Оск
data = {
    'Дата': ['2022-01-01', '2022-02-15', '2022-03-20', '2022-04-25'],
    'Уровень воды (м)': [10, 12, 15, 18]
}
df = pd.DataFrame(data)

# Анализ данных для определения закономерностей и тенденций
mean_water_level = df['Уровень воды (м)'].mean()
print(f'Средний уровень воды: {mean_water_level} м')

# Создание модели прогнозирования текущего уровня воды на основе исторических данных и метеоусловий
def predict_water_level(date, weather_conditions):
    # Простая модель для примера - в реальных приложениях использовать более сложные алгоритмы
    if date.month == 3 and date.day >= 20:
        return mean_water_level + (weather_conditions['rainfall'] * 0.5)
    else:
        return mean_water_level

# Текущая дата и метеоусловия
current_date = pd.to_datetime('2022-04-01')
weather_conditions = {'rainfall': 10}  # Примерные данные о осадках за текущую дату

# Прогнозирование текущего уровня воды на реке Оск
predicted_water_level = predict_water_level(current_date, weather_conditions)
print(f'Прогнозируемый уровень воды: {predicted_water_level} м')

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[current_date.date().timetuple().tm_yday, predicted_water_level], zoom_start=10)
Marker([current_date.date().timetuple().tm_yday, predicted_water_level]).add_to(m)
CircleMarker([current_date.date().timetuple().tm_yday, predicted_water_level], radius=100).add_to(m)

m.save("26.html")