# -*- coding: utf-8 -*-
"""
Generuje obrazky pro Google Business Profile.

  logo-google-720.png    720x720   (Google chce ctverec, min. 250x250)
  cover-google-1080.png  1080x608  (pomer 16:9, min. 480x270)

Vystup do slozky google-profile/ (mimo public/, aby se nedeployovalo na web).

Spusteni:  python make-google-assets.py
"""

import os
from PIL import Image, ImageDraw, ImageEnhance

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "google-profile")
BUILDING = os.path.join(ROOT, "public", "images", "building.jpg")

# firemni barvy (shodne s webem)
NAVY_TOP = (28, 43, 74)     # #1C2B4A
NAVY_BOT = (36, 54, 90)     # #24365A
GREEN = (111, 154, 133)     # #6F9A85
WHITE = (255, 255, 255)

SS = 4  # supersampling - kreslime 4x vetsi a zmensime, aby byly hrany hladke


def make_logo(size=720):
    """Tmave modry podklad + bily zdravotnicky kriz + zeleny prstenec.

    Google zobrazuje logo nekde jako ctverec, jinde orizle do kruhu.
    Podklad je proto pres celou plochu a prstenec kruhovy - funguje v obou
    pripadech.
    """
    S = size * SS

    # --- diagonalni gradient pozadi ---
    grad = Image.new("RGB", (2, 2))
    grad.putpixel((0, 0), NAVY_TOP)
    grad.putpixel((1, 0), NAVY_TOP)
    grad.putpixel((0, 1), NAVY_BOT)
    grad.putpixel((1, 1), NAVY_BOT)
    img = grad.resize((S, S), Image.BICUBIC)

    d = ImageDraw.Draw(img)

    # --- zeleny prstenec ---
    inset = int(S * 0.055)
    ring_w = max(1, int(S * 0.008))
    d.ellipse([inset, inset, S - inset, S - inset],
              outline=GREEN, width=ring_w)

    # --- bily kriz ---
    bar_thick = int(S * 0.208)     # tloustka ramene
    bar_len = int(S * 0.653)       # delka ramene
    r = int(S * 0.022)             # zaobleni rohu
    c0 = (S - bar_thick) // 2
    c1 = c0 + bar_thick
    l0 = (S - bar_len) // 2
    l1 = l0 + bar_len

    d.rounded_rectangle([c0, l0, c1, l1], radius=r, fill=WHITE)   # svisle
    d.rounded_rectangle([l0, c0, l1, c1], radius=r, fill=WHITE)   # vodorovne

    img = img.resize((size, size), Image.LANCZOS)
    path = os.path.join(OUT, "logo-google-720.png")
    img.save(path, "PNG", optimize=True)
    return path, img.size


def make_cover(width=1080, height=608):
    """Fotka budovy orezana na 16:9, s durazem na ceduli ZDRAVOTNI STREDISKO."""
    src = Image.open(BUILDING).convert("RGB")
    w, h = src.size
    target = width / height

    # orez na pozadovany pomer
    new_h = int(round(w / target))
    if new_h <= h:
        # ubirame vysku: vic zdola (trava), min shora (obloha),
        # aby budova i cedule zustaly v zaberu
        cut = h - new_h
        top = int(cut * 0.28)
        box = (0, top, w, top + new_h)
    else:
        # kdyby byl zdroj uzsi nez 16:9 - orizneme sirku na stred
        new_w = int(round(h * target))
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)

    img = src.crop(box).resize((width, height), Image.LANCZOS)

    # jemne doladeni - zadne drasticke filtry
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.15)

    path = os.path.join(OUT, "cover-google-1080x608.jpg")
    img.save(path, "JPEG", quality=92, optimize=True, progressive=True)
    return path, img.size, src.size, box


def make_og_image(width=1200, height=630):
    """Nahledovy obrazek pro socialni site (Facebook, LinkedIn, Telegram...).

    Poradi do public/, protoze na rozdil od podkladu pro Google profil
    musi byt verejne dostupny na webu.
    """
    src = Image.open(BUILDING).convert("RGB")
    w, h = src.size
    target = width / height

    new_h = int(round(w / target))
    if new_h <= h:
        cut = h - new_h
        top = int(cut * 0.28)   # vic ubrat zdola (trava) nez shora (obloha)
        box = (0, top, w, top + new_h)
    else:
        new_w = int(round(h * target))
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)

    img = src.crop(box).resize((width, height), Image.LANCZOS)
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.15)

    path = os.path.join(ROOT, "public", "og-image.jpg")
    img.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    return path, img.size


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)

    p, sz = make_logo()
    print("logo   %s  %dx%d  %.0f kB" % (os.path.basename(p), sz[0], sz[1],
                                         os.path.getsize(p) / 1024))

    p, sz, orig, box = make_cover()
    print("cover  %s  %dx%d  %.0f kB" % (os.path.basename(p), sz[0], sz[1],
                                         os.path.getsize(p) / 1024))
    print("       zdroj %dx%d, orez %s" % (orig[0], orig[1], str(box)))

    p, sz = make_og_image()
    print("og     %s  %dx%d  %.0f kB  (-> public/, pro socialni site)"
          % (os.path.basename(p), sz[0], sz[1], os.path.getsize(p) / 1024))

    print("\nHotovo -> %s" % OUT)
