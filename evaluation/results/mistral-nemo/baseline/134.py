import pandas as pd
import numpy as np

# Загрузите данные о стоке рек Bayankol и Kishi Almaty за последние десять лет
bayankol_data = pd.read_csv('bayankol_river_discharge.csv')
kishi_almaty_data = pd.read_csv('kishi_almaty_river_discharge.csv')

# Вычислите среднее значение стока для каждой реки
bayankol_mean = bayankol_data['discharge'].mean()
kishi_almaty_mean = kishi_almaty_data['discharge'].mean()

# Рассчитайте стандартное отклонение стока для каждой реки, чтобы получить волатильность
bayankol_volatility = bayankol_data['discharge'].std()
kishi_almaty_volatility = kishi_almaty_data['discharge'].std()

# Сравните волатильность стока обеих рек и выведите результат
if bayankol_volatility > kishi_almaty_volatility:
    print("Волатильность стока реки Bayankol выше, чем у реки Kishi Almaty.")
elif bayankol_volatility < kishi_almaty_volatility:
    print("Волатильность стока реки Kishi Almaty выше, чем у реки Bayankol.")
else:
    print("Волатильность стока обеих рек одинакова.")

# Визуализация данных на карте (для демонстрации)
import folium

bayankol_map = folium.Map(location=[43.2568, 71.0999], zoom_start=12) # Координаты реки Bayankol
kishi_almaty_map = folium.Map(location=[43.2432, 71.3661], zoom_start=12) # Координаты реки Kishi Almaty

folium.CircleMarker(location=[43.2568, 71.0999], radius=5, color='blue').add_to(bayankol_map)
folium.CircleMarker(location=[43.2432, 71.3661], radius=5, color='red').add_to(kishi_almaty_map)

bayankol_map.save("bayankol.html")
kishi_almaty_map.save("kishi_almaty.html")