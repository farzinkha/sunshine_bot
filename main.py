import os
from datetime import date
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ─── تاریخ شروع ───────────────────────────────────────────────────────────────
WORLD_START = date(2025, 11, 5)

def days_since_start() -> int:
    return (date.today() - WORLD_START).days

# ─── کلمات کلیدی شمارش ───────────────────────────────────────────────────────
KEYWORDS = [
    "چند", "چقدر", "چه قدر", "چه‌قدر", "چه مقدار", "چه‌مقدار",
    "چه تعداد", "چه‌تعداد", "چندتا", "چند تا",
    "چند روز", "چند هفته", "چند ماه", "چند سال",
    "چندین", "چه میزان",
    "گذشته", "گذشت", "شده", "میشه", "می‌شه",
    "طول کشیده", "سپری شده", "سپری شد",
    "از روزی که", "از وقتی که", "از زمانی که",
    "از اون روز", "از اون وقت", "از اون موقع",
    "فرزین", "رامیا", "خورشید", "آره" , "اره" , "بله" , "بگو" , "کی" , "when" ,
]

def is_day_question(text: str) -> bool:
    return any(kw in text for kw in KEYWORDS)

# ─── هندلر /start ─────────────────────────────────────────────────────────────
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "می‌خوای بدونی چند روزه این خورشید داره می‌تابه؟ ☀️"
    )

# ─── هندلر پیام‌ها ────────────────────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    if is_day_question(text):
        days = days_since_start()
        weeks = days // 7
        months = days // 30

        await update.message.reply_text(
            f"از روزی که خورشید فرزین و رامیا شروع به تابیدن کرد:\n"
            f"🗓 {days} روز\n"
            f"📅 {weeks} هفته\n"
            f"🌙 {months} ماه\n"
            f"گذشته! 🌞"
        )
    else:
        await update.message.reply_text(
            "فقط در مورد این که این خورشید چند روزه داره می‌تابه می‌تونم جواب بدم!"
        )

# ─── اجرا ────────────────────────────────────────────────────────────────────
def main():
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم نشده!")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
