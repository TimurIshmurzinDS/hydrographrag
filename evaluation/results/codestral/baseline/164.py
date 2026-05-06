python
         import folium
         from hydrolib import HydrologicalModel, HydraulicModel

         # Step 1: Get river data
         ili_river = RiverData('Ili River')
         shynzhaly_river = RiverData('Shynzhaly River')

         # Step 2: Create hydrological model
         hydrology_model = HydrologicalModel()
         rainfall_data = get_rainfall_data()
         extreme_rainfall_scenarios = generate_extreme_rainfall_scenarios(rainfall_data)

         # Step 3: Generate extreme rainfall scenarios
         ili_river_probabilities = []
         shynzhaly_river_probabilities = []

         for scenario in extreme_rainfall_scenarios:
             hydrology_model.set_rainfall(scenario)
             ili_river_runoff = hydrology_model.calculate_runoff(ili_river)
             shynzhaly_river_runoff = hydrology_model.calculate_runoff(shynzhaly_river)

             # Step 4: Create hydraulic model
             hydraulic_model = HydraulicModel()
             ili_river_water_levels = hydraulic_model.calculate_water_levels(ili_river, ili_river_runoff)
             shynzhaly_river_water_levels = hydraulic_model.calculate_water_levels(shynzhaly_river, shynzhaly_river_runoff)

             # Step 5: Calculate probabilities of exceedance
             ili_probability = calculate_exceedance_probability(ili_river_water_levels, threshold=10.0)
             shynzhaly_probability = calculate_exceedance_probability(shynzhaly_river_water_levels, threshold=8.0)

             ili_river_probabilities.append(ili_probability)
             shynzhaly_river_probabilities.append(shynzhaly_probability)

         # Step 6: Visualize results on a map
         m = folium.Map()
         add_river_to_map(m, ili_river, color='blue')
         add_river_to_map(m, shynzhaly_river, color='red')
         add_probabilities_to_map(m, ili_river, ili_river_probabilities)
         add_probabilities_to_map(m, shynzhaly_river, shynzhaly_river_probabilities)
         m.save("164.html")