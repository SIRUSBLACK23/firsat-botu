import telebot
import requests
from bs4 import BeautifulSoup
import re

TOKEN = "8980542235:AAEEPXsfz3rxfbUBOMHL-cJxqyqNhHShrbQ"
KANAL_ID = "-1004352564448"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Fırsat Botu hazır! Bana herhangi bir Trendyol veya Hepsiburada linki at, başlığını ve görselini alıp kanala atayım.")

@bot.message_handler(func=lambda message: True)
def link_yakala(message):
    text = message.text
    url_match = re.search(r'(https?://[^\s]+)', text)
    
    if not url_match:
        bot.reply_to(message, "Lütfen geçerli bir ürün linki gönder.")
        return

    url = url_match.group(0)
    bot.reply_to(message, "Ürün inceleniyor, kanala hazırlanıyor...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Başlık ve görsel yakalama
        title = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")

        urun_adi = title["content"] if title else "Fırsat Ürünü"
        gorsel_url = image["content"] if image else None

        mesaj = f"🔥 **GÜNÜN FIRSATI**\n\n📌 {urun_adi}\n\n👉 **Satın Al:** {url}"

        if gorsel_url:
            bot.send_photo(KANAL_ID, gorsel_url, caption=mesaj, parse_mode="Markdown")
        else:
            bot.send_message(KANAL_ID, mesaj, parse_mode="Markdown")

        bot.reply_to(message, "✅ Fırsat başarıyla Dx kanalında paylaşıldı!")
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {str(e)}")

bot.infinity_polling()
