import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # مثال: https://yourapp.onrender.com/

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً عکس خودتو بفرست تا چهره کارتونی‌ات رو بسازم.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال ساخت چهره کارتونی شما... 🎨")
    # اینجا می‌تونی درخواست API با API_KEY بفرستی
    await update.message.reply_text("✅ تصویر آماده است! (نسخه تست)")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Face Crafter Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    bot = Bot(TOKEN)
    webhook_url = WEBHOOK_URL + TOKEN
    bot.set_webhook(webhook_url)
    app.run(host="0.0.0.0", port=port)
