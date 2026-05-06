import pandas as pd
from folium import Map, Marker
import matplotlib.pyplot as plt

# Сбор данных о стоке для Emel River и Turgen River за определенный период времени.
data_emel = {
    'Year': [2010, 2011, 2012, 2013, 2014],
    'Flow': [100, 120, 110, 130, 105]
}
data_turgen = {
    'Year': [2010, 2011, 2012, 2013, 2014],
    'Flow': [90, 115, 125, 100, 120]
}

df_emel = pd.DataFrame(data_emel)
df_turgen = pd.DataFrame(data_turgen)

# Подготовка данных к анализу
print("Данные Emel River:")
print(df_emel)
print("\nДанные Turgen River:")
print(df_turgen)

# Вычисление показателей вариации (который является мерой изменчивости) для каждого года отдельно для каждой реки.
df_emel['Variation'] = df_emel['Flow'].pct_change()
df_turgen['Variation'] = df_turgen['Flow'].pct_change()

print("\nПоказатели вариации Emel River:")
print(df_emel)
print("\nPоказатели вариации Turgen River:")
print(df_turgen)

# Сравнение показателей вариации между Emel River и Turgen River
variation_emel = df_emel['Variation'].mean()
variation_turgen = df_turgen['Variation'].mean()

if variation_emel > variation_turgen:
    print("Emel River демонстрирует более значительную межгодовую изменчивость стока.")
elif variation_turgen > variation_emel:
    print("Turgen River демонстрирует более значительную межгодовую изменчивость стока.")
else:
    print("Обе реки демонстрируют одинаковую межгодовую изменчивость стока.")

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
Marker(location=[50.0, 70.0], popup='Emel River').add_to(m)
Marker(location=[51.0, 71.0], popup='Turgen River').add_to(m)

# Сохранение карты в файл
m.save("202.html")