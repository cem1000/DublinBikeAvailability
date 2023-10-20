import requests
from datetime import datetime, timedelta
import pandas as pd

# Define the URL
url = 'https://data.smartdublin.ie/dublinbikes-api/historical/'

# Get the current datetime
now = datetime.utcnow()

# Create an empty DataFrame to store the data
df = pd.DataFrame()

# Iterate through each hour in the last 14 days (24 hours * 14 days)
for i in range(24 * 14):
    # Calculate the datetime string for the initial datetime of each hour-long period
    init_datetime_str = (now - timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the parameters for the request
    params = {'init': init_datetime_str}
    
    # Send the GET request
    response = requests.get(url, params=params)
    
    # Check for a successful response
    if response.status_code == 201:
        # Parse the JSON response to a DataFrame
        data = response.json()
        hourly_df = pd.DataFrame(data)
        # Append the data to the DataFrame
        df = pd.concat([df, hourly_df], ignore_index=True)
    else:
        print(f'Failed to retrieve data for {init_datetime_str}: {response.status_code}')

df['last_update'] = pd.to_datetime(df['last_update'])

# Create time intervals
df['hour'] = df['last_update'].dt.hour
df['minute_interval'] = df['last_update'].dt.minute // 30 * 30  # this will give 0 or 30

# Logic for end interval
end_minute = (df['minute_interval'] + 30) % 60
end_hour = df['hour'] + ((df['minute_interval'] + 30) // 60)
    
df['time_interval'] = df['hour'].astype(str).str.zfill(2) + ':' + df['minute_interval'].astype(str).str.zfill(2) + " - " + end_hour.astype(str).str.zfill(2) + ':' + end_minute.astype(str).str.zfill(2)
    
df['day_of_week'] = df['last_update'].dt.day_name()

aggregated = df.groupby(['time_interval', 'day_of_week', 'address', 'latitude', 'longitude']).agg(
    available_bikes=('available_bikes', 'sum'),
    bike_stands=('bike_stands', 'sum')
).reset_index()
aggregated['capacity_ratio'] = aggregated['available_bikes'] / aggregated['bike_stands']

# Save to CSV (overwrites the existing file)
aggregated.to_csv('dublinbikes.csv', index=False)
print("Data saved to dublinbikes.csv")
