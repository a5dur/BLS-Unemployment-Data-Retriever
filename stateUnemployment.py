import os
import requests
import json
import pandas as pd

def get_data(place_series_ids, df):
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    registration_key = os.getenv('BLS_API_KEY')  
    with open('state_abbreviations.json', 'r') as file:
        state_abbreviations = json.load(file)
    
    
    payload = {
        "seriesid": place_series_ids,
        "startyear": "2024",
        "endyear": "2025",
        "annualaverage": True,
        "catalog": True,
        "registrationkey": registration_key
    }
    
    json_payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json_payload, headers=headers)
    json_data = json.loads(response.text)
    data_list = []
    
    if 'Results' in json_data and 'series' in json_data['Results']:
        for series in json_data['Results']['series']:
            series_id = series['seriesID']
            
            # Extract geoid from series_id
            geoid = str(int(series_id[-15:-13]))
            
            if 'catalog' in series:
                city_name = series['catalog']['series_title'].replace("Unemployment Rate: ", "").replace(" (U)","")
                # county_name, state_abbrev = map(str, city_name_with_state.split(', '))
                # state_name = state_abbreviations.get(state_abbrev, state_abbrev)
                # city_name = f"{county_name}, {state_name}"
                
            for data_point in series['data']:
                year = data_point['year']
                month = data_point['periodName']
                value = data_point['value']
                data_list.append([geoid, series_id, city_name, year, month, value])

    df_chunk = pd.DataFrame(data_list, columns=["GeoID", "Series ID", "Place", "Year", "Month", "Unemployment Rate"])
    df = pd.concat([df, df_chunk], ignore_index=True)
    return df

full_df = pd.DataFrame(columns=["GeoID", "Series ID", "Place", "Year", "Month", "Unemployment Rate"])

with open('series_ids_states.json', 'r') as file:
    series_ids_data = json.load(file)

all_series_ids = series_ids_data.get('series_ids', [])
chunk_size = 50

for i in range(0, len(all_series_ids), chunk_size):
#for i in range(0, 100, chunk_size):
    place_series_ids = all_series_ids[i:i + chunk_size]
    
    print(f'Fetching data from {i} to {i+chunk_size} ids')
    full_df = get_data(place_series_ids, full_df)

    print('-' * 50)

csv_file_path = '/app/output/stateUnemployment.csv'
full_df.to_csv(csv_file_path, index=False)
print(f"Data saved to {csv_file_path}")
