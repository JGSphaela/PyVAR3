# src/data_process/read_data_process.py

import pandas as pd
import re

'''
FMT 11 should be used. Error status is not yet handled.
'''


class DataProcess:
    def __init__(self):
        """
        Class for process data read from B1500.
        """

    @staticmethod
    def data_into_dataframe(data_read: str) -> pd.DataFrame:
        entries = data_read.split(',')  # Split input data

        status = []
        channel = []
        data_type = []
        values = []

        pattern = re.compile(r'([A-Z])([A-Z])([A-Z])([+-]\d+\.\d+E[+-]\d{2})')  # Regex Magic

        for entry in entries:
            match = pattern.match(entry)
            if match:
                status.append(match.group(1))
                channel.append(match.group(2))
                data_type.append(match.group(3))
                values.append(float(match.group(4)))

        df = pd.DataFrame({'Status': status, 'Channel': channel, 'Data_Type': data_type, 'Value': values})
        print(df)

        unique_combinations = sorted(set(df['Channel'] + '_' + df['Data_Type']))

        reshaped_data = []
        current_row = {}
        index = 0
        counter = 0  # Counter for checking FMT error

        for _, row in df.iterrows():
            column_name = f"{row['Channel']}_{row['Data_Type']}"
            current_row[column_name] = row['Value']

            # Check if we got more than 5 data in a row. Normally, it should be N Measurements and 1 Setting data.
            # Since it there is only 4 channels, more than 5 data means FMT setting is bad.
            if counter > 5:
                with open('error_input_data.txt', 'w') as file:
                    file.write(data_read)
                raise Exception('No Sweep Voltage in data, check FMT settings')
            elif row['Status'] == 'E':  # E means data for the last sweep step
                reshaped_data.append(current_row.copy())
                break
            elif row['Status'] == 'W':  # W means data for intermediate sweep step
                reshaped_data.append(current_row.copy())
                current_row = {}
                index += 1
                counter = 0

            counter += 1

        reshaped_df = pd.DataFrame(reshaped_data, columns=unique_combinations)

        sorted_columns = sorted(
            reshaped_df.columns,
            key=lambda x: (x.split('_')[1], x.split('_')[0])
        )
        reshaped_df = reshaped_df[sorted_columns]

        return reshaped_df
