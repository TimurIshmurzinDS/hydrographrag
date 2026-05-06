import hashlib
import time
import random
import folium
from datetime import datetime

# ==========================================
# 1. Блокчейн архитектура
# ==========================================

class Block:
    def __init__(self, index, timestamp, sensor_id, runoff_value, coords, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.runoff_value = runoff_value
        self.coords = coords
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Создание SHA-256 хеша блока"""
        block_string = f"{self.index}{self.timestamp}{self.sensor_id}{self.runoff_value}{self.coords}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Создание первого блока в сети"""
        return Block(0, time.time(), "GENESIS", 0, (0, 0), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, sensor_id, runoff_value, coords):
        """Добавление нового замера стока в блокчейн"""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            sensor_id=sensor_id,
            runoff_value=runoff_value,
            coords=coords,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Проверка целостности данных"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# ==========================================
# 2. Геоданные и симуляция (Река Осек)
# ==========================================

# Примерные координаты точек вдоль реки Осек (симуляция)
# В реальности здесь используются реальные координаты ГИС-слоя
osek_river_sensors = [
    {"id": "S1", "coords": [56.123, 38.456]},
    {"id": "S2", "coords": [56.145, 38.480]},
    {"id": "S3", "coords": [56.160, 38.510]},
    {"id": "S4", "coords": [56.185, 38.540]},
    {"id": "S5", "coords": [56.210, 38.570]},
]

# Инициализация блокчейна
river_blockchain = Blockchain()

# Симуляция сбора данных о стоке (м3/с)
for sensor in osek_river_sensors:
    runoff_val = round(random.uniform(1.5, 12.0), 2)
    river_blockchain.add_block(sensor["id"], runoff_val, sensor["coords"])

# Проверка валидности
validity = river_blockchain.is_chain_valid()
print(f"Blockchain Integrity Verified: {validity}")

# ==========================================
# 3. Визуализация на карте
# ==========================================

# Создаем карту, центрированную на среднем значении координат
m = folium.Map(location=[56.16, 38.51], zoom_start=11, tiles='OpenStreetMap')

# Добавляем точки из блокчейна на карту
for block in river_blockchain.chain[1:]:  # Пропускаем генезис-блок
    # Определяем цвет в зависимости от величины стока
    color = 'green' if block.runoff_value < 5 else 'orange' if block.runoff_value < 8 else 'red'
    
    folium.CircleMarker(
        location=block.coords,
        radius=8,
        popup=f"Sensor: {block.sensor_id}<br>Runoff: {block.runoff_value} m3/s<br>Hash: {block.hash[:10]}...",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Добавляем линию, имитирующую русло реки
river_coords = [s["coords"] for s in osek_river_sensors]
folium.PolyLine(river_coords, color="blue", weight=3, opacity=0.7, tooltip="River Osek").add_to(m)

# Сохранение карты
m.save("238.html")
print("Map has been saved as 238.html")