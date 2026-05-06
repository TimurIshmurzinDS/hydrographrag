import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

def generate_mars_climate_data(n_points=500):
    """
    Симуляция данных по Марсу: координаты, высота, индекс гидратации минералов.
    """
    np.random.seed(42)
    
    # Генерируем случайные координаты (в пределах Марса)
    lat = np.random.uniform(-89, 89, n_points)
    lon = np.random.uniform(-180, 180, n_points)
    
    # Высота (симуляция: более низкие значения в бассейнах, высокие на полюсах/горах)
    # Добавим зависимость: в экваториальных низинах больше шансов найти воду
    elevation = np.random.normal(0, 2000, n_points) 
    
    # Индекс гидратации (0.0 - сухо, 1.0 - высокая влажность в прошлом)
    # Логика: чем ниже высота и ближе к экватору, тем выше вероятность гидратации
    hydration_index = np.exp(-elevation / 3000) * (1 - np.abs(lat)/90)
    hydration_index = np.clip(hydration_index + np.random.normal(0, 0.1, n_points), 0, 1)
    
    # Расчет индекса климатического сдвига (Climate Shift Index)
    # CSI = (Прошлое состояние - Современное состояние)
    # Современное состояние Марса почти везде 0 по влажности.
    csi = hydration_index * 100 
    
    return pd.DataFrame({
        'lat': lat,
        'lon': lon,
        'elevation': elevation,
        'hydration': hydration_index,
        'csi': csi
    })

def main():
    # 1. Генерация данных
    df = generate_mars_climate_data(1000)
    
    # 2. Создание карты
    # Примечание: folium использует проекцию Земли (EPSG:4326). 
    # Для визуализации Марса мы проецируем его координаты на плоскость Земли.
    m = folium.Map(location=[0, 0], zoom_start=2, tiles='CartoDB dark_matter')
    
    # 3. Добавление тепловой карты (HeatMap)
    # Тепловая карта показывает зоны, где климатические изменения были наиболее выражены (была вода)
    heat_data = [[row['lat'], row['lon'], row['csi']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=20, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)
    
    # 4. Добавление отдельных маркеров для "Критически важных точек" (высокий CSI)
    critical_points = df[df['csi'] > 70].sample(20) # Выбираем 20 самых значимых точек
    
    for _, row in critical_points.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color='yellow',
            fill=True,
            fill_color='yellow',
            popup=f"CSI: {row['csi']:.2f} | Elev: {row['elevation']:.0f}m"
        ).add_to(m)
    
    # Добавление легенды через HTML
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Марс: Климатический анализ</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий сдвиг (Вода)<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Низкий сдвиг (Сухо)<br>
     <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Точки интереса
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Сохранение результата
    m.save("284.html")
    print("Analysis complete. Map saved as 284.html")

if __name__ == "__main__":
    main()