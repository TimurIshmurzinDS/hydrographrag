python
         import geopandas as gpd
         import hashlib
         import time
         import folium
         from folium.plugins import MarkerCluster

         # Load data
         river_data = gpd.read_file('river_osek_data.shp')

         class Block:
             def __init__(self, index, timestamp, data, previous_hash):
                 self.index = index
                 self.timestamp = timestamp
                 self.data = data
                 self.previous_hash = previous_hash
                 self.hash = self.hash_block()

             def hash_block(self):
                 sha = hashlib.sha256()
                 sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
                 return sha.hexdigest()

         class Blockchain:
             def __init__(self):
                 self.chain = [self.create_genesis_block()]

             def create_genesis_block(self):
                 return Block(0, time.time(), "Genesis Block", "0")

             def add_block(self, data):
                 previous_block = self.chain[-1]
                 new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
                 self.chain.append(new_block)

         # Add river data to blockchain
         blockchain = Blockchain()
         for index, row in river_data.iterrows():
             blockchain.add_block(row.to_json())

         # Visualize data on map
         m = folium.Map(location=[river_data['geometry'].y.mean(), river_data['geometry'].x.mean()], zoom_start=10)
         marker_cluster = MarkerCluster().add_to(m)
         for index, row in river_data.iterrows():
             folium.Marker([row['geometry'].y, row['geometry'].x]).add_to(marker_cluster)
         m.save("238.html")