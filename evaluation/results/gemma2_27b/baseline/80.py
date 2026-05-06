import pandas as pd
import folium

# Загрузка данных о расходе воды
tokyraun_data = pd.read_csv("tokyraun_river_flow.csv")
koktal_data = pd.read_csv("koktal_river_flow.csv")

# Преобразование данных в единые единицы измерения (если необходимо)

# Определение порога опасного уровня расхода воды

# Расчет показателей риска затопления

# Создание карты с folium
m = folium.Map(location=[tokyraun_data["latitude"].mean(), tokyraun_data["longitude"].mean()], zoom_start=10)

# Добавление данных о расходе воды на карту

# Сохранение карты
m.save("80.html")