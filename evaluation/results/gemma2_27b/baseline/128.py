import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression # Example model, choose appropriate one
from sklearn.metrics import accuracy_score
import folium

# 1. Load data (replace with actual file and column names)
data = pd.read_csv("lepsy_river_data.csv")

# 2. Preprocess data (handle missing values, convert to numerical format if needed)
# ...

# 3. Choose features for prediction (e.g., water level, precipitation)
features = ["water_level", "precipitation"] # Replace with actual column names
target = "flood" # Replace with the column name indicating flood occurrence

X = data[features]
y = data[target]

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 5. Train the model (replace with chosen model)
model = LogisticRegression() # Example model
model.fit(X_train, y_train)

# 6. Evaluate model accuracy on testing set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# 7. Predict flood probability for Dos River (replace with actual data for Dos River)
dos_river_data = pd.read_csv("dos_river_data.csv")[features] # Replace with actual file and column names
flood_probability = model.predict_proba(dos_river_data)[:, 1]

# 8. Visualize results on map (replace with actual coordinates for Dos River)
m = folium.Map(location=[40, -10], zoom_start=6) # Replace with actual coordinates
folium.GeoJson("dos_river_boundary.geojson").add_to(m)

# Add markers based on flood probability (replace with appropriate visualization logic)
for i in range(len(flood_probability)):
    folium.Marker([40, -10], popup=f"Flood Probability: {flood_probability[i]:.2f}").add_to(m)

m.save("128.html")