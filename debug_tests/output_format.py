import pandas as pd
import re
import matplotlib.pyplot as plt


# The given string
data_str = "NAT+3.40000E-04,NAI+00.0000E-03,WAV+0.00000E+00,NAT+5.47000E-03,NAI+00.0000E-03,WAV+0.05260E+00,NAT+1.06400E-02,NAI+00.0000E-03,WAV+0.10530E+00,NAT+1.58000E-02,NAI+00.0000E-03,WAV+0.15790E+00,NAT+2.09500E-02,NAI+00.0000E-03,WAV+0.21050E+00,NAT+2.61500E-02,NAI+00.0000E-03,WAV+0.26320E+00,NAT+3.12700E-02,NAI-00.0005E-03,WAV+0.31580E+00,NAT+3.64800E-02,NAI+00.0000E-03,WAV+0.36840E+00,NAT+4.15900E-02,NAI+00.0000E-03,WAV+0.42110E+00,NAT+4.67500E-02,NAI+00.0000E-03,WAV+0.47370E+00,NAT+5.19600E-02,NAI+00.0000E-03,WAV+0.52630E+00,NAT+5.71600E-02,NAI+00.0000E-03,WAV+0.57890E+00,NAT+6.23500E-02,NAI+00.0000E-03,WAV+0.63160E+00,NAT+6.74800E-02,NAI+00.0000E-03,WAV+0.68420E+00,NAT+7.25900E-02,NAI+00.0000E-03,WAV+0.73680E+00,NAT+7.77100E-02,NAI+00.0000E-03,WAV+0.78950E+00,NAT+8.28400E-02,NAI-00.0005E-03,WAV+0.84210E+00,NAT+8.77300E-02,NAI+00.0000E-03,WAV+0.89470E+00,NAT+9.28500E-02,NAI+00.0000E-03,WAV+0.94740E+00,NAT+9.79700E-02,NAI+00.0000E-03,EAV+1.00000E+00"

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