from dotenv import load_dotenv
from incomeandexpense import start, income_conv, undo_latest
from report import summary, send_monthly_report
from database import initialise_database, clear_old
from help import help
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from datetime import time
#Admin stuff
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

#Main program
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(income_conv)
    app.add_handler(CallbackQueryHandler(summary,pattern="^menu_report$"))
    app.add_handler(CallbackQueryHandler(undo_latest, pattern="^menu_undo$"))
    app.add_handler(CallbackQueryHandler(help, pattern="^menu_help$"))
    app.add_handler(CommandHandler("start", start))
    
    app.job_queue.run_monthly(send_monthly_report,when=time(hour=4, minute=0),day=1,)
    app.job_queue.run_monthly(clear_old,when=time(hour=0, minute=0),day=1,)
    
    initialise_database()
    app.run_polling()


if __name__ == "__main__":
    main()