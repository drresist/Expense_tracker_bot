import gspread
from datetime import datetime
import loguru
from dotenv import load_dotenv
import os

load_dotenv()

service_file = os.getenv("GOOGLE_SHEETS_KEY_FILE")
if service_file is None:
    raise RuntimeError("GOOGLE_SHEETS_KEY_FILE is not set")

gc = gspread.service_account(filename="creds/service_file.json")

gc.login()
sh = gc.open_by_key(os.getenv('SHEET_ID'))

# Open the first worksheet (sheet1) by name


def add_payment(category_type, category, amount):
    worksheet = sh.sheet1
    # Append payment data to the worksheet
    worksheet.append_row([str(datetime.now()), category_type, category, amount])
    loguru.logger.info(f"Added payment: {category} - {amount}")

def get_categories(category_type)->list:
    worksheet = sh.get_worksheet(1)
    loguru.logger.info(f"Getting categories: {category_type}")
    if category_type is None:
        return []
    if category_type == "Income":
        return worksheet.col_values(1)
    if category_type == "Expense":
        return worksheet.col_values(2)

def add_category_income(name):
    worksheet = sh.get_worksheet(1)
    worksheet.append_row([name])
    loguru.logger.info(f"Added category: {name}")

