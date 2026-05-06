import pandas as pd
import numpy as np
from folium import Map, CircleMarker

# Генерируем искусственные данные о русле реки Шилик
np.random.seed(0)
data = {
    'x': np.random.uniform(-180, 180, size=100),
    'y': np.random.uniform(-90, 90, size=100),
    'извилистость': np.random.uniform(0.1, 10, size=100)
}
df = pd.DataFrame(data)

# Генерируем случайные числа на основе извилистости русла реки
df['случайное_число'] = df['извилистость'].apply(lambda x: np.random.uniform(0, 1) * x)

# Создаем карту с помощью Folium
m = Map(location=[40.00, 75.00], zoom_start=4)

# Добавляем точки на карте с случайными числами
for index, row in df.iterrows():
    CircleMarker([row['y'], row['x']], radius=5).add_to(m)
    m.circle_marker(row['y'], row['x'], radius=5, popup=f"Случайное число: {row['случайное_число']}").add_to(m)

# Сохраним карту в файл
m.save("254.html")