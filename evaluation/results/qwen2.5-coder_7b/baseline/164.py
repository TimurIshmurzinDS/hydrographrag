import pandas as pd
import numpy as np
from scipy.stats import norm, expon
import folium
from folium.plugins import MarkerCluster

# Пример данных: исторические уровни воды на реках Ili и Shynzhaly
data = {
    'date': ['2019-01-01', '2019-01-02', '2019-01-03', '2019-01-04', '2019-01-05'],
    'Ili': [1.2, 1.3, 1.4, 1.5, 1.6],
    'Shynzhaly': [0.8, 0.9, 1.0, 1.1, 1.2]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Визуализация данных
m = folium.Map(location=[43.6589, 70.2518], zoom_start=10)

marker_cluster = MarkerCluster().add_to(m)

for index, row in df.iterrows():
    folium.Marker([row['Ili'], row['Shynzhaly']], popup=f"Ili: {row['Ili']}, Shynzhaly: {row['Shynzhaly']}").add_to(marker_cluster)

m.save("164.html")

# Анализ данных
def fit_distribution(data):
    dist_names = ['norm', 'expon']
    dist_results = []
    
    for dist_name in dist_names:
        dist = getattr(norm, dist_name)
        params = dist.fit(data)
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]
        
        pdf_fitted = dist.pdf(np.linspace(min(data), max(data)), *arg, loc=loc, scale=scale)
        dist_results.append((dist_name, arg, loc, scale, pdf_fitted))
    
    return dist_results

# Прогнозирование вероятности экстремальных паводков
def predict_extreme_probability(dist_results, threshold):
    extreme_probabilities = []
    
    for dist_name, arg, loc, scale, pdf_fitted in dist_results:
        if dist_name == 'norm':
            extreme_prob = 1 - norm.cdf(threshold, *arg, loc=loc, scale=scale)
        elif dist_name == 'expon':
            extreme_prob = 1 - expon.cdf(threshold, *arg, loc=loc, scale=scale)
        
        extreme_probabilities.append((dist_name, extreme_prob))
    
    return extreme_probabilities

# Пример использования
Ili_dist_results = fit_distribution(df['Ili'])
Shynzhaly_dist_results = fit_distribution(df['Shynzhaly'])

threshold_Ili = 2.0
threshold_Shynzhaly = 1.5

extreme_prob_Ili = predict_extreme_probability(Ili_dist_results, threshold_Ili)
extreme_prob_Shynzhaly = predict_extreme_probability(Shynzhaly_dist_results, threshold_Shynzhaly)

print("Вероятность экстремальных паводков на реке Ili:")
for dist_name, prob in extreme_prob_Ili:
    print(f"{dist_name}: {prob:.4f}")

print("\nВероятность экстремальных паводков на реке Shynzhaly:")
for dist_name, prob in extreme_prob_Shynzhaly:
    print(f"{dist_name}: {prob:.4f}")