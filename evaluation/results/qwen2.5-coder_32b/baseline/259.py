import folium
from branca.element import Template, MacroElement

# Шаг 1: Сбор данных о реке Баскан
# Для примера используем координаты приближенно расположенного места реки Баскан в Казахстане.
baskan_coords = [45.032869, 70.155376]

# Шаг 2: Анализ водных ресурсов
# Предположим, что у нас есть данные о среднем объеме воды в реке Баскан (в кубических метрах в секунду).
average_water_flow = 10.0  # Примерное значение

# Шаг 3: Моделирование потребностей корабля
# Предположим, что космический корабль требует для охлаждения двигателей 5 кубических метров воды в минуту.
required_water_flow = 5.0 * 60  # Переводим в секунды

# Шаг 4: Сравнение ресурсов и потребностей
if average_water_flow >= required_water_flow:
    result_text = "Река Баскан может обеспечить достаточное количество воды для охлаждения двигателей космического корабля."
else:
    result_text = "Река Баскан не может обеспечить достаточное количество воды для охлаждения двигателей космического корабля."

# Шаг 5: Визуализация результатов
m = folium.Map(location=baskan_coords, zoom_start=12)

# Добавляем маркер реки Баскан
folium.Marker(
    location=baskan_coords,
    popup=f"Река Баскан\n{result_text}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Добавление информации о результатах на карту
template = """
{% macro html(this, kwargs) %}
<div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 300px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;
     ">
     <div style="padding: 10px">
         {{this._parent.result_text}}
     </div>
</div>
{% endmacro %}
"""

macro = MacroElement()
macro._template = Template(template)
macro.result_text = result_text
m.get_root().add_child(macro)

# Сохранение карты в файл
m.save("259.html")