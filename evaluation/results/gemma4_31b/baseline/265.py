import folium

def generate_emel_joke_map():
    # Координаты района реки Эмел (приблизительные)
    emel_coords = [43.5000, 78.5000]
    
    # Создание карты
    m = folium.Map(location=emel_coords, zoom_start=9, tiles='OpenStreetMap')
    
    # 1. Создаем "Зону экологического оптимизма" (красный круг)
    folium.Circle(
        location=emel_coords,
        radius=20000, # 20 км
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.3,
        popup='Зона ускоренного развития иммунитета рыб'
    ).add_to(m)
    
    # 2. Маркер с анекдотом (Эпицентр)
    joke_text = (
        "<b>Экологическая катастрофа на Эмеле</b><br><br>"
        "Приходит инспектор на берег реки Эмел, видит — рыба плавает брюхом вверх. "
        "Спрашивает местного: 'Что здесь произошло? Это же катастрофа!'<br>"
        "Местный отвечает: 'Какая катастрофа? Мы просто решили провести "
        "эксперимент по ускоренному развитию иммунитета у карпов!'"
    )
    
    folium.Marker(
        location=emel_coords,
        popup=folium.Popup(joke_text, max_width=300),
        tooltip="Нажми, чтобы узнать правду",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # 3. Маркер "Офис контроля" (в стороне от событий)
    office_coords = [43.6000, 78.7000]
    folium.Marker(
        location=office_coords,
        popup="Офис экологического контроля (здесь все в порядке)",
        tooltip="Бюрократический центр",
        icon=folium.Icon(color='blue', icon='institution')
    ).add_to(m)
    
    # Сохранение карты
    m.save("265.html")
    print("Modeling complete. The map with the joke has been saved as 265.html")

if __name__ == "__main__":
    generate_emel_joke_map()