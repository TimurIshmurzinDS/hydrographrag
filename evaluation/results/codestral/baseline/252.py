python
         import folium
         from web3 import Web3, HTTPProvider
         # Connect to Ethereum node
         w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
         # Define smart contract ABI and address
         abi = [...] # ABI of the deployed smart contract
         contract_address = '0x...' # Address of the deployed smart contract
         # Create contract instance
         contract = w3.eth.contract(address=contract_address, abi=abi)
         # Get river coordinates from smart contract
         river_coords = contract.functions.getRiverCoordinates().call()
         # Create map centered at the first coordinate
         m = folium.Map(location=[river_coords[0][0], river_coords[0][1]], zoom_start=10)
         # Add river coordinates to map as markers
         for coord in river_coords:
             folium.Marker([coord[0], coord[1]]).add_to(m)
         # Save map as HTML file
         m.save("252.html")