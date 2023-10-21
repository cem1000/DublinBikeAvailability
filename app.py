import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

import pandas as pd

def load_data():
    df = pd.read_csv('dublinbikes.csv')
    return df


def get_color_and_status(capacity_ratio, mode):
    if mode == "Picking Up":
        if capacity_ratio < 0.25:
            return 'red', 'Low availability of bikes'
        elif capacity_ratio < 0.75:
            return 'orange', 'Medium availability of bikes'
        else:
            return 'green', 'High availability of bikes'
    else:  # Dropping Off
        if capacity_ratio < 0.25:
            return 'green', 'High availability of bike stands'
        elif capacity_ratio < 0.75:
            return 'orange', 'Medium availability of bike stands'
        else:
            return 'red', 'Low availability of bike stands'



        
def plot_map_for_hour_and_day(time_interval, day, mode, data):
    filtered_data = data[(data['time_interval'] == time_interval) & (data['day_of_week'] == day)]
    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=14)
    
    for _, row in filtered_data.iterrows():
        color, availability = get_color_and_status(row['capacity_ratio'], mode)
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=availability,
            icon=folium.Icon(color=color),
        ).add_to(m)

    return m



# Streamlit UI
st.markdown("# Dublin Bikes Availability")

# Description
st.write("""
This app displays the availability of Dublin Bikes based on the selected day and hour from the last 14 days of data.
Markers on the map represent bike stations. Their color indicates bike availability:
- **Green**: Good availability for picking up bikes.
- **Orange**: Medium availability.
- **Red**: Low availability for picking up and low capacity for dropping off.
""")

# A prompt to guide users to use the sidebar
st.sidebar.title("Select Time Interval and Day")
st.sidebar.text("""
Use the filters below to 
select the day and time interval
This gets you what the typical 
availablility was in the past two weeks!""")

# Choose Mode (Reduced Gap)
st.markdown("### Choose mode:", unsafe_allow_html=True)
mode = st.radio("", ["Picking Up", "Dropping Off"])

# Load data only if it hasn't been loaded yet
if 'data' not in st.session_state:
    st.session_state.data = load_data()




with st.sidebar:
    st.header("Filters")
    # Order days from Monday to Sunday
    days_ordered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = st.selectbox("Select Day:", days_ordered, key="day_selectbox")

    # Order time intervals logically
    intervals_ordered = sorted(st.session_state.data['time_interval'].unique())

    # Setting default time interval
    default_time_interval = "09:00 - 09:30"
    default_index = intervals_ordered.index(default_time_interval)

    time_interval = st.selectbox("Select Time Interval:", intervals_ordered, index=default_index, key="time_interval_selectbox")


st.write(f"Selected Day: {day} | Time Interval: {time_interval}")

# Use the user's selections to update the map
map_data = plot_map_for_hour_and_day(time_interval, day, mode, st.session_state.data)
folium_static(map_data, width=800, height=800)
