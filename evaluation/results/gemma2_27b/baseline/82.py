import requests
import pandas as pd
from folium import Map, FeatureGroup, GeoJson


# API endpoint for river posts data (replace with actual URL)
posts_url = "https://api.example.com/river-posts?river=Karaoy River"

# API endpoint for water discharge data (replace with actual URL)
discharge_url = "https://api.example.com/water-discharge?location={post_id}"

# Critical discharge level (replace with actual value)
critical_level = 100


def main():
    # Load posts data from API
    posts_response = requests.get(posts_url)
    posts_data = pd.DataFrame(posts_response.json())

    # Create map object
    m = Map(location=[45, 30], zoom_start=12)

    # Feature group for posts exceeding critical level
    exceeding_posts = FeatureGroup(name="Posts Exceeding Critical Level")

    for index, row in posts_data.iterrows():
        post_id = row["id"]
        lat = row["latitude"]
        lon = row["longitude"]

        # Get discharge data for the post
        discharge_response = requests.get(discharge_url.format(post_id=post_id))
        discharge_data = discharge_response.json()

        # Check if discharge exceeds critical level
        if discharge_data["value"] > critical_level:
            exceeding_posts.add_child(GeoJson(
                {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            ))

    m.add_child(exceeding_posts)
    m.save("82.html")


if __name__ == "__main__":
    main()