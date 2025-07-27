import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# جلب التوكن من Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔥 تم تنفيذ /start")
    keyboard = [[InlineKeyboardButton("تشغيل أغنية 🎵", callback_data="play_music")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔥 اهلا بيك! دوس على الزرار لتشغيل الأغاني.", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "play_music":
        await query.edit_message_text("🎤 ابعت اسم الأغنية اللي عايزها:")

async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song_name = update.message.text
    print(f"🔍 البحث عن الأغنية: {song_name}")
    await update.message.reply_text(f"🔎 جاري البحث عن: {song_name}")

    try:
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'song.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=True)
            file_name = ydl.prepare_filename(info['entries'][0])
        
        await update.message.reply_audio(audio=open(file_name, 'rb'))
        os.remove(file_name)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        await update.message.reply_text("😢 حصل خطأ في تشغيل الأغنية")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN غير موجود في Environment Variables")
        return

    print("✅ بدء تشغيل البوت...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, play_music))
    app.add_handler(MessageHandler(filters.COMMAND, start))
    app.add_handler(MessageHandler(filters.Regex('تشغيل أغنية 🎵'), play_music))

    app.run_polling()

if __name__ == "__main__":
    main()
