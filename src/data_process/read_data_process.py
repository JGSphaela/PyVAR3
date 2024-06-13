# src/data_process/read_data_process.py

import pandas as pd
import re

class read_data_process:
    def __init__(self, read_data: str):
        """
        Class for process data read from B1500.
        :param read_data:
        """
        self.read_data = read_data