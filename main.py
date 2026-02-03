import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- AYARLAR ---
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Kontrol edilecek ürünlerin listesi
URLS_TO_CHECK = [
    {"store": "zara", "url": "https://www.zara.com/tr/tr/yun-karisimli-kazak-p05755352.html?v1=484669241"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/yunlu-monty-harry-lambert-for-zara-x-disney-kazak-p05755376.html?v1=459127737"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/straight-fit-rahat-pantolon-p03046213.html?v1=484867453"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/yun-straight-fit-pantolon-p06807814.html?v1=485225817"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/jakarli-cizgili-t-shirt-p04087380.html?v1=465255237"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/relaxed-fit-limited-edition-jean-p03991391.html?v1=464614591"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/basic-fermuarli-yaka-sweatshirt-p00761311.html?v1=458120097"},
    {"store": "zara", "url": "https://www.zara.com/tr/tr/cizgili-jakarli-gomlek---limited-edition-p06402151.html?v1=477849840"} 
]

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
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        # LİSTEDEKİ HER BİR ÜRÜN İÇİN DÖNGÜ
        for item in URLS_TO_CHECK:
            url = item["url"]
            print(f"\nKontrol ediliyor: {url}")
            
            try:
                driver.get(url)
                time.sleep(3) # Sayfanın yüklenmesi için kısa bekleme

                # Stok Kontrolü (Sepete Ekle butonu var mı?)
                try:
                    add_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa-action='add-to-cart']")
                    print(">> STOK BULUNDU! 🚨")
                    send_telegram_message(f"🚨 STOK GELDİ! KOŞ: {url}")
                except:
                    print(">> Stok yok.")
                
            except Exception as e:
                print(f"Bu linkte hata oluştu: {e}")
                continue # Bir link hata verirse diğerine geç

    except Exception as e:
        print(f"Genel Tarayıcı Hatası: {e}")
    finally:
        if driver:
            driver.quit()
            print("Tarayıcı kapatıldı.")

if __name__ == "__main__":
    check_stock()
