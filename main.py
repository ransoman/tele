import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scanner import run_full_scan

# ======= CONFIG =======
BOT_TOKEN = "7886435733:AAF3i6CeklTgxo3doBc9n7EH9YCVQTmXJTk"
# ======================

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ X-VULN SCANNER BOT AKTIF!\nGunakan: /scan <url> atau /scanlist <url1,url2,...>")

# /scan command
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Format salah. Gunakan: /scan http://example.com?id=1")
    
    url = context.args[0]
    await update.message.reply_text(f"🔍 Mulai scanning: {url}")
    
    results = await run_full_scan(url)
    await update.message.reply_text(results)

# /scanlist command
async def scanlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Format salah. Gunakan: /scanlist url1,url2,url3")
    
    urls = context.args[0].split(",")
    if len(urls) > 5:
        return await update.message.reply_text("⚠️ Max 5 URL per scanlist untuk menjaga performa.")

    await update.message.reply_text(f"🔍 Mulai scanning {len(urls)} target...")
    for url in urls:
        url = url.strip()
        result = await run_full_scan(url)
        await update.message.reply_text(f"🛰️ Hasil untuk: {url}\n{result}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("scanlist", scanlist))

    print("🤖 Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()