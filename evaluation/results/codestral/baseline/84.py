python
        import pandas as pd
        import folium
        from scipy import stats

        # Load data
        hydro_posts = pd.read_csv('hydro_posts.csv')
        flow_data = pd.read_csv('flow_data.csv')

        # Merge data
        merged_data = pd.merge(hydro_posts, flow_data, on='post_id')

        # Calculate z-score for spring flood season
        merged_data['z_score'] = stats.zscore(merged_data['spring_flow'])

        # Define risk levels based on z-score
        def risk_level(z):
            if z > 2:
                return 'high'
            elif z > 1:
                return 'medium'
            else:
                return 'low'

        merged_data['risk'] = merged_data['z_score'].apply(risk_level)

        # Create map
        m = folium.Map(location=[merged_data['latitude'].mean(), merged_data['longitude'].mean()], zoom_start=10)

        # Add hydro posts to map with color based on risk level
        for i, row in merged_data.iterrows():
            if row['risk'] == 'high':
                color = 'red'
            elif row['risk'] == 'medium':
                color = 'orange'
            else:
                color = 'green'
            folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=10, color=color, fill=True, fill_color=color).add_to(m)

        # Save map
        m.save("84.html")