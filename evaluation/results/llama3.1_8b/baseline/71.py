import pandas as pd
from folium import Map, Marker

# Загрузим данные о сенсорах (предположим, они хранятся в файле sensors.csv)
sensors_data = pd.read_csv('sensors.csv')

# Фильтруем данные по реке Byzhy River
byzhy_sensors = sensors_data[sensors_data['river'] == 'Byzhy']

# Проверяем, все ли сенсоры находятся в активном режиме
active_sensors = byzhy_sensors[byzhy_sensors['status'] == 'активен']

# Если есть сенсоры, которые не работают, выведем информацию об них
inactive_sensors = byzhy_sensors[byzhy_sensors['status'] != 'активен']
if not inactive_sensors.empty:
    print("Следующие сенсоры не работают:")
    print(inactive_sensors)

# Создадим карту с маркерами для активных сенсоров
m = Map(location=[55.76, 37.62], zoom_start=10)
for index, row in active_sensors.iterrows():
    Marker([row['latitude'], row['longitude']], popup=row['id']).add_to(m)

# Сохраним карту в файл
m.save("71.html")