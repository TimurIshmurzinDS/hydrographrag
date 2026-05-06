import pandas as pd
import folium

# Загрузить данные о расходе воды для рек Tekes и Bayankol за последние 5 лет
tekes_data = pd.read_csv('tekes_river.csv')
bayankol_data = pd.read_csv('bayankol_river.csv')

# Вычислить среднее значение расхода воды для каждой реки за последние 5 лет
 tekes_avg = tekes_data['flow'].mean()
bayankol_avg = bayankol_data['flow'].mean()

# Найти максимальное значение расхода воды для каждой реки в этом же периоде
tekes_max = tekes_data['flow'].max()
bayankol_max = bayankol_data['flow'].max()

# Определить, какая река показала наибольшее увеличение расхода воды
if (tekes_max - tekes_avg) > (bayankol_max - bayankol_avg):
    print("Tekes River showed the greatest increase in water flow.")
else:
    print("Bayankol River showed the greatest increase in water flow.")

# Создать карту местоположений рек Tekes и Bayankol
m = folium.Map(location=[43.2, 76.9], zoom_start=5)

# Добавить метку для реки Tekes с относительным значением расхода воды
folium.Marker([tekes_data['latitude'].mean(), tekes_data['longitude'].mean()],
              popup=f"Tekes River\nAverage flow: {tekes_avg:.2f}\nMax flow: {tekes_max:.2f}").add_to(m)

# Добавить метку для реки Bayankol с относительным значением расхода воды
folium.Marker([bayankol_data['latitude'].mean(), bayankol_data['longitude'].mean()],
              popup=f"Bayankol River\nAverage flow: {bayankol_avg:.2f}\nMax flow: {bayankol_max:.2f}").add_to(m)

# Сохранить карту как HTML-файл
m.save("125.html")