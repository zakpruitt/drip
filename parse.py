from dataclasses import dataclass
from enum import Enum

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from warcraft_logs_api import WarcraftLogsAPI




# now write it

def flatten_data(processed_reclear_data):
    flattened_data = []
    for boss_name, performances in processed_reclear_data.items():
        for performance_type in PerformanceType:
            for performance in performances[performance_type]:
                row = {
                    'Boss Name': boss_name,
                    'Player Name': performance.name,
                    'Spec': performance.player_spec,
                    'Performance Type': performance_type.name,
                    'Rank Percent': performance.rank_percent,
                    'Amount': performance.amount
                }
                flattened_data.append(row)
    return flattened_data


# Flattening your data
flattened_data = flatten_data(processed_reclear_data)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('resources/credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('drip').sheet1

# Prepare data for batch update
header = ['Boss Name', 'Player Name', 'Spec', 'Performance Type', 'Rank Percent', 'Amount']
data_to_write = [header]
for row in flattened_data:
    data_to_write.append([
        row['Boss Name'],
        row['Player Name'],
        row['Spec'],
        row['Performance Type'],
        row['Rank Percent'],
        row['Amount']
    ])

# Define the range to update
range_to_update = f"A1:F{len(data_to_write)}"  # Adjust the range as needed

# Batch update the sheet
sheet.update(range_to_update, data_to_write, value_input_option='USER_ENTERED')