import hashlib
import time
from geopy.geocoders import Nominatim
import folium

# Step 1: Collect data about the flow of Osek River
def collect_data():
    # Assume we have a function that fetches data from a sensor or a database
    data = fetch_sensor_data()
    return data

# Step 2: Prepare data for blockchain
def prepare_data(data):
    # Normalize and aggregate data as needed
    prepared_data = normalize_and_aggregate(data)
    return prepared_data

# Step 3: Create blocks
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

# Step 4: Add metadata to blocks
def add_metadata(block):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode("Osek River")
    block['location'] = (location.latitude, location.longitude)
    block['timestamp'] = time.time()
    return block

# Step 5: Create blockchain network
def create_network():
    # Assume we have a list of participants in the network
    participants = ['participant1', 'participant2', ...]
    return participants

# Step 6: Visualize data on map using folium
def visualize_data(data):
    m = folium.Map(location=[50.45, 30.52], zoom_start=8) # Starting location and zoom level for Osek River area
    for item in data:
        lat, lon = item['location']
        folium.Marker([lat, lon]).add_to(m)
    m.save("238.html")

# Main function to run the blockchain creation process
def main():
    data = collect_data()
    prepared_data = prepare_data(data)

    # Initialize the blockchain with the genesis block
    blockchain = [Block(0, "0", time.time(), prepared_data[0], calculate_hash(0, "0", time.time(), prepared_data[0]))]

    for i in range(1, len(prepared_data)):
        new_block = Block(i, blockchain[-1].hash, time.time(), prepared_data[i], calculate_hash(i, blockchain[-1].hash, time.time(), prepared_data[i]))
        blockchain.append(new_block)

    # Add metadata to blocks
    for block in blockchain:
        add_metadata(block)

    # Create blockchain network
    participants = create_network()

    # Visualize data on map using folium
    visualize_data(prepared_data)

if __name__ == "__main__":
    main()