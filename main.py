import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# GitHub Secrets'tan bilgileri al
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
# Ürün linkini buraya sabit yazıyoruz veya secret olarak da alabilirsin
URUN_URL = "https://www.zara.com/tr/tr/yun-karisimli-kazak-p05755352.html?v1=484669241"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram hatası: {e}")

def check_stock():
    print("Tarayıcı başlatılıyor...")
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ekransız mod (Sunucu için şart)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(URUN_URL)
        time.sleep(5) 

        # Sepete Ekle butonu kontrolü
        try:
            add_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa-action='add-to-cart']")
            print(">> STOK BULUNDU!")
            send_telegram_message(f"🚨 STOK GELDİ! LİNK: {URUN_URL}")
        except:
            print(">> Stok yok (Sepete ekle butonu yok).")

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    check_stock()
