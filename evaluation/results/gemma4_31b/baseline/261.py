import folium
import numpy as np
import pandas as pd

def solve_pickling_gis_task():
    # 1. Координаты реки Киши Осек (аппроксимация русла для моделирования)
    # В реальности здесь используются Shape-файлы или GeoJSON
    river_coords = [
        [42.150, 71.200], [42.160, 71.220], [42.175, 71.250], 
        [42.190, 71.280], [42.210, 71.310], [42.230, 71.350],
        [42.250, 71.390], [42.270, 71.430]
    ]
    
    # 2. Моделирование минерализации (г/л)
    # Предположим, что соленость растет вниз по течению
    salinity_values = np.linspace(0.5, 12.0, len(river_coords)) 
    
    # Создаем DataFrame для анализа
    df = pd.DataFrame({
        'lat': [c[0] for c in river_coords],
        'lon': [c[1] for c in river_coords],
        'salinity': salinity_values
    })
    
    # 3. Поиск точки с максимальной соленостью
    optimal_point = df.loc[df['salinity'].idxmax()]
    opt_lat, opt_lon = optimal_point['lat'], optimal_point['lon']
    max_sal = optimal_point['salinity']
    
    # 4. "Рецепт" на основе данных
    # Для засолки нужно ~30-50 г соли на литр. 
    # Если в воде 12 г/л, нужно выпарить воду примерно в 3-4 раза.
    evaporation_factor = 40 / max_sal if max_sal > 0 else float('inf')
    
    recipe = (
        f"РЕЦЕПТ: \n"
        f"1. Отправиться в точку с макс. минерализацией: {opt_lat}, {opt_lon}.\n"
        f"2. Зачерпнуть воду (текущая соленость: {max_sal:.2f} г/л).\n"
        f"3. Выпарить воду в котле примерно в {evaporation_factor:.1f} раз, "
        f"чтобы достичь концентрации соли ~40 г/л.\n"
        f"4. Залить полученным рассолом овощи."
    )
    
    print(recipe)
    
    # 5. Визуализация на карте
    m = folium.Map(location=[42.21, 71.31], zoom_start=11)
    
    # Рисуем реку
    folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.8, tooltip="Река Киши Осек").add_to(m)
    
    # Отмечаем все точки замера солености
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color='blue',
            fill=True,
            popup=f"Соленость: {row['salinity']:.2f} г/л"
        ).add_to(m)
        
    # Отмечаем точку забора воды для засолки
    folium.Marker(
        location=[opt_lat, opt_lon],
        popup="ТОЧКА ЗАСОЛКИ (Max Salinity)",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Сохранение карты
    m.save("261.html")
    print("\nКарта сохранена в файл 261.html")

if __name__ == "__main__":
    solve_pickling_gis_task()