import requests
import base64

def collect_configs():
    # منابع جدید و تست شده
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/reality",
        "https://raw.githubusercontent.com/IranianBackbox/V2ray-Configs/main/All_Configs_Sub.txt",
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
    ]
    
    configs_list = []
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                content = response.text.strip()
                # بررسی اینکه آیا محتوا Base64 است یا خیر
                try:
                    decoded = base64.b64decode(content).decode('utf-8')
                    configs_list.extend(decoded.splitlines())
                except:
                    configs_list.extend(content.splitlines())
        except:
            continue

    # فیلتر کردن فقط کانفیگ‌های معتبر (vless, vmess, trojan)
    valid_protocols = ('vless://', 'vmess://', 'trojan://', 'ss://')
    unique_configs = list(set([c for c in configs_list if c.startswith(valid_protocols)]))
    
    # اگر لیستی پیدا شد، ذخیره کن
    if unique_configs:
        final_text = "\n".join(unique_configs)
        encoded_base64 = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
        with open('best_reality_configs.txt', 'w') as f:
            f.write(encoded_base64)
        print(f"Done! Found {len(unique_configs)} configs.")
    else:
        # اگر چیزی پیدا نشد، یک متن ساده بنویس که فایل کاملاً سفید نباشه
        with open('best_reality_configs.txt', 'w') as f:
            f.write("No configs found yet. Please wait for next update.")
        print("No configs found.")

if __name__ == "__main__":
    collect_configs()
