import pandas as pd
from folium import Map, FeatureGroup, GeoJson

# Загрузка данных о реках
data_byzhy = pd.read_csv("data_byzhy.csv")
data_tekeli = pd.read_csv("data_tekeli.csv")

# Вычисление средних значений индикаторов
avg_byzhy = data_byzhy.mean()
avg_tekeli = data_tekeli.mean()

# Сравнение средних значений с помощью t-теста (пример)
from scipy import stats
t_stat, p_value = stats.ttest_ind(data_byzhy["BOD"], data_tekeli["BOD"])

print("T-statistic:", t_stat)
print("P-value:", p_value)

# Создание карты с folium
m = Map(location=[43, 78], zoom_start=6)

# Добавление данных о реках на карту (пример)
feature_group_byzhy = FeatureGroup(name="Byzhy River")
geojson_byzhy = GeoJson(data_byzhy["geometry"], name="Byzhzy River")
feature_group_byzhy.add_child(geojson_byzhy)

feature_group_tekeli = FeatureGroup(name="Tekeli River")
geojson_tekeli = GeoJson(data_tekeli["geometry"], name="Tekeli River")
feature_group_tekeli.add_child(geojson_tekeli)

m.add_child(feature_group_byzhy)
m.add_child(feature_group_tekeli)

# Сохранение карты
m.save("119.html")