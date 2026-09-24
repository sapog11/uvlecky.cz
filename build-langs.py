# -*- coding: utf-8 -*-
"""
Generuje jazykové mutace webu z českého originálu public/index.html.

Překlady jsou v atributech data-lang-ru / data-lang-ua / data-lang-en.
Tento skript je "zapeče" přímo do HTML, aby je Googlebot viděl jako
skutečný text stránky (atributy se neindexují).

Výstup: public/ru/index.html, public/ua/index.html, public/en/index.html

Spuštění po každé změně public/index.html:
    python build-langs.py
"""

import os
import re
import shutil
from bs4 import BeautifulSoup

ROOT   = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, "public")
MASTER = os.path.join(PUBLIC, "index.html")
SITE   = "https://uvlecky.cz"

# kód v data-lang-* -> (adresář, hreflang, html lang)
LANGS = {
    "ru": ("ru", "ru", "ru"),
    "ua": ("ua", "uk", "uk"),
    "en": ("en", "en", "en"),
}

TITLES = {
    "ru": "Русскоговорящий терапевт Ústí nad Labem и Устецкий край | U Vlečky",
    "ua": "Терапевт Ústí nad Labem — україномовний сімейний лікар | U Vlečky",
    "en": "English-speaking doctor in Ústí nad Labem – PVZP and VZP accepted",
}

DESCRIPTIONS = {
    "ru": ("Русскоговорящий врач-терапевт регистрирует новых пациентов из "
           "Ústí nad Labem, Děčín, Litoměřice и всего Устецкого края. "
           "Принимаем VZP и PVZP для иностранцев. U Vlečky 3086/6. +420 606 755 784"),
    "ua": ("Україномовний сімейний лікар-терапевт реєструє нових пацієнтів з "
           "Ústí nad Labem, Děčín, Litoměřice та всього Устецького краю. "
           "Приймаємо VZP і PVZP для іноземців. U Vlečky 3086/6. +420 606 755 784"),
    "en": ("English-speaking general practitioner in Ústí nad Labem accepting new "
           "patients. We take VZP and PVZP insurance for foreigners. Russian and "
           "Ukrainian spoken too. U Vlečky 3086/6. +420 606 755 784"),
}

OG_LOCALE = {"ru": "ru_RU", "ua": "uk_UA", "en": "en_GB"}

# jazykový přepínač: kód tlačítka -> URL
SWITCH_URLS = {"CS": "/", "RU": "/ru/", "UA": "/ua/", "EN": "/en/"}


def hreflang_block(soup):
    """Vrátí sadu <link rel=alternate> mířících na SKUTEČNĚ různé adresy."""
    out = []
    for code, href in (("cs", SITE + "/"), ("ru", SITE + "/ru/"),
                       ("uk", SITE + "/ua/"), ("en", SITE + "/en/"),
                       ("x-default", SITE + "/")):
        tag = soup.new_tag("link", rel="alternate", href=href)
        tag["hreflang"] = code
        out.append(tag)
    return out


def fix_head(soup, lang, canonical):
    """Sjednotí hlavičku: title, description, canonical, hreflang, og."""
    if lang:
        soup.html["lang"] = LANGS[lang][2]

    if lang:
        if soup.title:
            soup.title.string = TITLES[lang]
        desc = soup.find("meta", attrs={"name": "description"})
        if desc:
            desc["content"] = DESCRIPTIONS[lang]

    can = soup.find("link", attrs={"rel": "canonical"})
    if can:
        can["href"] = canonical

    # hreflang přepsat kompletně (původní mířily všechny na jednu adresu)
    for old in soup.find_all("link", attrs={"rel": "alternate"}):
        old.decompose()
    anchor = soup.find("link", attrs={"rel": "canonical"})
    for tag in reversed(hreflang_block(soup)):
        anchor.insert_after(tag)

    og_url = soup.find("meta", attrs={"property": "og:url"})
    if og_url:
        og_url["content"] = canonical
    if lang:
        og_t = soup.find("meta", attrs={"property": "og:title"})
        if og_t:
            og_t["content"] = TITLES[lang]
        og_d = soup.find("meta", attrs={"property": "og:description"})
        if og_d:
            og_d["content"] = DESCRIPTIONS[lang]
        if not soup.find("meta", attrs={"property": "og:locale"}):
            loc = soup.new_tag("meta")
            loc["property"] = "og:locale"
            loc["content"] = OG_LOCALE[lang]
            soup.find("meta", attrs={"property": "og:url"}).insert_after(loc)


HREF_TO_CODE = {v: k for k, v in SWITCH_URLS.items()}


def make_switcher_links(soup, current):
    """Přepínač jazyků = skutečné odkazy, aby je Google prošel a objevil mutace.

    Funkce je idempotentní - zvládne jak původní <button>, tak už převedené <a>.
    """
    menu = soup.select_one(".lang-menu")
    if not menu:
        return

    for btn in menu.find_all("button"):
        code = btn.get("data-lang")
        if not code:
            continue
        a = soup.new_tag("a", href=SWITCH_URLS[code])
        a["role"] = "menuitem"
        a["hreflang"] = {"CS": "cs", "RU": "ru", "UA": "uk", "EN": "en"}[code]
        a.string = btn.get_text()
        btn.replace_with(a)

    # aktivní jazyk nastavit až nakonec, ať je jen jeden
    for a in menu.find_all("a"):
        code = HREF_TO_CODE.get(a.get("href"))
        if code == current:
            a["class"] = "active"
        elif a.has_attr("class"):
            del a["class"]

    cur = soup.find(id="langCur")
    if cur:
        cur.string = current


def bake_translations(soup, lang):
    """Nahradí obsah prvků překladem z data-lang-<lang>."""
    attr = "data-lang-" + lang
    count = 0
    for el in soup.select("[%s]" % attr):
        val = el.get(attr)
        if not val:
            continue
        frag = BeautifulSoup(val, "html.parser")
        el.clear()
        for child in list(frag.contents):
            el.append(child)
        count += 1
    return count


def inject_faq_schema(soup):
    """FAQPage JSON-LD sestavene primo z prelozenych <details class="faq-item">.

    Schema tak vzdy odpovida viditelnemu textu dane jazykove mutace -
    Google nesoulad mezi schematem a obsahem penalizuje.
    Funkce je idempotentni (stary FAQPage blok nejdriv odstrani).
    """
    import json as _json

    for old in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if old.string and '"FAQPage"' in old.string:
            old.decompose()

    items = []
    for d in soup.select("details.faq-item"):
        s = d.find("summary")
        p = d.find("p")
        if not (s and p):
            continue
        items.append({
            "@type": "Question",
            "name": s.get_text(" ", strip=True),
            "acceptedAnswer": {"@type": "Answer", "text": p.get_text(" ", strip=True)},
        })
    if not items:
        return 0

    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    tag = soup.new_tag("script", type="application/ld+json")
    tag.string = _json.dumps(data, ensure_ascii=False, indent=2)
    # vlozit za posledni existujici JSON-LD, at jsou schemata pohromade
    anchors = soup.find_all("script", attrs={"type": "application/ld+json"})
    if anchors:
        anchors[-1].insert_after(tag)
    else:
        soup.head.append(tag)
    return len(items)


def tag_schema_entity(soup):
    """Přidá @id, aby Google chápal všechny mutace jako JEDEN podnik, ne čtyři."""
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        txt = script.string or ""
        if '"@type": "MedicalBusiness"' in txt and '"@id"' not in txt:
            txt = txt.replace('"@type": "MedicalBusiness",',
                              '"@type": "MedicalBusiness",\n  "@id": "%s/#organization",' % SITE, 1)
        if '"@type": "LocalBusiness"' in txt and '"@id"' not in txt:
            txt = txt.replace('"@type": "LocalBusiness",',
                              '"@type": "LocalBusiness",\n  "@id": "%s/#localbusiness",' % SITE, 1)
        script.string = txt


def build(lang, master_html):
    soup = BeautifulSoup(master_html, "html.parser")

    subdir = LANGS[lang][0]
    canonical = "%s/%s/" % (SITE, subdir)

    n = bake_translations(soup, lang)
    fix_head(soup, lang, canonical)
    make_switcher_links(soup, {"ru": "RU", "ua": "UA", "en": "EN"}[lang])
    tag_schema_entity(soup)
    faq = inject_faq_schema(soup)

    outdir = os.path.join(PUBLIC, subdir)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("  /%s/  -> %d prvku prelozeno, FAQ %d otazek" % (subdir, n, faq))


def rebuild_master(master_html):
    """Český originál: opravit hreflang + přepínač na odkazy."""
    soup = BeautifulSoup(master_html, "html.parser")
    fix_head(soup, None, SITE + "/")
    make_switcher_links(soup, "CS")
    tag_schema_entity(soup)
    faq = inject_faq_schema(soup)
    with open(MASTER, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("  /      -> hreflang + prepinac aktualizovan, FAQ %d otazek" % faq)


if __name__ == "__main__":
    print("Generuji jazykove mutace...")
    # originál načíst JEDNOU, ať přestavba masteru neovlivní mutace
    with open(MASTER, encoding="utf-8") as f:
        master_html = f.read()
    for code in LANGS:
        build(code, master_html)
    rebuild_master(master_html)
    print("Hotovo.")
