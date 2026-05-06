import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'Year': [1850, 1860, 1870, 1880, 1890, 1900, 2000, 2010, 2020],
    'Country': ['USA', 'Russia', 'Canada', 'Australia', 'South Africa', 'China', 'India', 'Brazil', 'Mexico'],
    'Gold_Mined': [5.6, 7.8, 9.1, 10.3, 12.4, 15.6, 18.9, 21.1, 23.4]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Разделение данных на два периода
df_19th_century = df[df['Year'] < 1900]
df_20th_century = df[df['Year'] >= 1900]

# Функция для создания тепловых карт
def create_heatmap(df, title):
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Создание списка точек с координатами и значениями добычи золота
    heat_data = [[row['Country'], row['Gold_Mined']] for index, row in df.iterrows()]
    
    # Добавление тепловых данных на карту
    HeatMap(heat_data).add_to(m)
    
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.LayerControl().add_to(m)
    
    m.save(f"{title}.html")
    return m

# Создание тепловых карт для XIX и XX веков
m_19th_century = create_heatmap(df_19th_century, "274_19th_Century_Gold_Mining")
m_20th_century = create_heatmap(df_20th_century, "274_20th_Century_Gold_Mining")

# Вывод карт
print("Тепловая карта XIX века сохранена как 274_19th_Century_Gold_Mining.html")
print("Тепловая карта XX века сохранена как 274_20th_Century_Gold_Mining.html")