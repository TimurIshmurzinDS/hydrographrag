import pandas as pd
import folium

# Шаг 1: Сбор данных о криптовалютах
crypto_data = {
    'Name': ['Bitcoin', 'Ethereum', 'Ripple', 'Litecoin'],
    'MarketCap': [189076523456, 2147483647, 37879636288, 4493983936],
    'Volume': [37497700000, 13722800000, 2592000000, 288000000},
    'PriceChangePercent': [-1.23, -0.56, 0.87, -0.45]
}

crypto_df = pd.DataFrame(crypto_data)

# Шаг 2: Определение факторов влияющих на инвестиции в сельское хозяйство реки Бутак
factors_data = {
    'Country': ['Kazakhstan', 'USA', 'Japan', 'Germany'],
    'BlockchainTechAvailability': [7, 9, 8, 6],
    'PoliticalStability': [6, 8, 7, 9],
    'EconomicSituation': [7, 6, 8, 7]
}

factors_df = pd.DataFrame(factors_data)

# Шаг 3: Анализ данных о криптовалютах с учетом факторов
crypto_factors_df = pd.merge(crypto_df, factors_df, left_on='Name', right_on='Country')
crypto_factors_df['Score'] = crypto_factors_df['MarketCap'] * crypto_factors_df['BlockchainTechAvailability'] + \
                            crypto_factors_df['Volume'] * crypto_factors_df['PoliticalStability'] + \
                            crypto_factors_df['PriceChangePercent'] * crypto_factors_df['EconomicSituation']

# Шаг 4: Визуализация результатов на карте
m = folium.Map(location=[53.9162, 71.3087], zoom_start=5) # Координаты реки Бутак

for index, row in crypto_factors_df.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=f"{row['Name']}: {row['Score']}").add_to(m)

m.save("268.html")