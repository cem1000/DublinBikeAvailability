import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

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

# Streamlit UI & Layout Adjustments
st.set_page_config(layout="wide")

# Title
st.title("Dublin Bikes Availability")

# Description
st.write("""
This app displays the availability of Dublin Bikes based on the selected day and hour from the last 14 days of data.
Markers on the map represent bike stations. Their color indicates bike availability.
""")

# Adding custom CSS to make it visually appealing
st.markdown("""
<style>
    div[data-baseweb="select"] > div {
        width: 250px;
    }
    .css-2trqyj {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    .css-17eq0hr {
        margin: 0.2rem !important;
    }
</style>
""", unsafe_allow_html=True)



# Load data only if it hasn't been loaded yet
if 'data' not in st.session_state:
    st.session_state.data = load_data()  # Assuming you have a load_data() function to get the data

# Adjust the widths of the columns
col1, col2, col3, col4 = st.columns([2,1,1,1]) # Adjust the numbers for desired widths

# Place your filters in the columns
col1.subheader("Choose mode:")
mode = col1.radio("", ["Picking Up", "Dropping Off"])

col2.subheader("Select Day:")
days_ordered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day = col2.selectbox("", days_ordered, key="day_selectbox")

col3.subheader("Select Time Interval:")
intervals_ordered = sorted(st.session_state.data['time_interval'].unique())
default_time_interval = "09:00 - 09:30"
default_index = intervals_ordered.index(default_time_interval)
time_interval = col3.selectbox("", intervals_ordered, index=default_index, key="time_interval_selectbox")


# Use the user's selections to update the map
map_data = plot_map_for_hour_and_day(time_interval, day, mode, st.session_state.data)

# Display the map below the filters
folium_static(map_data, width=1200, height=600)

