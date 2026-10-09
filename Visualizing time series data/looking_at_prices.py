
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
month = 3
N = 96
epsilon = 0.05
scale = 4

days = range(1,14)
df = []

for day in days:

	url = "https://www.elprisetjustnu.se/api/v1/prices/" + num_to_text(year) + "/" + num_to_text(month) + "-" + num_to_text(day) + "_" + "SE3" + ".json" 

	response = requests.get(url, timeout=30)
	response.raise_for_status()  # Raises an error if the HTTP request failed
	
	data = response.json()  # Convert JSON into Python dictionaries/lists

	df.append(pd.json_normalize(data)["SEK_per_kWh"])


series_raw = np.vstack(df).reshape((1,N*len(days)))[0]


plt.plot([i/scale for i in range(0,len(series_raw))], series_raw)

for day in days:
	plt.plot([N*(day - days[0])/scale for i in range(1,N)],[i * epsilon for i in range(1,N)], color = "red")


#series_df = pd.DataFrame(series_raw)
#series_df.plot()

plt.show()

'''


with open("data.json", "w", encoding="utf-8") as file:
	json.dump(data, file, indent=2, ensure_ascii=False)

# Inspect the structure (show only the first 2,000 characters)
print(json.dumps(data, indent=2, ensure_ascii=False)[:20000])
'''



