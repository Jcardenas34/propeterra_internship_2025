import os
import folium


# Declaring the mapbox api token for full access throughout script
# Define your mapbox api key in your environment variables for this to work
mapbox_access_token = os.getenv('MAPBOX_API_KEY')

# Create a map with default OpenStreetMap tiles
def create_map_without_mapbox():
    m = folium.Map(
        location=[37.7749, -122.4194],  # Coordinates for San Francisco
        zoom_start=12
    )

    # Add a marker
    folium.Marker(
        location=[37.7749, -122.4194],
        popup='San Francisco',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    # Save the map to an HTML file
    m.save('map_without_mapbox.html')

# Create a map with Mapbox tiles
def create_map_with_mapbox(mapbox_access_token):
    m = folium.Map(
        location=[37.7749, -122.4194],  # Coordinates for San Francisco
        zoom_start=12,
        tiles=f'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{{z}}/{{x}}/{{y}}?access_token={mapbox_access_token}',
        attr='Mapbox'
    )

    # Add a marker
    folium.Marker(
        location=[37.7749, -122.4194],
        popup='San Francisco',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    # Save the map to an HTML file
    m.save('map_with_mapbox.html')



def main(mapbox_access_token):
    '''
    
    '''
    create_map_without_mapbox()
    create_map_with_mapbox(mapbox_access_token)

if __name__ == "__main__":


    main(mapbox_access_token)

