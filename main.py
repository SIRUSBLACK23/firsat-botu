import telebot
import requests
from bs4 import BeautifulSoup
import re

TOKEN = "8980542235:AAEEPXsfz3rxfbUBOMHL-cJxqyqNhHShrbQ"
KANAL_ID = "-1004352564448"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Fırsat Botu hazır! Trendyol veya Hepsiburada linki at, görseli ve başlığıyla kanala paylaşayım.")

@bot.message_handler(func=lambda message: True)
def link_yakala(message):
    text = message.text
    url_match = re.search(r'(https?://[^\s]+)', text)
    
    if not url_match:
        bot.reply_to(message, "Lütfen geçerli bir ürün linki gönder.")
        return

    raw_url = url_match.group(0)
    bot.reply_to(message, "Ürün inceleniyor, kanala hazırlanıyor...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        session = requests.Session()
        res = session.get(raw_url, headers=headers, allow_redirects=True, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Başlık ve görsel çekme
        title = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")

        urun_adi = title["content"] if title else "Günün İndirim Fırsatı"
        
        # Site isimlerini başlıktan temizle
        urun_adi = re.sub(
            r'(\s*-\s*Trendyol|\s*-\s*Hepsiburada|\s*Fiyatı.*)$',
            '',
            urun_adi,
            flags=re.IGNORECASE
        ).strip()

        gorsel_url = image["content"] if image else None

        # Mesaj şablonu
        mesaj = (
            f"🔥 **GÜNÜN FIRSATI**\n\n"
            f"📌 **Ürün:** {urun_adi}\n\n"
            f"🛒 **Hemen İncele / Satın Al:**\n👉 {raw_url}"
        )

        if gorsel_url:
            bot.send_photo(KANAL_ID, gorsel_url, caption=mesaj, parse_mode="Markdown")
        else:
            bot.send_message(KANAL_ID, mesaj, parse_mode="Markdown")

        bot.reply_to(message, "✅ Fırsat kanala başarıyla gönderildi!")
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {str(e)}")

bot.infinity_polling()
