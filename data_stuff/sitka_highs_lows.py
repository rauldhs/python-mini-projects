from pathlib import Path
import csv
from datetime import datetime

import matplotlib.pyplot as plt

path = Path('weather data/death_valley_2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

highs = []
dates = []
lows = []

for row in reader:
    date = datetime.strptime(row[2],'%Y-%m-%d')
    try:
        high = int(row[3])
        low = int(row[4])
    except ValueError:
        print(f"missing data for {date}")
    else:
        lows.append(low)
        highs.append(high)
        dates.append(date)

fig, ax = plt.subplots()
ax.plot(dates,highs,color='red')
ax.plot(dates,lows,color='blue')
ax.fill_between(dates,highs,lows,facecolor='blue',alpha=0.1)

ax.set_title("Daily High Temperatures, 2021", fontsize=14)
ax.set_xlabel('', fontsize=6)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (F)", fontsize=10)
ax.tick_params(labelsize=6)

plt.show()