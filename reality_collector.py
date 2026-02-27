import requests
import base64
import os

def collect_configs():
    # لیست منابع (می‌توانی لینک‌های معتبر دیگر را اینجا اضافه کنی)
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/reality",
        "https://raw.githubusercontent.com/WilliamStar007/ClashX-V2Ray-Config/main/All.txt"
    ]
    
    configs_list = []
    
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                # اگر محتوا از قبل Base64 بود، آن را دیکود می‌کنیم
                try:
                    decoded_data = base64.b64decode(content).decode('utf-8')
                    configs_list.extend(decoded_data.splitlines())
                except:
                    configs_list.extend(content.splitlines())
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    # حذف تکراری‌ها و فیلتر کردن فقط پروتکل‌های مورد نظر (مثل vless)
    unique_configs = list(set([c for c in configs_list if c.startswith('vless://')]))
    
    # تبدیل نهایی به Base64 برای سازگاری کامل با v2rayNG
    final_text = "\n".join(unique_configs)
    encoded_base64 = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    # ذخیره در فایل
    with open('best_reality_configs.txt', 'w') as f:
        f.write(encoded_base64)
    
    print(f"Success! {len(unique_configs)} configs collected and encoded.")

if __name__ == "__main__":
    collect_configs()
