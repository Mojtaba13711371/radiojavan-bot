from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

TOKEN = "7514451714:AAH5Z1arcJEJ73jrnA5mN-NDyRVVMhN12ck"  # اینجا توکن رباتتو بذار

async def get_mp3_link(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    try:
        audio = driver.find_element(By.TAG_NAME, "audio")
        return audio.get_attribute("src")
    except:
        return None
    finally:
        driver.quit()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "radiojavan.com/song/" not in url:
        await update.message.reply_text("لینک معتبر ارسال کن! مثل:
https://play.radiojavan.com/song/abcd1234")
        return

    await update.message.reply_text("⏳ در حال دریافت لینک...")
    mp3 = await get_mp3_link(url)
    if mp3:
        await update.message.reply_text(f"✅ لینک پخش:
{mp3}")
    else:
        await update.message.reply_text("❌ نتونستم لینک رو پیدا کنم.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
