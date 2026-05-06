python
         import folium
         import pandas as pd
         from shapely.geometry import Point, Polygon
         from scipy.spatial import distance_matrix
         import numpy as np
         # Load flood level data
         flood_data = pd.read_csv('flood_level_sharyn.csv')
         # Create a map centered around the area of interest
         m = folium.Map(location=[55.76, 49.12], zoom_start=10)
         # Add flood level data to the map
         for i in range(len(flood_data)):
             folium.CircleMarker(
                 location=[flood_data.iloc[i]['lat'], flood_data.iloc[i]['lon']],
                 radius=flood_data.iloc[i]['level']*10,
                 color='blue',
                 fill=True,
                 fill_color='blue'
             ).add_to(m)
         # Define safe zone for apple picking
         safe_zone = Polygon([(55.74, 49.10), (55.76, 49.12), (55.78, 49.10), (55.76, 49.08)])
         # Generate random apple orchard points within the safe zone
         np.random.seed(0)
         num_points = 10
         x = np.random.uniform(safe_zone.bounds[0], safe_zone.bounds[2], size=num_points)
         y = np.random.uniform(safe_zone.bounds[1], safe_zone.bounds[3], size=num_points)
         apple_orchard = [Point(x[i], y[i]) for i in range(num_points)]
         # Add apple orchard points to the map
         for point in apple_orchard:
             folium.CircleMarker(
                 location=[point.y, point.x],
                 radius=5,
                 color='green',
                 fill=True,
                 fill_color='green'
             ).add_to(m)
         # Define a function to calculate the optimal route for apple picking
         def optimize_route(points):
             coords = [(point.y, point.x) for point in points]
             dist_matrix = distance_matrix(coords, coords)
             start = np.random.choice(range(len(points)))
             route = [start]
             while len(route) < len(points):
                 last = route[-1]
                 next_point = np.argmin([dist if i not in route else np.inf for i, dist in enumerate(dist_matrix[last])])
                 route.append(next_point)
             return [points[i] for i in route]
         # Calculate the optimal route for apple picking
         optimal_route = optimize_route(apple_orchard)
         # Add the optimal route to the map
         folium.PolyLine([(point.y, point.x) for point in optimal_route], color='red').add_to(m)
         # Save the final map
         m.save("226.html")