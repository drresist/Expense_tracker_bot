# Expense Tracker Bot

The Expense Tracker Bot is a Telegram bot that helps you keep track of your income and expenses. You can record your transactions by specifying the category and amount. This bot is a simple example and can be expanded upon to include more features and functionalities.

## Getting Started

Follow these steps to set up and use the Expense Tracker Bot:

1. **Clone the Repository**
   Clone this repository to your local machine:

   ```
   git clone https://github.com/yourusername/expense-tracker-bot.git
   ```

2. **Install Dependencies**
   Make sure you have Python and pip installed. Then, navigate to the project directory and install the required dependencies:

   ```
   pip install telebot loguru python-dotenv gspread oauth2client
   # or 
   pip install -r requirements.txt
   ```

3. **Set Up Telegram Bot**
   - Create a new bot on Telegram by talking to the BotFather.
   - Obtain your Telegram bot token.

4. **Set Up Google Sheets Integration**
   - If you want to use Google Sheets to store transaction data, create a Google Sheets document and share it with the email address associated with the service account JSON key.
   - Download the JSON key for your service account and save it as `service_account.json` in the project directory.

5. **Set Environment Variables**
   Create a `.env` file in the project directory and set the following variables:

   ```
   TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   GOOGLE_SHEETS_KEY_FILE=service_account.json
   SHEET_ID=YOUR_SHEET_ID
   ```

6. **Run the Bot**
   Execute the bot script:

   ```
   python expense_tracker_bot.py
   ```

7. **Start Tracking Expenses**
   - Start a chat with your Telegram bot and use the following commands:
     - `/start` to begin recording a transaction.
   - Choose the transaction type (Income or Expense) and category.
   - Enter the transaction amount.
   - The bot will record the transaction and display it.

8. **Customization**
   You can customize the categories for both income and expenses by modifying the `categories` dictionary in the script.

## Features and Functionality
- Record income and expenses with categories and amounts.
- Transactions are logged and can be saved to Google Sheets.
- Simple and user-friendly chat interface.
- Easily extendable and customizable.

## TODO
- Write records to DB 
- Every day send report 

# Expense_tracker_bot
