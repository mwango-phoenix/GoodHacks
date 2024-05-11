import streamlit as st
from geopy.geocoders import Photon
import pandas as pd
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Load the dataset
data = pd.read_csv('hackathon_data.csv')

# Function to get latitude and longitude from an address
def get_lat_lon(address):
    geolocator = Photon(user_agent="measurements")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)

# Function to find the nearest facility and its address
def find_nearest(lat, lon, category):
    data['Distance'] = data.apply(lambda row: geodesic((lat, lon), (row['LATITUDE'], row['LONGITUDE'])).meters, axis=1)
    sorted_data = data.sort_values('Distance')
    return sorted_data.iloc[0][category], sorted_data.iloc[0]['Address']

# Function to display the map with the route
def show_map(origin, destination, key):
    directions_result = gmaps.directions(origin, destination, mode="driving")
    m = folium.Map(location=origin, zoom_start=12)
    folium.Marker(origin, popup='Origin', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(destination, popup='Destination', icon=folium.Icon(color='red')).add_to(m)
    if directions_result:
        steps = directions_result[0]['legs'][0]['steps']
        for step in steps:
            polyline = step['polyline']['points']
            folium.PolyLine(locations=folium.util.decode_polyline(polyline), weight=2, color='blue').add_to(m)
    # Generate unique key for each map based on destination coordinates
    map_key = f"map_{key}_{destination[0]}_{destination[1]}".replace('.', '_').replace(',', '_')
    st_folium(m, width=725, height=500, key=map_key)

def main():
    st.title('Cool Compass')
    address = st.text_input('Enter your address:')
    submitted = st.button('Find')

    if submitted and address:
        lat, lon = get_lat_lon(address)
        if lat is not None and lon is not None:
            origin = (lat, lon)

            pool_name, pool_address = find_nearest(lat, lon, 'POOL_NAME')
            community_name, community_address = find_nearest(lat, lon, 'COMMUNITY_NAME')
            splash_pad_name, splash_pad_address = find_nearest(lat, lon, 'SPLASH_PAD_NAME')
            
            destination_pool = get_lat_lon(pool_address)
            destination_comm = get_lat_lon(community_address)
            destination_splash = get_lat_lon(splash_pad_address)

            # Can Implement Google Maps API to show the route
            with st.expander("Nearest Pool", expanded=True):
                st.subheader(f'{pool_name}')

            with st.expander("Nearest Community Center", expanded=True):
                st.subheader(f'{community_name}')
            
            with st.expander("Nearest Splash Pad", expanded=True):
                st.subheader(f'{splash_pad_name}')

        else:
            st.error("Address not found. Please enter a valid address.")

if __name__ == "__main__":
    main()