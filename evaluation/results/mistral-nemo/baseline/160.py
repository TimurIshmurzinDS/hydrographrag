import pandas as pd
import matplotlib.pyplot as plt
import folium

# Load Ili River water discharge data
ili_data = pd.read_csv('ili_river_data.csv')
ili_data['date'] = pd.to_datetime(ili_data['date'])
ili_data.set_index('date', inplace=True)
ili_series = ili_data['discharge']

# Load Shyzhyn River water discharge data
shyzhyn_data = pd.read_csv('shyzhyn_river_data.csv')
shyzhyn_data['date'] = pd.to_datetime(shyzhyn_data['date'])
shyzhyn_data.set_index('date', inplace=True)
shyzhyn_series = shyzhyn_data['discharge']

# Create a frequency series for each river
ili_freq = ili_series.resample('M').mean()
shyzhyn_freq = shyzhyn_series.resample('M').mean()

# Plot histograms for each month of the year
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

for i, month in enumerate(months):
    ili_data_month = ili_freq[month]
    shyzhyn_data_month = shyzhyn_freq[month]

    plt.figure(figsize=(10, 5))
    plt.hist(ili_data_month, bins=30, alpha=0.5, label='Ili River')
    plt.hist(shyzhyn_data_month, bins=30, alpha=0.5, label='Shyzhyn River')
    plt.legend()
    plt.title(f'Water discharge in {month}')
    plt.show()

# Create a map with the locations of both rivers
m = folium.Map(location=[45.015, 72.393], zoom_start=6)

folium.GeoJson(
    ili_data[['geometry']],
    style_function=lambda x: {'fillColor': 'blue', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': 'yellow'}),
).add_to(m)

folium.GeoJson(
    shyzhyn_data[['geometry']],
    style_function=lambda x: {'fillColor': 'red', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': 'yellow'}),
).add_to(m)

m.save("160.html")