import telebot
from telebot import types
from loguru import logger
import os
from dotenv import load_dotenv
from gsheet import add_payment, get_categories

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

@bot.message_handler(commands=['reload'])
def reload_categories(message):
    categories['Income'] = get_categories('Income')
    categories['Expense'] = get_categories('Expense')
    logger.info("Reloaded categories")
    logger.info("New categories:")
    logger.info(categories)



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

# Create a dictionary to store user-defined categories
custom_categories = {}

@bot.message_handler(commands=['addcategory'])
def add_category(message):
    bot.send_message(message.chat.id, "Enter the name of the new category in next format. Example\n"
                                      "Income:auto")
    bot.register_next_step_handler(message, process_new_category)
    bot.send_message(message.chat.id, "Enter the name of the new category:")

def process_new_category(message):
    category_name = message.text
    user_id = message.from_user.id

    # Store the custom category for the user
    custom_categories[user_id] = custom_categories.get(user_id, [])
    custom_categories[user_id].append(category_name)

    bot.send_message(message.chat.id, f"Category '{category_name}' added successfully!")

# Modify the 'handle_category' function to include custom categories
@bot.message_handler(func=lambda message: message.text in categories.get(user_data.get('category_type', ''), []) or message.text in custom_categories.get(message.from_user.id, []))
def handle_category(message):
    user_data['category'] = message.text
    bot.send_message(message.chat.id, f"You selected: {user_data['category']}\n\nEnter the amount:")

# Modify the 'view_categories' function to show custom categories
@bot.message_handler(commands=['viewcategories'])
def view_categories(message):
    user_id = message.from_user.id
    user_categories = custom_categories.get(user_id, [])

    if user_categories:
        categories_str = "\n".join(user_categories)
        bot.send_message(message.chat.id, f"Your custom categories:\n{categories_str}")
    else:
        bot.send_message(message.chat.id, "You haven't added any custom categories yet.")

@bot.message_handler(commands=['help'])
def display_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_start = types.KeyboardButton("/start")
    item_add_category = types.KeyboardButton("/addcategory")
    item_view_categories = types.KeyboardButton("/viewcategories")
    item_view_summary = types.KeyboardButton("/viewsummary")
    markup.add(item_start, item_add_category, item_view_categories, item_view_summary)

    commands_text = "Here are some commands you can use:"
    bot.send_message(message.chat.id, commands_text, reply_markup=markup)


if __name__ == '__main__':
    bot.polling()
