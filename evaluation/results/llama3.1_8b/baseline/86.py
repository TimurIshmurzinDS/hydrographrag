import pandas as pd
from folium import Map, Marker, CircleMarker
import matplotlib.pyplot as plt

# Сбор данных о уровнях воды на каждой реке за последние несколько лет.
data = {
    'Река': ['Караой', 'Темирлик', 'Турген'],
    'Данные уровня воды': [
        [10, 15, 20],  # Данные уровня воды для Караойской реки
        [12, 18, 22],  # Данные уровня воды для Темирликовской реки
        [11, 16, 21]   # Данные уровня воды для Тургенской реки
    ]
}

df = pd.DataFrame(data)

# Анализ данных для выявления тенденций и закономерностей в изменении уровней воды.
for river in df['Река'].unique():
    river_data = df[df['Река'] == river]
    plt.plot(river_data['Данные уровня воды'])
    plt.title(f'Уровень воды на реке {river}')
    plt.show()

# Определение критических значений уровня воды, которые могут указывать на опасный рост воды из-за паводка.
critical_levels = {
    'Караой': 18,
    'Темирлик': 20,
    'Турген': 19
}

# Создание модели, которая может прогнозировать уровень воды на каждой реке на основе исторических данных и текущих метеоусловий.
from sklearn.linear_model import LinearRegression

model = LinearRegression()
X = df[['Данные уровня воды']]
y = df['Река']
model.fit(X, y)

# Визуализация результатов на карте с помощью библиотеки Folium.
m = Map(location=[46.0, 68.0], zoom_start=6)
for i, river in enumerate(df['Река']):
    level = df.loc[i, 'Данные уровня воды']
    if level > critical_levels[river]:
        marker = Marker(
            location=[df.loc[i, 'location'].latitude, df.loc[i, 'location'].longitude],
            popup=f'Опасный рост уровня воды на реке {river}',
            icon=CircleMarker(color='red')
        ).add_to(m)
    else:
        marker = Marker(
            location=[df.loc[i, 'location'].latitude, df.loc[i, 'location'].longitude],
            popup=f'Уровень воды на реке {river} безопасен'
        ).add_to(m)

m.save("86.html")