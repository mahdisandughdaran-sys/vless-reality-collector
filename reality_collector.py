import requests
import base64

def collect_configs():
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
                try:
                    decoded = base64.b64decode(content).decode('utf-8')
                    configs_list.extend(decoded.splitlines())
                except:
                    configs_list.extend(content.splitlines())
        except:
            continue

    # ۱. حذف تکراری‌ها
    unique_configs = list(set([c for c in configs_list if c.startswith(('vless://', 'vmess://', 'trojan://'))]))
    
    # ۲. گلچین کردن (اولویت با VLESS و Reality)
    # ابتدا کانفیگ‌هایی که کلمه reality یا sni دارن رو جدا می‌کنیم چون باکیفیت‌ترن
    top_configs = [c for c in unique_configs if "reality" in c.lower() or "sni" in c.lower()]
    
    # اگر تعداد ریالیتی‌ها کم بود، از بقیه اضافه کن
    if len(top_configs) < 10:
        remaining = [c for c in unique_configs if c not in top_configs]
        top_configs.extend(remaining[:(10 - len(top_configs))])
    
    # ۳. نهایی کردن لیست (فقط ۱۰ مورد اول)
    final_list = top_configs[:10]
    
    if final_list:
        final_text = "\n".join(final_list)
        encoded_base64 = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
        with open('best_reality_configs.txt', 'w') as f:
            f.write(encoded_base64)
        print(f"Success! 10 best configs saved.")
    else:
        with open('best_reality_configs.txt', 'w') as f:
            f.write("No configs found.")
        print("No configs found.")

if __name__ == "__main__":
    collect_configs()
