import pandas as pd

file_names = ["/app/output/stateUnemployment.csv", "/app/output/countyUnemployment.csv", "/app/output/placeUnemployment.csv"]
dataframes = []

for file in file_names:
    df = pd.read_csv(file)
    dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)
merged_df.to_csv("/app/output/Unemployment_data.csv", index=False)
print("'Unemployment_data.csv' Ready")
