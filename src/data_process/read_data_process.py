# src/data_process/read_data_process.py

import logging
import re

import pandas as pd

from src.gpib.exceptions import PyVARError

logger = logging.getLogger(__name__)

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
        """
        Parse raw B1500 measurement response string into a structured DataFrame.

        The raw response is a comma-separated string of encoded measurement values.
        Each value follows the pattern: [Status][Channel][Data_Type][Value]
        where Status is 'W' (intermediate step) or 'E' (final step).

        :param data_read: Raw comma-separated response string from B1500.
        :return: DataFrame with columns named as '{Channel}_{Data_Type}' (e.g. 'A_I', 'B_V').
        :raises PyVARError: If the data contains no sweep voltage or has wrong module settings.
        """
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
        logger.debug(f"Parsed {len(df)} entries from raw data")

        if df.empty:
            return pd.DataFrame()

        unique_combinations = sorted(set(df['Channel'] + '_' + df['Data_Type']))

        reshaped_data = []
        current_row = {}
        index = 0
        counter = 0  # Counter for checking FMT error

        for _, row in df.iterrows():
            column_name = f"{row['Channel']}_{row['Data_Type']}"
            current_row[column_name] = row['Value']

            # Check if we got more than [module count] data in a row. Normally, it should be N Measurements and 1 Setting data.
            # Since it there is only [module count] channels, more than [module count] data means FMT setting is bad.
            if counter > 6:
                with open('error_input_data.txt', 'w') as file:
                    file.write(data_read)
                raise PyVARError('No Sweep Voltage in data or module setting wrong, check FMT and MM settings')
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
