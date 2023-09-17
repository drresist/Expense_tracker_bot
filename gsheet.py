import gspread
from datetime import datetime
import loguru
from dotenv import load_dotenv
import os

load_dotenv()

service_file = os.getenv("GOOGLE_SHEETS_KEY_FILE")
if service_file is None:
    raise RuntimeError("GOOGLE_SHEETS_KEY_FILE is not set")

gc = gspread.service_account(filename=os.getenv(service_file))

gc.login()
sh = gc.open_by_key(os.getenv('SHEET_ID'))

# Open the first worksheet (sheet1) by name
worksheet = sh.sheet1

# Print the value in cell A1 of the first worksheet
print(worksheet.get('A1'))


def add_payment(category_type, category, amount):
    # Append payment data to the worksheet
    worksheet.append_row([str(datetime.now()), category_type, category, amount])
    loguru.logger.info(f"Added payment: {category} - {amount}")
