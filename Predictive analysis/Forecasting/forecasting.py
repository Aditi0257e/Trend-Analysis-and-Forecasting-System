import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import json

# Load JSON data
file_path = r'all_hastags_post_counts.json'  # Adjust path to your JSON file location
with open(file_path, 'r') as file:
    all_hashtags_post_counts = json.load(file)

# Extract data for a specific hashtag (e.g., "saree")
hashtag = 'sneakers'
dates = all_hashtags_post_counts[hashtag]

# Convert to DataFrame
df = pd.DataFrame(list(dates.items()), columns=['date', 'count'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Resample the data by day (you can change this to 'H' for hourly if needed)
df = df.resample('D').sum()  # Change 'D' to 'H' for hourly

# Fit ARIMA model
model = ARIMA(df['count'], order=(1, 1, 1))  # ARIMA(p, d, q)
model_fit = model.fit()

# Forecast for the next 5 days (change this according to your needs)
forecast_steps = 5
forecast = model_fit.forecast(steps=forecast_steps)

# Plot the original data and forecasted data
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['count'], label='Original')
plt.plot(df.index[-1] + pd.to_timedelta(range(1, forecast_steps + 1), unit='D'), forecast, label='Forecast', color='red')
plt.xlabel('Date')
plt.ylabel('Number of Posts')
plt.title(f'Instagram Posts with ARIMA Forecast for #{hashtag}')
plt.legend()
plt.show()
