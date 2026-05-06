import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from folium import Map, Marker

# Загрузка данных о уровне воды в реке Баянколь
data = pd.read_csv('bayankol_water_level.csv')

# Предобработка данных: удаление пропусков и нормализация значений
data.dropna(inplace=True)
data['water_level'] = (data['water_level'] - data['water_level'].min()) / (data['water_level'].max() - data['water_level'].min())

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание линейной регрессии для прогнозирования будущих колебаний уровня воды
model = LinearRegression()
model.fit(train_data[['time']], train_data['water_level'])

# Прогнозирование будущих колебаний уровня воды
future_water_levels = model.predict([[data['time'].max() + 1], [data['time'].max() + 2]])

# Создание алгоритма майнинга, который будет использовать прогнозы для оптимизации процесса поиска блоков в блокчейне криптовалюты
def mining_algorithm(future_water_levels):
    # Используем прогнозы для определения оптимального времени для поиска блоков
    optimal_time = future_water_levels.argmax()
    
    # Создаем алгоритм майнинга, который будет использовать этот прогноз для оптимизации процесса поиска блоков
    def mining_optimization(data):
        if data['time'] == optimal_time:
            return True  # Время для поиска блоков найдено!
        else:
            return False
    
    return mining_optimization

# Создание карты с прогнозами будущих колебаний уровня воды
m = Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
for i in range(len(future_water_levels)):
    Marker([data['latitude'].iloc[-1], data['longitude'].iloc[-1]], popup=f'Прогноз на {i+1} день: {future_water_levels[i]}').add_to(m)

# Сохранение карты в файл
m.save("215.html")