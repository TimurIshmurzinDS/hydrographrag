# Установка необходимых библиотек
!pip install web3 folium pandas

import pandas as pd
from web3 import Web3, HTTPProvider
from solcx import compile_source
import folium

### Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о стоке реки Осек
data = pd.read_csv('oska_river_data.csv')  # Пример файла с данными

### Шаг 2: Обработка данных
# Предварительная обработка данных (например, удаление пропущенных значений)
data.dropna(inplace=True)

### Шаг 3: Выбор технологии блокчейна и разработка смарт-контракта
# Пример простого смарт-контракта на Solidity для хранения данных о стоке реки

contract_source_code = '''
pragma solidity ^0.8.0;

contract OskaRiverData {
    struct WaterLevelRecord {
        uint256 timestamp;
        uint256 waterLevel;  // Уровень воды в сантиметрах
    }

    mapping(uint256 => WaterLevelRecord) public records;
    uint256 public recordCount;

    function addWaterLevelRecord(uint256 _timestamp, uint256 _waterLevel) public {
        records[recordCount] = WaterLevelRecord(_timestamp, _waterLevel);
        recordCount++;
    }

    function getWaterLevelRecord(uint256 _index) public view returns (uint256, uint256) {
        return (records[_index].timestamp, records[_index].waterLevel);
    }
}
'''

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:OskaRiverData']
bytecode = contract_interface['bin']
abi = contract_interface['abi']

# Подключение к Ethereum-сети
w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))  # Замените на ваш Infura ID

# Создание аккаунта (для демонстрации)
account = w3.eth.account.create()
private_key = account.key.hex()

# Развертывание контракта
OskaRiverData = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(account.address)

transaction = OskaRiverData.constructor().buildTransaction({
    'chainId': 1,
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
    'nonce': nonce
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Ожидание подтверждения транзакции
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt.contractAddress

### Шаг 4: Интеграция данных в блокчейн
oska_river_data_contract = w3.eth.contract(address=contract_address, abi=abi)

# Добавление записей о стоке реки в блокчейн
for index, row in data.iterrows():
    nonce = w3.eth.getTransactionCount(account.address)
    
    transaction = oska_river_data_contract.functions.addWaterLevelRecord(
        int(row['timestamp']),  # Предполагается, что есть столбец 'timestamp'
        int(row['water_level'])  # Предполагается, что есть столбец 'water_level'
    ).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': nonce
    })
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

### Шаг 5: Визуализация данных на карте
# Создание интерактивной карты с использованием folium
m = folium.Map(location=[42.8670, 139.6917], zoom_start=10)  # Координаты реки Осек

# Добавление маркера на карте (пример)
folium.Marker(
    location=[42.8670, 139.6917],
    popup='Сток реки Осек',
    icon=folium.Icon(icon="info-sign")
).add_to(m)

# Сохранение карты в HTML файл
m.save("238.html")

print("Карта сохранена как 238.html")