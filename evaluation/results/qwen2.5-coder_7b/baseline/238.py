import folium
from pyblockchain2 import Blockchain, Block

# Пример данных о стоке реки Осек (время, объем воды)
data = [
    {"timestamp": "2023-10-01 08:00", "volume": 500},
    {"timestamp": "2023-10-01 09:00", "volume": 550},
    {"timestamp": "2023-10-01 10:00", "volume": 600},
    # Добавьте больше данных по мере необходимости
]

# Создание блокчейна
blockchain = Blockchain()

# Функция для создания блока из данных
def create_block(data):
    block = Block(index=len(blockchain.chain), timestamp=data["timestamp"], data=data)
    return block

# Добавление блоков в блокчейн
for entry in data:
    block = create_block(entry)
    blockchain.add_block(block)

# Визуализация данных на карте
m = folium.Map(location=[50.45, 30.52], zoom_start=13)  # Координаты примера (Киев)

for entry in data:
    timestamp = entry["timestamp"]
    volume = entry["volume"]
    folium.Marker(
        location=[50.45, 30.52],  # Здесь можно использовать реальные координаты для каждой точки
        popup=f"Timestamp: {timestamp}<br>Volume: {volume} m³",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты как HTML файл
m.save("238.html")