import folium
import pandas as pd

def solve_hydrological_task():
    # 1. Имитация данных гидрологического мониторинга
    # В реальном сценарии здесь был бы запрос к API гидромета или чтение из БД (PostGIS/NetCDF)
    data = {
        'river': ['Baskan River', 'Prokhodnaya River'],
        'lat': [45.35, 45.20], # Примерные координаты
        'lon': [34.10, 34.30], # Примерные координаты
        'current_discharge': [12.5, None], # Расход для Баскана (м3/с)
        'peak_level': [None, 4.2],         # Уровень для Проходной (м) в пик половодья
    }
    
    df = pd.DataFrame(data)
    
    # Извлекаем конкретные значения для расчета
    baskan_val = df.loc[df['river'] == 'Baskan River', 'current_discharge'].values[0]
    prokhodnaya_val = df.loc[df['river'] == 'Prokhodnaya River', 'peak_level'].values[0]
    
    # 2. Расчет разницы
    # Примечание: Сравниваем числовые значения показателей
    diff = abs(baskan_val - prokhodnaya_val)
    
    print(f"Текущий расход р. Баскан: {baskan_val} м3/с")
    print(f"Пиковый уровень р. Проходная: {prokhodnaya_val} м")
    print(f"Разница между показателями: {diff:.2f}")

    # 3. Визуализация на карте
    # Центрируем карту между двумя точками
    m = folium.Map(location=[45.27, 34.20], zoom_start=10, tiles='OpenStreetMap')
    
    # Добавляем маркер для реки Баскан
    folium.Marker(
        location=[df.loc[0, 'lat'], df.loc[0, 'lon']],
        popup=f"<b>Baskan River</b><br>Текущий расход: {baskan_val} м3/с",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Добавляем маркер для реки Проходная
    folium.Marker(
        location=[df.loc[1, 'lat'], df.loc[1, 'lon']],
        popup=f"<b>Prokhodnaya River</b><br>Пиковый уровень: {prokhodnaya_val} м",
        icon=folium.Icon(color='red', icon='warning-sign')
    ).add_to(m)
    
    # Добавляем текстовое примечание о разнице в центре карты
    info_text = f"Анализ: Разница между расходом Баскана и уровнем Проходной составляет {diff:.2f} ед."
    folium.Popup(info_text).add_to(m) # Это технически создаст popup, но мы выведем его в консоль и в маркеры
    
    # Добавим общую информацию в отдельный маркер или просто сохраним карту
    # Для наглядности добавим финальный результат в popup первого маркера
    m.add_child(folium.Marker(
        location=[45.27, 34.20],
        popup=f"<b>Результат анализа:</b><br>Разница: {diff:.2f}",
        icon=folium.Icon(color='green', icon='leaf')
    ))

    # Сохранение карты строго по условию
    m.save("89.html")
    print("Карта успешно сохранена в файл 89.html")

if __name__ == "__main__":
    solve_hydrological_task()