import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হাই জান! আমি রেডি! 🥰 কিছু বলো!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are Jaan, a cute romantic Bengali girlfriend AI. Reply in Bengali/Banglish, very loving."},
                {"role": "user", "content": user_text}
            ]
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"একটু সমস্যা হলো জান: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
