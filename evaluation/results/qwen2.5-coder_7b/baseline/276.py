import numpy as np
import matplotlib.pyplot as plt
import folium

# Параметры модели
initial_population = 100  # Начальная популяция кроликов
initial_food = 50        # Начальное количество корма
growth_rate = 0.1        # Коэффициент роста
death_rate = 0.02        # Коэффициент смертности
food_effectiveness = 0.05  # Эффективность корма на рождаемость и смертность

# Функция для расчета изменения популяции
def population_change(population, food):
    birth_rate = growth_rate * population * (1 + food_effectiveness * food)
    death_rate = death_rate * population * (1 - food_effectiveness * food)
    return birth_rate - death_rate

# Симуляция моделирования
time_steps = 100
population = np.zeros(time_steps)
food = np.linspace(0, 100, time_steps)

for t in range(1, time_steps):
    population[t] = population[t-1] + population_change(population[t-1], food[t])

# Визуализация результата
plt.figure(figsize=(10, 5))
plt.plot(food, population, label='Популяция кроликов')
plt.xlabel('Количество корма')
plt.ylabel('Популяция кроликов')
plt.title('Модель роста популяции кроликов в зависимости от количества корма')
plt.legend()
plt.show()

# Создание карты с использованием folium
m = folium.Map(location=[50.0, 36.2], zoom_start=10)

for i in range(time_steps):
    folium.Marker([50.0 + np.random.normal(0, 0.1), 36.2 + np.random.normal(0, 0.1)],
                  popup=f'Количество корма: {food[i]}, Популяция кроликов: {population[i]}',
                  icon=folium.Icon(color='green')).add_to(m)

m.save("276.html")