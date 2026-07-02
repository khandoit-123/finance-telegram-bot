from database import get_month_summary, get_all_users
from datetime import datetime

def generate_report(user_id):
    now = datetime.now()
    curr_month = now.month
    curr_year = now.year

    report = "***REPORT***\n\n\n"

    for month in range(1, curr_month + 1):
        income, expense = get_month_summary(user_id, month, curr_year)

        report += f"{month}/{curr_year}\n"

        report += "Income:\n"
        if income:
            for category, amount in income.items():
                report += f"  {category}: ${amount:.2f}\n"
        else:
            report += "  None\n"

        report += "\nExpense:\n"
        if expense:
            for category, amount in expense.items():
                report += f"  {category}: ${abs(amount):.2f}\n"
        else:
            report += "  None\n"

        total_income = sum(income.values())
        total_expense = abs(sum(expense.values()))
        savings = total_income - total_expense

        report += f"\nTotal Income: ${total_income:.2f}\n"
        report += f"Total Expense: ${total_expense:.2f}\n"
        report += f"Total Savings: ${savings:.2f}\n"
        report += "-" * 10 + "\n\n\n"

    return report

async def summary(update, context):
    query = update.callback_query
    await query.answer()

    report = generate_report(update.effective_user.id)

    await query.message.reply_text(report)

async def send_monthly_report(context):
    users = get_all_users()

    for user_id in users:
        report = generate_report(user_id)

        await context.bot.send_message(
            chat_id=user_id,
            text=report
        )