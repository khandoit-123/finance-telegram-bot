async def help(update, context):
    query = update.callback_query
    await query.answer()
    help = '''
    ***Commands***
    - /start:
        Starts the program
    - /cancel:
        Works for adding income and expense, cancels current operation
    - Add Income:
        Add your earnings like salary, allowance etc
    - Add Expense:
        Add your expenditure like food, transport etc
    - Report:
        Returns a monthly report for the current year
    - Undo:
        Undo your latest expenditure/income
           '''
    await query.message.reply_text(help)