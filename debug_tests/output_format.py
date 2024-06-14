import pandas as pd
import re
import matplotlib.pyplot as plt

# The given string
data_str = "NAI+000.0000E-06,NBI-000.0050E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.000000E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.052600E+00,NAI-000.0050E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.105300E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.157900E+00,NAI+000.0000E-06,NBI-000.0050E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.210500E+00,NAI-000.0050E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.263200E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.315800E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.368400E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.421100E+00,NAI+000.0000E-06,NBI-000.0050E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.473700E+00,NAI+000.0000E-06,NBI-000.0050E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.526300E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.578900E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI-00.00050E-03,WDV+0.631600E+00,NAI+000.0000E-06,NBI-000.0050E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.684200E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.736800E+00,NAI-000.0050E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.789500E+00,NAI-000.0050E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.842100E+00,NAI+000.0000E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.894700E+00,NAI+000.0000E-06,NBI-000.0050E-06,NCI+000.0000E-06,NDI+00.00000E-03,WDV+0.947400E+00,NAI-000.0050E-06,NBI+000.0000E-06,NCI+000.0000E-06,NDI+00.00000E-03,EDV+1.000000E+00"


# Split the string by commas
entries = data_str.split(',')

# Initialize lists to store the parsed data
status = []
channel = []
data_type = []
values = []

# Regular expression to parse the data entries
pattern = re.compile(r"([A-Z])([A-Z])([A-Z])([+-]\d+\.\d+E[+-]\d{2})")

for entry in entries:
    match = pattern.match(entry)
    if match:
        status.append(match.group(1))
        channel.append(match.group(2))
        data_type.append(match.group(3))
        values.append(float(match.group(4)))

# Create a DataFrame
df = pd.DataFrame({'Status': status, 'Channel': channel, 'Data_Type': data_type, 'Value': values})

#ax = df.plot(x='Explanation', y='Value')
#plt.show()

# import ace_tools as tools; tools.display_dataframe_to_user(name="Lab Instrument Data", dataframe=df)

# Display the DataFrame
print(df)


# Sample DataFrame
# data = {
#     'Status': ['N', 'N', 'N', 'N', 'W', 'N', 'N', 'N', 'N', 'E'],
#     'Channel': ['A', 'B', 'C', 'D', 'D', 'A', 'B', 'C', 'D', 'D'],
#     'Data_Type': ['I', 'I', 'I', 'I', 'V', 'I', 'I', 'I', 'I', 'V'],
#     'Value': [0.0, -5e-09, 0.0, 0.0, 0.0, -5e-09, 0.0, 0.0, 0.0, 1.0]
# }
#
# df = pd.DataFrame(data)

# Detect unique combinations of channels and data types
unique_combinations = sorted(set(df['Channel'] + '_' + df['Data_Type']))

# Initialize variables
reshaped_data = []
current_row = {}
index = 0

# Iterate over the DataFrame
for _, row in df.iterrows():
    if row['Status'] == 'E':
        reshaped_data.append(current_row)
        break
    if row['Status'] == 'W':
        reshaped_data.append(current_row)
        current_row = {}
        index += 1
        continue
    column_name = f"{row['Channel']}_{row['Data_Type']}"
    current_row[column_name] = row['Value']

# Convert the list of dictionaries to a DataFrame
reshaped_df = pd.DataFrame(reshaped_data, columns=unique_combinations)

print(reshaped_df)
