# 在博客根目录创建清除缓存脚本 clear_cache.py
import webbrowser
import time

urls = [
    "https://mieor.github.io",
    "https://mieor.github.io/?v=" + str(int(time.time())),
    "https://purge.jsdelivr.net/gh/mieor/mieor.github.io@gh-pages/",
]

for url in urls:
    print("访问:", url)
    webbrowser.open(url)
    time.sleep(2)