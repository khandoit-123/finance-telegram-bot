from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    CommandHandler,
)

from database import (
    add_transaction,
    delete_transaction,
    get_latest_transaction
)
AMOUNT, CATEGORY = 0,1,

###functions###
#undo function
async def undo_latest(update, context):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    latest = get_latest_transaction(user_id)
    if latest is None:
        await query.message.reply_text("There are no transactions to undo.")
        return

    delete_transaction(latest[0])
    await query.message.reply_text("Undid "+latest[2]+" ("+str(latest[1])+")")

CallbackQueryHandler(undo_latest,pattern="^menu_undo$")

#cancel function
async def cancel(update, context):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

#start function
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Add Income", callback_data="menu_income")],
        [InlineKeyboardButton("Add Expense", callback_data="menu_expense")],
        [InlineKeyboardButton("Report", callback_data="menu_report")],
        [InlineKeyboardButton("Help", callback_data="menu_help")],
        [InlineKeyboardButton("Undo latest income/expense", callback_data="menu_undo")]
    ]
    kb = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to your Finance Tracker!\nChoose an option below:",
        reply_markup=kb
    )

#remove money/spending function
async def expense_input(update, context):
    query = update.callback_query
    await query.answer()

    context.user_data["is_income"] = False

    await query.message.reply_text("Enter the amount:")
    return AMOUNT

#adding money/income function
async def income_input(update, context):
    query = update.callback_query
    await query.answer()
    context.user_data["is_income"] = True
    await query.message.reply_text("Enter the amount:")
    return AMOUNT

async def amount_received(update, context):
    try:
        amount = float(update.message.text)
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return AMOUNT

    context.user_data["amount"] = amount
    await update.message.reply_text("Enter the category:")
    return CATEGORY

async def category_received(update, context):
    context.user_data["category"] = update.message.text.upper()

    amount = context.user_data["amount"]
    if not context.user_data["is_income"]:
        amount = -amount
    category = context.user_data["category"]
    user_id = update.effective_user.id
    add_transaction(user_id, amount, category)

    await update.message.reply_text("Data recorded!")
    return ConversationHandler.END

income_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(income_input, pattern="^menu_income$"),
        CallbackQueryHandler(expense_input, pattern="^menu_expense$")],

    states={
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_received)],

        CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category_received)],
    },

    fallbacks=[CommandHandler("cancel", cancel)]
)

