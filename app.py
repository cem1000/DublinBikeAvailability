import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import datetime
import pytz
import streamlit.components.v1 as components

google_analytics_script = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2D3Y5N8KXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2D3Y5N8KXX');
</script>
"""

# Use the `html` method to inject HTML into the app.
# The height is set to zero since we don't need to display anything.
components.html(google_analytics_script, height=0)

def load_data():
    df = pd.read_csv('dublinbikes.csv')
    return df

def get_color_and_status(capacity_ratio, mode):
    if mode == "Picking Up":
        if capacity_ratio <= 0.2:
            return 'red', 'Very Low availability'
        elif capacity_ratio <= 0.4:
            return 'orange', 'Low availability'
        elif capacity_ratio <= 0.6:
            return 'beige', 'Moderate availability'
        elif capacity_ratio <= 0.8:
            return 'green', 'High availability'
        else:
            return 'lightgreen', 'Very High availability'
    else:  # Dropping Off
        if capacity_ratio <= 0.2:
            return 'lightgreen', 'Very High availability of stands'
        elif capacity_ratio <= 0.4:
            return 'green', 'High availability of stands'
        elif capacity_ratio <= 0.6:
            return 'beige', 'Moderate availability of stands'
        elif capacity_ratio <= 0.8:
            return 'orange', 'Low availability of stands'
        else:
            return 'red', 'Very Low availability of stands'


        
def plot_map_for_hour_and_day(time_interval, day, mode, data):
    filtered_data = data[(data['time_interval'] == time_interval) & (data['day_of_week'] == day)]
    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=14)
    
    for _, row in filtered_data.iterrows():
        color, availability = get_color_and_status(row['capacity_ratio'], mode)
        label = f"{row['address']} - {availability}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=label,
            icon=folium.Icon(color=color),
        ).add_to(m)

    return m

st.set_page_config(layout="wide")

# Streamlit UI
st.markdown("# Dublin Bikes Historical Availability")

# Description
st.write("""
This app showcases the typical availability of Dublin Bikes over the last 14 days. 
If you're planning your commute and often find no bikes available at 8 AM, use this app to discover the best time to get one. 

Remember, this app does not have real time data. Only holds last 14 days historical data. For real time data, visit https://www.dublinbikes.ie/en/mapping. 
Markers indicate bike stations and their colors represent availability:
- **Very High (Green)**: Plentiful bikes or stands.
- **High (Light Green)**: Good number of bikes or stands.
- **Moderate (Orange)**: Average availability.
- **Low (Dark Orange)**: Limited bikes or stands.
- **Very Low (Red)**: Hardly any bikes or stands available.
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



def get_current_irish_time():
    # Convert current UTC time to Irish local time
    current_time = datetime.datetime.utcnow()
    tz_dublin = pytz.timezone('Europe/Dublin')
    local_time = current_time.astimezone(tz_dublin)

    # Fetch current day of the week
    day_of_week = local_time.strftime('%A') # This will give you 'Monday', 'Tuesday' etc.

    # Get the current time interval
    current_hour = local_time.hour
    current_minute = local_time.minute
    if current_minute >= 30:
        next_hour = (current_hour + 1) % 24  # handle case for end of day
        interval = f"{current_hour:02d}:30 - {next_hour:02d}:00"
    else:
        if current_hour == 0:
            prev_hour = 23
        else:
            prev_hour = current_hour - 1
        interval = f"{prev_hour:02d}:30 - {current_hour:02d}:00"

    return day_of_week, interval

with st.sidebar:
    st.header("Filters")
    # Order days from Monday to Sunday
    days_ordered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_of_week, interval = get_current_irish_time()
    
    default_day_index = days_ordered.index(day_of_week)

    day = st.selectbox("Select Day:", days_ordered, index=default_day_index, key="day_selectbox")

    # Order time intervals logically
    intervals_ordered = sorted(st.session_state.data['time_interval'].unique())
    default_index = intervals_ordered.index(interval)

    time_interval = st.selectbox("Select Time Interval:", intervals_ordered, index=default_index, key="time_interval_selectbox")



st.write(f"Selected Day: {day} | Time Interval: {time_interval}")



# Use the user's selections to update the map
map_data = plot_map_for_hour_and_day(time_interval, day, mode, st.session_state.data)
folium_static(map_data, width=800, height=600)
