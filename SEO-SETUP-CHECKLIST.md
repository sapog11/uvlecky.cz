# 🚀 SEO Setup Checklist - Poliklinika U Vlečky

## ✅ Уже выполнено (On-site SEO)

### Meta Tags & Headers
- [x] Title tags с русскими ключевыми словами
- [x] Meta descriptions на 4 языках
- [x] Keywords оптимизация для русской версии
- [x] Open Graph tags (og:title, og:description, og:image, og:url)
- [x] Twitter Card tags
- [x] Robots meta tags (index, follow, max-snippet)

### Structured Data
- [x] MedicalBusiness JSON-LD schema
- [x] LocalBusiness schema с geo-координатами
- [x] Person schema для врачей
- [x] OfferCatalog для услуг
- [x] AggregateRating schema
- [x] OpeningHoursSpecification

### Technical SEO
- [x] Sitemap.xml создан (с изображениями и приоритетами)
- [x] Robots.txt создан (с Sitemap ссылкой)
- [x] Canonical tags добавлены
- [x] hreflang tags для 4 языков
- [x] Image alt texts оптимизированы
- [x] Firebase cache headers правильно настроены

### Content
- [x] Русские переводы во всех секциях (77 элементов)
- [x] Ключевые слова интегрированы в контент
- [x] Заголовки (H1, H2, H3) правильно структурированы
- [x] Мобильная оптимизация завершена
- [x] Google Analytics 4 установлена

---

## ⚠️ Требует выполнения вручную (Off-site SEO)

### 1️⃣ Google Search Console Setup (PRIORITY!)
```
URL: https://search.google.com/search-console
Steps:
1. Нажмите "Start Now"
2. Добавьте property: https://uvlecky-f9d20.web.app
3. Выберите DNS verification method или HTML file method
4. Verify ownership
5. Submit sitemap: https://uvlecky-f9d20.web.app/sitemap.xml
6. Go to Coverage tab and monitor indexing
```

**Why:** Google не будет индексировать ваш сайт без подтверждения собственности в Search Console

### 2️⃣ Google My Business Setup
```
URL: https://business.google.com
Steps:
1. Создайте аккаунт (используйте Gmail email clinic'а)
2. Добавьте Business Type: Medical Office / Health Services
3. Заполните:
   - Business Name: Poliklinika U Vlečky
   - Category: Medical office, Clinic
   - Address: U Vlečky 3086/6, 400 01 Ústí nad Labem – Předlice
   - Phone: +420 606 755 784
   - Website: https://uvlecky-f9d20.web.app
   - Hours: Po 8-18, Út-Pá 8-14
4. Add photos (clinic photos)
5. Add services (лечение зубов, консультация врача, анализы крови)
6. Enable messaging/booking
```

**Why:** Для лучшей видимости в Google Maps и локальном поиске

### 3️⃣ Yandex Search Console Setup (Russian Users!)
```
URL: https://webmaster.yandex.ru/
Steps:
1. Создайте аккаунт Яндекса
2. Добавьте сайт: https://uvlecky-f9d20.web.app
3. Verify через HTML файл или DNS
4. Добавьте sitemap.xml
5. Установите Yandex Metrica для аналитики
```

**Why:** В России и странах СНГ Яндекс - второй по величине поисковик

### 4️⃣ Yandex Metrica Setup (Analytics for Russian Users)
```
URL: https://metrica.yandex.ru/
Steps:
1. Создайте account
2. Add counter code to website
3. Track: Russian user behavior, conversion rates, landing pages
```

### 5️⃣ Local Business Directories Submission
**Czech Directories:**
- [ ] Mapy.cz (Czech Google Maps equivalent)
- [ ] Firmy.cz (Business directory)
- [ ] Kurzy.cz (Medical services directory)
- [ ] Zdravotnicke-sluzby.cz

**Russian Directories:**
- [ ] Yandex.Карты (Yandex Maps - Russian search engine maps)
- [ ] 2GIS (Russian/CIS business directory)
- [ ] Avvo.com (For medical professionals)
- [ ] ZoomInfo (International business info)

**International:**
- [ ] Google My Business (already planned)
- [ ] Bing Places
- [ ] TripAdvisor (for medical reviews)

### 6️⃣ Backlink Building (Quality Over Quantity)
**Target websites for backlinks:**
- Czech medical directories and associations
- Regional business directories
- Medical review sites (Czech & Russian)
- Local news sites
- Business networking sites

**Strategy:**
- [ ] Contact Czech medical associations for directory listing
- [ ] Reach out to local news for clinic feature
- [ ] Join Russian expat community websites
- [ ] Get mentioned in local business guides

### 7️⃣ Review Generation (Critical for Local SEO)
```
Steps to encourage reviews:
1. Add QR code to clinic flyer directing to Google Reviews
2. Include review request in appointment confirmations
3. Email follow-up to patients asking for review
4. Add review links to website footer
5. Train staff to ask for online reviews
```

**Target:** 20-30 positive reviews minimum for authority

### 8️⃣ Social Media Optimization
- [ ] Facebook page setup (multi-language posts)
- [ ] Instagram setup (clinic photos/before-after)
- [ ] LinkedIn (professional content for doctors)
- [ ] Add social media links to website

### 9️⃣ Schema.org Review Implementation
Once reviews accumulated (5+ reviews):
```
Add to JSON-LD schema:
{
  "@type": "Review",
  "reviewRating": {"@type": "Rating", "ratingValue": "5"},
  "reviewBody": "Excellent clinic with professional staff",
  "author": {"@type": "Person", "name": "Patient Name"},
  "datePublished": "2026-07-15"
}
```

### 🔟 Content Expansion (Ongoing)
- [ ] Add FAQ section with schema.org
- [ ] Create blog posts about medical topics (Czech & Russian)
- [ ] Add case studies / success stories
- [ ] Create video content (doctor introductions)
- [ ] Add "Meet the Team" blog posts

---

## 📊 Monitoring & Maintenance

### Weekly Tasks
- [ ] Check Google Search Console for errors
- [ ] Monitor Core Web Vitals
- [ ] Check indexing status

### Monthly Tasks
- [ ] Review search queries in GSC
- [ ] Analyze organic traffic in Analytics 4
- [ ] Check competitor rankings
- [ ] Review backlink profile
- [ ] Update content if needed

### Quarterly Tasks (Every 3 months)
- [ ] Full SEO audit
- [ ] Content gap analysis
- [ ] Keyword ranking review
- [ ] Update SEO documentation

---

## 🎯 Expected Timeline

**Week 1-2:** GSC & Yandex Setup + GMB listing (HIGH IMPACT)
**Week 3-4:** Directory submissions (MEDIUM IMPACT)
**Month 2-3:** Review generation campaign (MEDIUM IMPACT)
**Month 3+:** Content expansion & backlink building (ONGOING)

---

## 📈 Success Metrics to Track

**In Google Search Console:**
```
Target (Month 6):
- Impressions: 5,000+
- Clicks: 500+
- CTR: 10%+
- Position: 1-50 for target keywords
```

**In Google Analytics 4:**
```
Target (Month 6):
- Organic Sessions: 1,000+/month
- Organic Conversion Rate: 5%+
- Average Session Duration: 2+ minutes
- Pages/Session: 3+
```

**Business Metrics:**
```
Target (Month 6):
- New patient inquiries from organic: 50+/month
- New patient conversions: 10-20/month
- Phone calls: 100+/month
```

---

## 🔐 Security & Performance Checklist

- [x] HTTPS enabled (Firebase)
- [x] Mobile responsive design
- [x] Fast page load times (optimized assets)
- [ ] Page speed optimization (run PageSpeed Insights)
- [ ] Image WebP compression (future optimization)

---

## 📧 Action Items Summary

**IMMEDIATE (This week):**
1. ✅ Review this SEO checklist
2. ⏳ Setup Google Search Console - Verify ownership
3. ⏳ Setup Yandex Webmaster - Verify ownership
4. ⏳ Create Google My Business listing

**SHORT TERM (This month):**
5. ⏳ Submit sitemap.xml to GSC and Yandex
6. ⏳ Configure Yandex Metrica analytics
7. ⏳ Add clinic to 5+ Czech business directories
8. ⏳ Add clinic to 5+ Russian business directories
9. ⏳ Request doctor profiles in medical directories

**MEDIUM TERM (This quarter):**
10. ⏳ Generate 20+ patient reviews
11. ⏳ Build 10+ quality backlinks
12. ⏳ Create 5+ blog posts with medical content
13. ⏳ Setup social media presence

---

## 💡 Pro Tips for Russian SEO

1. **Яндекс очень важен** - 40% of Russian internet traffic goes through Yandex
2. **Кирилица в URL** - Яндекс лучше ранжирует русскоязычные URL (не обязательно, но помогает)
3. **Локальные ключевые слова** - "врач рядом со мной" более важны чем "врач в Чехии"
4. **Социальные сигналы** - В Яндексе социальные ссылки важнее чем в Google
5. **Мобильный трафик** - 70%+ трафика из мобильных устройств

---

## ❓ FAQ

**Q: How long until we rank?**
A: Initial indexing: 2-4 weeks. First page rankings: 3-6 months. Depends on competition.

**Q: Is English SEO needed?**
A: Yes, but lower priority (3% traffic). Focus on Russian (80%) and Czech (15%) first.

**Q: Do we need backlinks?**
A: Yes, quality backlinks improve authority. Target 10-20 per year from relevant sites.

**Q: Should we do paid ads (PPC)?**
A: Can complement organic strategy for immediate visibility while waiting for organic rankings.

---

**Last Updated:** August 1, 2026
**Responsible:** Clinic Management Team
**Next Review:** September 1, 2026
