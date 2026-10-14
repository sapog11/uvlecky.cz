# -*- coding: utf-8 -*-
"""
Oznami vyhledavacum pres IndexNow, ze se stranky zmenily.

Podporuji: Seznam.cz, Yandex, Bing (a dalsi partneri IndexNow).
Google IndexNow NEpodporuje - tam zustava jen Search Console.

Klic je v souboru .indexnow-key a musi byt zaroven verejne dostupny
na https://uvlecky.cz/<klic>.txt (lezi v public/, deployuje se s webem).

Spusteni po deployi:  python indexnow-ping.py
"""

import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
HOST = "uvlecky.cz"

def sitemap_urls():
    """Vsechny adresy z public/sitemap.xml (+ samotny sitemap), aby ping
    vzdy odpovidal aktualnimu webu."""
    path = os.path.join(ROOT, "public", "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        urls = re.findall(r"<loc>([^<]+)</loc>", f.read())
    return urls + ["https://%s/sitemap.xml" % HOST]


URLS = sitemap_urls()

ENDPOINTS = [
    ("IndexNow (vsichni partneri)", "https://api.indexnow.org/indexnow"),
    ("Seznam.cz",                   "https://search.seznam.cz/indexnow"),
    ("Bing",                        "https://www.bing.com/indexnow"),
    ("Yandex",                      "https://yandex.com/indexnow"),
]


def main():
    with open(os.path.join(ROOT, ".indexnow-key"), encoding="utf-8") as f:
        key = f.read().strip()

    payload = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": "https://%s/%s.txt" % (HOST, key),
        "urlList": URLS,
    }).encode("utf-8")

    for name, url in ENDPOINTS:
        req = urllib.request.Request(
            url, data=payload, method="POST",
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                code = r.status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = "chyba: %s" % e
        ok = code in (200, 202)
        print("  %-30s %s %s" % (name, code, "OK" if ok else "!!"))


if __name__ == "__main__":
    print("IndexNow ping pro %d URL..." % len(URLS))
    main()
