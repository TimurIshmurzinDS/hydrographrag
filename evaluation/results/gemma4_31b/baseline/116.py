import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

def analyze_water_stability(river_name, data):
    """
    Анализирует стабильность уровня воды на основе коэффициента вариации.
    """
    mean_val = np.mean(data)
    std_val = np.std(data)
    cv = (std_val / mean_val) * 100
    
    if cv < 15:
        status = "Стабильный (Высокая пригодность)"
        color = "green"
    elif 15 <= cv < 30:
        status = "Умеренно стабильный (Требуется ирригация)"
        color = "orange"
    else:
        status = "Нестабильный (Высокий риск)"
        color = "red"
        
    return {
        "river": river_name,
        "mean": round(mean_val, 2),
        "cv": round(cv, 2),
        "status": status,
        "color": color
    }

# 1. Симуляция данных об уровне воды (в метрах) за 12 месяцев
# Tekeli: более стабильная река
# Lepsy: более подвержена сезонным колебаниям
np.random.seed(42)
data_tekeli = np.random.normal(loc=2.5, scale=0.3, size=12) 
data_lepsy = np.random.normal(loc=3.0, scale=1.1, size=12)

rivers_data = {
    "Tekeli River": {
        "coords": [43.51, 80.52], 
        "levels": data_tekeli
    },
    "Lepsy River": {
        "coords": [43.85, 81.20], 
        "levels": data_lepsy
    }
}

# 2. Проведение анализа
results = []
for name, info in rivers_data.items():
    res = analyze_water_stability(name, info["levels"])
    res["coords"] = info["coords"]
    results.append(res)

# 3. Визуализация на карте
# Центрируем карту в регионе рек (Казахстан, область Жетысу)
m = folium.Map(location=[43.68, 80.86], zoom_start=8, tiles="OpenStreetMap")

for res in results:
    popup_text = (
        f"<b>Река:</b> {res['river']}<br>"
        f"<b>Средний уровень:</b> {res['mean']} м<br>"
        f"<b>Коэф. вариации (CV):</b> {res['cv']}%<br>"
        f"<b>Вердикт:</b> {res['status']}"
    )
    
    folium.CircleMarker(
        location=res["coords"],
        radius=10,
        popup=popup_text,
        color=res["color"],
        fill=True,
        fill_color=res["color"],
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("116.html")

print("Анализ завершен. Результаты сохранены в файл 116.html")
for r in results:
    print(f"Река {r['river']}: CV={r['cv']}%, Статус={r['status']}")