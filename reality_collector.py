import requests
import re
from urllib.parse import urlparse, parse_qs, unquote
from datetime import datetime

# منابع معتبر VLESS (به‌روزترین collectorها)
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/vless.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/iboxz/free-v2ray-collector/main/main/vless.txt",
    "https://raw.githubusercontent.com/lagzian/SS-Collector/main/reality.txt",  # مخصوص REALITY
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/vless"
]

def parse_vless(link):
    try:
        if not link.startswith("vless://"):
            return None
        
        # جدا کردن uuid@host:port?params#remark
        rest = link[8:]
        if '#' in rest:
            rest, remark = rest.split('#', 1)
            remark = unquote(remark)
        else:
            remark = "No remark"
        
        if '?' in rest:
            main, query = rest.split('?', 1)
        else:
            main, query = rest, ""
        
        if '@' in main:
            uuid, host_port = main.split('@', 1)
            if ':' in host_port:
                host, port = host_port.split(':', 1)
            else:
                host, port = host_port, "443"
        else:
            return None
        
        params = parse_qs(query)
        
        # همه مقادیر را lowercase برای مقایسه دقیق
        security = params.get('security', [''])[0].lower()
        flow = params.get('flow', [''])[0].lower()
        typ = params.get('type', ['tcp'])[0].lower()
        port = port.strip()
        
        # فیلتر دقیق REALITY + xtls-rprx-vision + پورت 443 + TCP
        if (security == 'reality'
            and flow == 'xtls-rprx-vision'
            and port == '443'
            and typ in ['', 'tcp']):
            return link.strip()
    except:
        pass
    return None

all_configs = []
seen = set()

print("🔍 در حال جمع‌آوری و فیلتر کانفیگ‌های VLESS+REALITY...")

for i, url in enumerate(SOURCES, 1):
    try:
        print(f"[{i}/{len(SOURCES)}] در حال بررسی: {url}")
        resp = requests.get(url, timeout=25)
        if resp.status_code == 200:
            count = 0
            for line in resp.text.splitlines():
                line = line.strip()
                if line and line.startswith("vless://") and line not in seen:
                    cfg = parse_vless(line)
                    if cfg:
                        all_configs.append(cfg)
                        seen.add(cfg)
                        count += 1
            print(f"   ✅ {count} کانفیگ معتبر پیدا شد")
        else:
            print(f"   ❌ خطا HTTP {resp.status_code}")
    except Exception as e:
        print(f"   ❌ خطا: {str(e)[:80]}...")

# محدود به 100 تا بهترین (جدیدترین/فعال)
all_configs = all_configs[:100]

# ذخیره با شماره‌گذاری
with open("best_reality_configs.txt", "w", encoding="utf-8") as f:
    f.write(f"# بهترین کانفیگ‌های VLESS + REALITY + xtls-rprx-vision\n")
    f.write(f"# جمع‌آوری‌شده در: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"# تعداد: {len(all_configs)} | پورت ۴۴۳ | TCP | بدون نیاز به روت\n")
    f.write(f"# مناسب برای: v2rayNG, Hiddify, FoXray, v2rayN\n\n")
    
    for i, cfg in enumerate(all_configs, 1):
        f.write(f"{i:2d}. {cfg}\n")

print(f"\n✅ تمام شد! {len(all_configs)} کانفیگ عالی در best_reality_configs.txt ذخیره شد!")
print("\n📋 برای استفاده:\n   1. فایل را باز کن\n   2. هر خط را کپی کن\n   3. در v2rayNG: + > Import config from clipboard")
