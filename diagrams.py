from datetime import datetime, timedelta

import plotly.graph_objects as go


# data = get_all_vals()


def filter_data_by_last_month(data):
    today = datetime.today()
    last_month_start = today - timedelta(days=today.day)
    filtered_data = []

    for row in data[1:]:
        date_str = row[0]
        operation_type = row[1]
        date = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')

        if last_month_start <= date <= today and operation_type == "Expense":
            filtered_data.append(row)

    return filtered_data


def group_expenses_by_date_category(data):
    expenses_by_date_category = {}

    for row in data:
        date_str, _, category, amount_str = row
        amount = int(amount_str.strip().replace("\xa0", ""))
        date = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S').date()

        if date not in expenses_by_date_category:
            expenses_by_date_category[date] = {}

        if category in expenses_by_date_category[date]:
            expenses_by_date_category[date][category] += amount
        else:
            expenses_by_date_category[date][category] = amount

    return expenses_by_date_category


def create_stacked_bar_chart(data):
    filtered_data = filter_data_by_last_month(data)
    expenses_by_date_category = group_expenses_by_date_category(filtered_data)

    dates = list(expenses_by_date_category.keys())
    unique_categories = list(
        set(category for categories in expenses_by_date_category.values() for category in categories))

    traces = []

    for category in unique_categories:
        amounts = [expenses_by_date_category[date].get(category, 0) for date in dates]
        trace = go.Bar(x=[date.strftime('%d.%m.%Y') for date in dates], y=amounts, name=category)
        traces.append(trace)

    fig = go.Figure(data=traces)

    fig.update_layout(
        xaxis=dict(title='Date', tickangle=45),
        yaxis=dict(title='Amount'),
        barmode='stack',
        title='Expense by Date and Category (Last Month)'
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    fig.write_image("month_expense.png")
