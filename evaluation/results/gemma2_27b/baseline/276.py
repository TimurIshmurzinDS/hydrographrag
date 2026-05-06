import numpy as np
import matplotlib.pyplot as plt
import folium

# Параметры модели
initial_population = 100
birth_rate = 0.2  # Скорость размножения (в зависимости от количества корма)
death_rate = 0.05 # Скорость смерти
carrying_capacity = 500 # Максимальная популяция

# Функция роста популяции
def population_growth(population, food):
    return population * (1 + birth_rate * min(food / population, 1)) - death_rate * population

# Моделирование роста популяции
time_steps = 50
population = [initial_population]
food = np.arange(carrying_capacity)

for t in range(time_steps):
    population.append(population[-1] + population_growth(population[-1], food[t]))

# Визуализация результатов
m = folium.Map(location=[40, 30], zoom_start=5)
folium.CircleMarker(location=[40, 30], radius=population[-1]/10, color='green').add_to(m)
m.save("276.html")

# График роста популяции
plt.plot(range(time_steps+1), population)
plt.xlabel('Время')
plt.ylabel('Популяция')
plt.title('Рост популяции кроликов')
plt.show()