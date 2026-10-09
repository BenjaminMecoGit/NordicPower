
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def num_to_text(num): 
	if num < 10:
		return "0" + str(num)
	else:
		return str(num)


year = 2026
month = 6
days = range(1,30)

N = 100
epsilon = 0.05

series_raw = []
day_ends = [0]
total_points = 0

for day in days:

	url = "https://www.elprisetjustnu.se/api/v1/prices/" + num_to_text(year) + "/" + num_to_text(month) + "-" + num_to_text(day) + "_" + "SE3" + ".json" 

	response = requests.get(url, timeout=30)
	response.raise_for_status()  # Raises an error if the HTTP request failed

	# storing the data
	data = response.json()  # Convert JSON into Python dictionaries/lists
	new_data = pd.json_normalize(data)["SEK_per_kWh"].to_numpy()
	series_raw = np.concatenate([series_raw,new_data])

	# remembering the number of datapoints corresponding to this day
	if len(day_ends) == 1:
		day_ends.append(len(new_data))
	else:
		day_ends.append(len(new_data) + day_ends[-1])
	
# first vertical line
plt.plot([0 for j in range(0,N)],[j * epsilon for j in range(0,N)], color = "red")

for i in range(1,len(day_ends)):
	scale = 24 / (day_ends[i] - day_ends[i - 1])

	# vertical line at the end of the day
	plt.plot([day_ends[i] * scale for j in range(day_ends[i - 1],day_ends[i])],[j * epsilon for j in range(0,day_ends[i] - day_ends[i - 1])], color = "red")

	# the data for this particular day
	plt.plot([i * scale for i in range(day_ends[i - 1], day_ends[i])], series_raw[day_ends[i - 1]: day_ends[i]], color = "blue")


plt.show()





