import telebot
from telebot import types
from loguru import logger
import os
from dotenv import load_dotenv
from gsheet import add_payment, get_categories, get_all_vals
from diagrams import create_expense_by_date_category

load_dotenv()

# Load the Telegram bot token from environment variables
token = os.getenv('TOKEN')
if token is None:
    raise RuntimeError("TOKEN is not set")

# Initialize the Telegram bot
bot = telebot.TeleBot(token)

# Dictionary to store user data during interactions
user_data = {}

# Dictionary of categories for income and expense
categories = {
    'Income': ['Salary', 'Freelance', 'Investment'],
    'Expense': ['Food', 'Transportation', 'Rent'],
}

# Command to reload categories
@bot.message_handler(commands=['reload'])
def reload_categories(message):
    categories['Income'] = get_categories('Income')
    categories['Expense'] = get_categories('Expense')
    logger.info("Reloaded categories")
    logger.info("New categories:")
    logger.info(categories)
    bot.send_message(message.chat.id, "Reloaded categories\nNew categories: " + str(categories))

# Command to view transaction summary
@bot.message_handler(commands=['viewsummary'])
def view_summary(message):
    logger.info("Viewing summary")

# Command to view statistics diagram
@bot.message_handler(commands=['stat'])
def stat(message):
    data = get_all_vals()
    create_expense_by_date_category(data)
    with open('expense_by_date_category.png', 'rb') as f:
        bot.send_photo(message.chat.id, f)

# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_income = types.KeyboardButton("Income")
    item_expense = types.KeyboardButton("Expense")
    markup.add(item_income, item_expense)

    bot.send_message(message.chat.id, "Welcome to the Expense Tracker Bot! "
                                      "Please choose an option:", reply_markup=markup)

# Handle user choice of category type (Income or Expense)
@bot.message_handler(func=lambda message: message.text in ["Income", "Expense"])
def handle_choice(message):
    user_data['category_type'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for category in categories[message.text]:
        markup.add(category)

    bot.send_message(message.chat.id, f"Choose a category for {message.text.lower()}:", reply_markup=markup)

# Handle user choice of category
@bot.message_handler(func=lambda message: message.text in categories.get(user_data.get('category_type', ''), []))
def handle_category(message):
    user_data['category'] = message.text
    bot.send_message(message.chat.id, f"You selected: {user_data['category']}\n\nEnter the amount:")

# Handle user input of transaction amount
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_amount(message):
    user_data['amount'] = message.text
    transaction_info = f"Category: {user_data['category_type']}, " \
                       f"Transaction: {user_data['category']}, " \
                       f"Amount: {user_data['amount']}"
    bot.send_message(message.chat.id, f"Transaction recorded:\n{transaction_info}")

    # Log the transaction
    logger.info(transaction_info)

    add_payment(
        user_data['category_type'],
        user_data['category'],
        user_data['amount']
    )

    user_data.clear()

# Command to display help
@bot.message_handler(commands=['help'])
def display_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_start = types.KeyboardButton("/start")
    item_add_category = types.KeyboardButton("/addcategory")
    item_view_categories = types.KeyboardButton("/viewcategories")
    item_view_summary = types.KeyboardButton("/viewsummary")
    reload = types.KeyboardButton("/reload")
    markup.add(item_start, item_add_category, item_view_categories, item_view_summary, reload)

    commands_text = "Here are some commands you can use:"
    bot.send_message(message.chat.id, commands_text, reply_markup=markup)

# Start the bot
if __name__ == '__main__':
    bot.polling()
