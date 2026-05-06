import folium

# Create a map centered around Taldar River
m = folium.Map(location=[43.2641° N, 71.2967° E], zoom_start=10)

# Add Taldar River source as a marker
folium.Marker([43.2641, 71.2967], popup='Taldar River Source').add_to(m)

# Add other water sources along the river as markers (you can add more coordinates)
folium.Marker([43.2850, 71.3232], popup='Water Source 1').add_to(m)
folium.Marker([43.3123, 71.3678], popup='Water Source 2').add_to(m)

# Add ingredients that can be found near the river (you can add more coordinates)
folium.Marker([43.2905, 71.3345], popup='Ingredients: Berries').add_to(m)
folium.Marker([43.3087, 71.3562], popup='Ingredients: Herbs').add_to(m)

# Create a simple recipe using water from Taldar River and found ingredients
recipe = """
Water from Taldar River:
- Collect water from the river at various points.

Ingredients:
- Berries: Collect berries growing near the river.
- Herbs: Gather herbs growing along the riverbank.

Instructions:
1. Boil the collected water to make it safe for drinking and cooking.
2. Use the boiled water as the base for your dish.
3. Add the collected berries and herbs to create a unique flavor.
4. Enjoy your meal!
"""

# Display the recipe in a popup on the map center
folium.Popup(recipe).add_to(m)

# Save the final map as an HTML file named "256.html"
m.save("256.html")