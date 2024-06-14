import pandas as pd
import re
import matplotlib.pyplot as plt

# The given string
data_str = "NAI+00.00800E-12,NBI-00.00650E-12,NCI+00.03350E-12,WBV+0.000000E+00,NAI+00.00050E-12,NBI-00.00150E-12,NCI+00.01000E-12,WBV+0.050000E+00,NAI+00.00050E-12,NBI-00.00100E-12,NCI+00.03450E-12,WBV+0.100000E+00,NAI+00.00250E-12,NBI-00.01250E-12,NCI-00.01550E-12,WBV+0.150000E+00,NAI+00.00350E-12,NBI-00.01850E-12,NCI-00.00900E-12,WBV+0.200000E+00,NAI-00.00100E-12,NBI+00.00950E-12,NCI+00.01850E-12,WBV+0.250000E+00,NAI+00.00350E-12,NBI-00.00250E-12,NCI+00.02550E-12,WBV+0.300000E+00,NAI-00.00650E-12,NBI+00.02400E-12,NCI+00.03200E-12,WBV+0.350000E+00,NAI-00.01150E-12,NBI+00.01300E-12,NCI+00.01550E-12,WBV+0.400000E+00,NAI-00.00100E-12,NBI-00.03100E-12,NCI+00.00800E-12,WBV+0.450000E+00,NAI+00.01750E-12,NBI+00.06450E-12,NCI+00.05650E-12,WBV+0.500000E+00,NAI-00.00050E-12,NBI-00.00250E-12,NCI-00.00400E-12,WBV+0.550000E+00,NAI+00.01100E-12,NBI+00.04550E-12,NCI+00.02300E-12,WBV+0.600000E+00,NAI+00.00650E-12,NBI-00.00450E-12,NCI+00.01300E-12,WBV+0.650000E+00,NAI-00.00750E-12,NBI+00.02750E-12,NCI+00.01100E-12,WBV+0.700000E+00,NAI+00.00500E-12,NBI-00.01150E-12,NCI+00.02950E-12,WBV+0.750000E+00,NAI-00.00750E-12,NBI-00.01300E-12,NCI-00.00100E-12,WBV+0.800000E+00,NAI+00.01600E-12,NBI+00.02750E-12,NCI+00.02700E-12,WBV+0.850000E+00,NAI+00.01650E-12,NBI+00.03950E-12,NCI+00.03050E-12,WBV+0.900000E+00,NAI+00.00750E-12,NBI+00.04700E-12,NCI+00.00350E-12,WBV+0.950000E+00,NAI+00.01400E-12,NBI+00.00100E-12,NCI+00.00200E-12,EBV+1.000000E+00"



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
    column_name = f"{row['Channel']}_{row['Data_Type']}"
    current_row[column_name] = row['Value']

    if row['Status'] == 'E':
        reshaped_data.append(current_row.copy())
        break
    elif row['Status'] == 'W':
        reshaped_data.append(current_row.copy())
        current_row = {}
        index += 1

# Convert the list of dictionaries to a DataFrame
reshaped_df = pd.DataFrame(reshaped_data, columns=unique_combinations)

sorted_columns = sorted(
    reshaped_df.columns,
    key=lambda x: (x.split('_')[1], x.split('_')[0])
)
reshaped_df = reshaped_df[sorted_columns]

print(reshaped_df)
