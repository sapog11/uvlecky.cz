# -*- coding: utf-8 -*-
"""
Generuje všechny stránky webu ve čtyřech jazycích.

Zdroje:
  src/index.html          hlavní stránka (celá, se šablonou webu)
  src/pages/<slug>.html   vnitřní stránky — jen obsah; hlavičku, patičku,
                          styly a skripty si vezmou z src/index.html

Překlady jsou v atributech data-lang-ru / data-lang-ua / data-lang-en.
Tento skript je "zapeče" přímo do HTML, aby je Googlebot viděl jako
skutečný text stránky (atributy se neindexují).

Prvky s data-only="tr" (témata pro cizince) jsou jen v překladech,
z české verze se vypustí; data-only="cs" naopak jen v české.

Výstup: public/index.html (cs), public/ru/, public/ua/, public/en/
        a pro každou vnitřní stránku public/<slug>/, public/ru/<slug>/ …

Spuštění po každé změně ve src/ (soubory v public/ needitovat, přepíší se):
    python build-langs.py
"""

import json
import os
from bs4 import BeautifulSoup

ROOT   = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, "public")
MASTER = os.path.join(ROOT, "src", "index.html")
PAGES  = os.path.join(ROOT, "src", "pages")
SITE   = "https://uvlecky.cz"

# kód v data-lang-* -> (adresář, hreflang, html lang)
LANGS = {
    "ru": ("ru", "ru", "ru"),
    "ua": ("ua", "uk", "uk"),
    "en": ("en", "en", "en"),
}

# titulek a popis hlavní stránky v překladech (česká verze je ve src/index.html)
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
HREFLANG_TO_DIR = {"cs": "", "ru": "ru/", "uk": "ua/", "en": "en/"}


def page_paths():
    """Cesty všech stránek webu: "/" a "/<slug>/"."""
    out = ["/"]
    if os.path.isdir(PAGES):
        for name in sorted(os.listdir(PAGES)):
            if name.endswith(".html"):
                out.append("/%s/" % name[:-5])
    return out


def url(lang_dir, path):
    """"ru/" + "/odbery/" -> "/ru/odbery/"."""
    return "/" + lang_dir + path.lstrip("/")


def hreflang_block(soup, path):
    """Sada <link rel=alternate> na jazykové verze TÉTO stránky."""
    out = []
    for code, d in (("cs", ""), ("ru", "ru/"), ("uk", "ua/"), ("en", "en/"), ("x-default", "")):
        tag = soup.new_tag("link", rel="alternate", href=SITE + url(d, path))
        tag["hreflang"] = code
        out.append(tag)
    return out


def fix_head(soup, lang, path, title=None, desc=None):
    """Sjednotí hlavičku: title, description, canonical, hreflang, og."""
    canonical = SITE + url(LANGS[lang][0] + "/" if lang else "", path)
    if lang:
        soup.html["lang"] = LANGS[lang][2]
    if title and soup.title:
        soup.title.string = title
    if desc:
        d = soup.find("meta", attrs={"name": "description"})
        if d:
            d["content"] = desc

    can = soup.find("link", attrs={"rel": "canonical"})
    if can:
        can["href"] = canonical

    for old in soup.find_all("link", attrs={"rel": "alternate"}):
        old.decompose()
    anchor = soup.find("link", attrs={"rel": "canonical"})
    for tag in reversed(hreflang_block(soup, path)):
        anchor.insert_after(tag)

    og_url = soup.find("meta", attrs={"property": "og:url"})
    if og_url:
        og_url["content"] = canonical
    if title:
        og_t = soup.find("meta", attrs={"property": "og:title"})
        if og_t:
            og_t["content"] = title
    if desc:
        og_d = soup.find("meta", attrs={"property": "og:description"})
        if og_d:
            og_d["content"] = desc
    if lang and not soup.find("meta", attrs={"property": "og:locale"}):
        loc = soup.new_tag("meta")
        loc["property"] = "og:locale"
        loc["content"] = OG_LOCALE[lang]
        soup.find("meta", attrs={"property": "og:url"}).insert_after(loc)


def make_switcher_links(soup, lang, path):
    """Přepínač jazyků = skutečné odkazy na jazykové verze TÉTO stránky."""
    menu = soup.select_one(".lang-menu")
    if not menu:
        return
    current = {None: "cs", "ru": "ru", "ua": "uk", "en": "en"}[lang]
    for a in menu.find_all("a"):
        code = a.get("hreflang")
        if code not in HREFLANG_TO_DIR:
            continue
        a["href"] = url(HREFLANG_TO_DIR[code], path)
        if code == current:
            a["class"] = "active"
        elif a.has_attr("class"):
            del a["class"]
    cur = soup.find(id="langCur")
    if cur:
        cur.string = {"cs": "CS", "ru": "RU", "uk": "UA", "en": "EN"}[current]


def localize_links(soup, lang):
    """Odkazy mezi stránkami webu vedou v překladu na stejnou jazykovou verzi."""
    paths = page_paths()
    d = LANGS[lang][0] + "/"
    for a in soup.find_all(href=True):
        if a.find_parent(class_="lang-menu"):
            continue
        href = a["href"]
        base, _, frag = href.partition("#")
        if base in paths:
            a["href"] = url(d, base) + ("#" + frag if frag else "")


def apply_only(soup, keep):
    """Vypustí prvky určené jen pro druhou skupinu jazyků (data-only="cs"|"tr")."""
    removed = 0
    for el in soup.select("[data-only]"):
        if el.get("data-only") != keep:
            el.decompose()
            removed += 1
        else:
            del el["data-only"]
    return removed


def bake_translations(soup, lang):
    """Nahradí obsah prvků překladem z data-lang-<lang>; atributy (alt, aria-label,
    placeholder, title) se berou z data-lang-<lang>-<atribut>."""
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
    for name in ("alt", "aria-label", "placeholder", "title"):
        key = "%s-%s" % (attr, name)
        for el in soup.select("[%s]" % key):
            el[name] = el[key]
            count += 1
    return count


def inject_faq_schema(soup):
    """FAQPage JSON-LD sestavené přímo z přeložených <details class="faq-item">.

    Schéma tak vždy odpovídá viditelnému textu dané stránky a jazyka —
    Google nesoulad mezi schématem a obsahem penalizuje.
    Funkce je idempotentní (starý FAQPage blok nejdřív odstraní).
    """
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
    tag.string = json.dumps(data, ensure_ascii=False, indent=2)
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


def page_from_master(master_html, page_html):
    """Vnitřní stránka = šablona hlavní stránky bez jejího obsahu + obsah stránky.

    Zdroj stránky obsahuje:
      <script type="application/json" id="page-meta"> {title:{cs..}, description:{cs..}}
      <style id="page-style">          přidá se do <head>
      <div id="page-main">             obsah, vloží se do <main> před patičku
      <script id="page-script">        přidá se na konec <body>
    """
    soup = BeautifulSoup(master_html, "html.parser")
    page = BeautifulSoup(page_html, "html.parser")
    meta = json.loads(page.find(id="page-meta").string)

    hero = soup.select_one("section.hero-pin")
    if hero:
        hero.decompose()
    main = soup.select_one("main.page")
    footer = main.select_one("footer.site-footer")
    for child in list(main.children):
        if child is not footer:
            child.extract()
    content = page.find(id="page-main")
    for child in list(content.children):
        footer.insert_before(child)

    style = page.find(id="page-style")
    if style:
        del style["id"]
        soup.head.append(style)
    script = page.find(id="page-script")
    if script:
        del script["id"]
        soup.body.append(script)

    # navigace v hlavičce míří na sekce hlavní stránky
    for a in soup.select("header.site-header a[href^='#']"):
        a["href"] = "/" + a["href"] if a["href"] != "#top" else "/"

    return soup, meta


def write(soup, lang, path):
    rel = (LANGS[lang][0] + "/" if lang else "") + path.lstrip("/")
    outdir = os.path.join(PUBLIC, rel)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(str(soup))


def finish(soup, lang, path, title, desc):
    """Společný závěr pro každou stránku a jazyk. Vrací (počet překladů, FAQ)."""
    if lang:
        apply_only(soup, "tr")
        n = bake_translations(soup, lang)
        localize_links(soup, lang)
    else:
        n = apply_only(soup, "cs")
    fix_head(soup, lang, path, title, desc)
    make_switcher_links(soup, lang, path)
    tag_schema_entity(soup)
    faq = inject_faq_schema(soup)
    write(soup, lang, path)
    return n, faq


if __name__ == "__main__":
    print("Generuji stranky...")
    with open(MASTER, encoding="utf-8") as f:
        master_html = f.read()

    for lang in LANGS:
        n, faq = finish(BeautifulSoup(master_html, "html.parser"), lang, "/",
                        TITLES[lang], DESCRIPTIONS[lang])
        print("  /%s/  -> %d prvku prelozeno, FAQ %d otazek" % (LANGS[lang][0], n, faq))
    n, faq = finish(BeautifulSoup(master_html, "html.parser"), None, "/", None, None)
    print("  /      -> cestina, vypusteno %d prvku pro cizince, FAQ %d otazek" % (n, faq))

    for path in page_paths()[1:]:
        with open(os.path.join(PAGES, path.strip("/") + ".html"), encoding="utf-8") as f:
            page_html = f.read()
        for lang in [None] + list(LANGS):
            soup, meta = page_from_master(master_html, page_html)
            key = lang or "cs"
            n, faq = finish(soup, lang, path, meta["title"][key], meta["description"][key])
            print("  %-22s %s: %d, FAQ %d" % (path, key, n, faq))
    print("Hotovo.")
