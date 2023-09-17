import telebot
from telebot import types
from loguru import logger
import os
from dotenv import load_dotenv
from gsheet import add_payment

load_dotenv()

token = os.getenv('TOKEN')
if token is None:
    raise RuntimeError("TOKEN is not set")
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot(token)

# Dictionary to store transaction data
user_data = {}

# Dictionary of categories for income and expense
categories = {
    'Income': ['Salary', 'Freelance', 'Investment'],
    'Expense': ['Food', 'Transportation', 'Rent'],
}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_income = types.KeyboardButton("Income")
    item_expense = types.KeyboardButton("Expense")
    markup.add(item_income, item_expense)

    bot.send_message(message.chat.id, "Welcome to the Expense Tracker Bot! "
                                      "Please choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["Income", "Expense"])
def handle_choice(message):
    user_data['category_type'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for category in categories[message.text]:
        markup.add(category)

    bot.send_message(message.chat.id, f"Choose a category for {message.text.lower()}:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in categories.get(user_data.get('category_type', ''), []))
def handle_category(message):
    user_data['category'] = message.text
    bot.send_message(message.chat.id, f"You selected: {user_data['category']}\n\nEnter the amount:")


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
    # TODO: add to sql record

    user_data.clear()


if __name__ == '__main__':
    bot.polling()
