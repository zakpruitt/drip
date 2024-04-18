import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./resources/credentials.json', scope)
client = gspread.authorize(creds)
worksheet = client.open('drip').sheet1

## fill in data ##
bosses = ["Gnarlroot", "Another Boss", "Overall"]
sub_headers = ["DPS", "HPS", "BDPS"]

current_column = 2
for boss in bosses:
    end_column = current_column + len(sub_headers) - 1

    # Use 'merge_cells' function with the correct parameters
    worksheet.merge_cells(start_row=1, start_col=current_column, end_row=1, end_col=end_column)

    # Update 'update_cell' to 'update' with named arguments
    worksheet.update(cell='A1', value='Player Name')

    for i, sub_header in enumerate(sub_headers):
        cell = gspread.utils.rowcol_to_a1(2, current_column + i)
        worksheet.update(cell, sub_header)

    current_column = end_column + 1


worksheet.update("Player Name", 'A1')

# Apply formatting, for example, a bold format for the headers
header_format = CellFormat(textFormat=TextFormat(bold=True))
set_frozen(worksheet, rows=1, cols=1)  # Freeze the first row and column
format_cell_ranges(worksheet, [('A1', header_format), ('B1:1', header_format)])
