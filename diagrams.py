from gsheet import *
from matplotlib import pyplot as plt
import numpy as np


data = get_all_vals()



def create_expense_by_date_category(data):
    expenses_by_date_category = {}
    # Extract relevant data and calculate totals by date and category
    for row in data[1:]:
        date_str = row[0]
        category = row[2]
        amount = int(row[3])
        
        # Parse the date and extract the date without time
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f').date()
        
        if date not in expenses_by_date_category:
            expenses_by_date_category[date] = {}
        
        if category in expenses_by_date_category[date]:
            expenses_by_date_category[date][category] += amount
        else:
            expenses_by_date_category[date][category] = amount

    # Extract unique categories for labeling the x-axis
    unique_categories = list(set(category for categories in expenses_by_date_category.values() for category in categories))

    # Create a grouped bar chart
    dates = list(expenses_by_date_category.keys())
    num_dates = len(dates)
    bar_width = 0.2  # Width of each bar
    index = np.arange(num_dates)  # X-axis index for the bars
    for i, category in enumerate(unique_categories):
        amounts = [expenses_by_date_category[date].get(category, 0) for date in dates]
        plt.bar(index + i * bar_width, amounts, bar_width, label=category)

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Expense by Date and Category')
    plt.xticks(index + bar_width * (num_dates / 2), dates, rotation=45)  # Set x-axis labels
    plt.savefig('expense_by_date_category.png')

