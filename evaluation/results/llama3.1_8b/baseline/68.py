import pandas as pd
from folium import Map, Marker

# Загрузим данные о датчиках из базы данных (для примера мы будем использовать DataFrame)
data = {
    'id': [1, 2, 3],
    'location': [(48.6784, 42.2975), (48.6798, 42.2987), (48.6779, 42.2963)],
    'status': ['работает', 'неисправен', 'работает']
}
df = pd.DataFrame(data)

# Создадим функцию для определения неисправных датчиков
def find_broken_sensors(df):
    broken_sensors = df[df['status'] == 'неисправен']
    return broken_sensors

# Определим неисправные датчики
broken_sensors = find_broken_sensors(df)

# Создадим карту с местоположением всех датчиков
m = Map(location=[48.6784, 42.2975], zoom_start=12)
for index, row in df.iterrows():
    Marker(row['location'], popup=f'Датчик {row["id"]}: {row["status"]}').add_to(m)

# Отметим неисправные датчики на карте
for index, row in broken_sensors.iterrows():
    Marker(row['location'], popup=f'Датчик {row["id"]}: неисправен', icon=folium.Icon(color='red')).add_to(m)

# Сохраним карту в файл
m.save("68.html")