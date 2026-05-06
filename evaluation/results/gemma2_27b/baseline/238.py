import datetime
import hashlib
import json
import folium

class Block:
    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = None
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(json.dumps(self.__dict__, sort_keys=True).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(datetime.datetime.now(), "Genesis block")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(datetime.datetime.now(), data)
        new_block.previous_hash = previous_block.hash
        self.chain.append(new_block)

# Load river Osek data (replace with actual file loading logic)
data = [{"timestamp": datetime.datetime(2023, 1, 1), "value": 10},
        {"timestamp": datetime.datetime(2023, 1, 2), "value": 15}]

# Create blockchain and add data
blockchain = Blockchain()
for item in data:
    blockchain.add_block(item)

# Visualize on map (replace with actual coordinates of river Osek)
m = folium.Map(location=[48.7, 20.5], zoom_start=12)
for item in blockchain.chain:
    folium.Marker(location=[48.7, 20.5], popup=f"Timestamp: {item.timestamp}, Value: {item.data['value']}").add_to(m)

m.save("238.html")