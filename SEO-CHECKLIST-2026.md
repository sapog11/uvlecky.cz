# SEO Настройка для uvlecky.cz - 2026

## ✅ Выполнено

### Технические SEO
- [x] Meta tags оптимизированы для чешских поисков
- [x] Добавлены локальные ключевые слова: Ústí nad Labem, Chomutov, Litoměřice, Louny
- [x] JSON-LD MedicalBusiness и LocalBusiness структуры добавлены
- [x] Sitemap.xml создан и обновлен
- [x] robots.txt настроен
- [x] Canonical URL обновлен на uvlecky.cz
- [x] hreflang теги добавлены для языковых версий
- [x] OpenGraph мета теги добавлены

### Русскоязычное SEO
- [x] Ключевые слова для русских поисков добавлены
- [x] Описание на русском языке в JSON-LD
- [x] Альтернативные названия на русском и украинском

---

## 📋 Следующие шаги

### 1. Google Search Console (для Чешских поисков)

**Добавление домена:**
1. Перейти на https://search.google.com/search-console
2. Нажать "Добавить свойство"
3. Выбрать "Только URL-префикс"
4. Ввести: `https://uvlecky.cz`
5. Выбрать метод проверки:
   - **Рекомендуется:** HTML тег метаверификации
   - Добавить этот тег в `<head>` раздел (если нужно):
     ```html
     <meta name="google-site-verification" content="[КОД]" />
     ```

**После добавления:**
1. Перейти в "Карта сайта"
2. Отправить sitemap: `https://uvlecky.cz/sitemap.xml`
3. Отправить URL для индексирования:
   - https://uvlecky.cz
   - https://uvlecky.cz#sluzby
   - https://uvlecky.cz#lekar
   - https://uvlecky.cz#informace
   - https://uvlecky.cz#kontakt

**Ключевые слова для мониторинга (Czech):**
- "praktický lékař Ústí nad Labem"
- "terapeut Ústí"
- "lékař Ústí"
- "stomatolog Ústí"
- "zdravotní prohlídky Ústí"
- "laboratorní testy Ústí"

---

### 2. Yandex.Webmaster (для Русских поисков)

**Добавление сайта:**
1. Перейти на https://webmaster.yandex.ru/
2. Нажать "Добавить сайт"
3. Ввести: `https://uvlecky.cz`
4. Выбрать метод проверки:
   - HTML тег: Добавить `<meta name="yandex-verification" content="[КОД]" />`
   - Или загрузить файл проверки

**После добавления:**
1. Перейти в "Карта сайта"
2. Добавить: `https://uvlecky.cz/sitemap.xml`
3. Отправить индексирование URL

**Ключевые слова для мониторинга (Russian):**
- "терапевт в Усти"
- "врач в Усти над Лабем"
- "стоматолог Усти"
- "анализы крови Усти"
- "профессиональные осмотры Усти"
- "медкомиссия Усти"

---

### 3. Google My Business (для локального SEO)

**Настройка:**
1. Перейти на https://www.google.com/business
2. Нажать "Добавить свой бизнес"
3. Ввести название: "Poliklinika U Vlečky"
4. Выбрать адрес: U Vlečky 3086/6, 400 01 Ústí nad Labem, Чехия
5. Выбрать категорию: "Medical office" или "Medical clinic"
6. Добавить телефон: +420 606 755 784
7. Загрузить логотип: `/logo-512.svg` (экспортировать в PNG 512x512)
8. Добавить фото клиники (building.jpg, corridor.jpg, cabinet.jpg)
9. Добавить часы работы
10. Добавить услуги:
    - General practice
    - Dentistry
    - Laboratory testing
    - Occupational health exams
    - Gynecology (coming September 2026)

---

### 4. Локальные справочники (чешские)

**Добавить информацию на:**
1. Seznam.cz (чешский аналог Google)
2. Firmy.cz (справочник компаний)
3. MUDr.info (справочник врачей)
4. Doktory.cz (справочник медицинских услуг)
5. Toplevice.cz (локальные услуги)

**Информация для добавления:**
- Название: Poliklinika U Vlečky
- Адрес: U Vlečky 3086/6, 400 01 Ústí nad Labem – Předlice
- Телефон: +420 606 755 784
- Специальности: praktický lékař, stomatolog, laboratorní testy

---

### 5. Мониторинг SEO

**Инструменты для отслеживания:**

**Google Search Console:**
- Отчеты о производительности
- Ошибки индексирования
- Отправка URL для индексирования
- Панель мобильной удобства

**Yandex.Webmaster:**
- Статистика индексирования
- Качество сайта
- Мобильная версия

**Бесплатные инструменты для мониторинга:**
- https://www.ubersuggest.com (отслеживание позиций ключевых слов)
- https://www.seobility.net (анализ SEO)
- https://www.woorank.com (быстрый SEO аудит)

---

### 6. Регулярные действия (Monthly)

**Ежемесячно проверять:**
1. Google Search Console - новые ошибки индексирования
2. Позиции ключевых слов (через Ubersuggest или аналоги)
3. Трафик из поисковых систем (Google Analytics)
4. Рейтинг в Google My Business

**Обновлять контент:**
- Добавлять новые отзывы врачей
- Обновлять информацию о расписании
- Добавлять новых врачей по мере необходимости
- Обновлять JSON-LD структуры при изменениях

---

### 7. Добавление разметки для Structured Data

**Текущие структуры:**
- MedicalBusiness (основной тип)
- LocalBusiness (локальная информация)
- OpeningHoursSpecification (время работы)
- PostalAddress (адрес)
- Person (врачи)
- Organization (партнеры)

**Рекомендуемые дополнительные:**
- AggregateRating (отзывы врачей)
- Review (отзывы пациентов)
- BreadcrumbList (навигация)

---

## 📱 Проверка на мобильных устройствах

**Протестировать на:**
1. https://search.google.com/test/mobile-friendly
2. https://webmaster.yandex.ru/tools/mobile-usability/

---

## 🔍 Ожидаемые результаты

**После полной настройки (2-4 недели):**
- Появление в поисковых результатах Google для местных запросов
- Увеличение видимости в поисковой системе Yandex
- Оптимизация Google My Business для локальных поисков
- Улучшение CTR (click-through rate) через Rich Snippets

**Целевые ключевые слова для мониторинга:**

| Язык | Ключевое слово | Цель | Приоритет |
|------|---|---|---|
| Czech | praktický lékař Ústí nad Labem | Top 3 | High |
| Czech | terapeut Ústí | Top 5 | High |
| Czech | lékař Chomutov | Top 10 | Medium |
| Russian | терапевт в Усти | Top 10 | High |
| Russian | врач Усти над Лабем | Top 10 | High |
| Russian | анализы крови Усти | Top 20 | Medium |

---

## ⚠️ Важные замечания

1. **301 редирект с Firebase URL:**
   - Если Firebase URL был проинсексирован, добавить 301 редирект с uvlecky-f9d20.web.app на uvlecky.cz
   - Это передаст "authority" с Firebase на новый домен

2. **Обновление ссылок:**
   - Все внешние ссылки должны указывать на https://uvlecky.cz (не на Firebase URL)
   - Обновить ссылки в социальных сетях

3. **Мониторинг индексирования:**
   - Проверять Search Console каждую неделю первые 2 месяца
   - Убедиться что все страницы индексируются

4. **Локализация контента:**
   - Текущий контент на чешском оптимален
   - Русский контент рекомендуется как альтернативный (через data-lang атрибуты)

---

**Дата обновления:** 3 августа 2026  
**Автор:** Claude Code  
**Статус:** ✅ Готово к индексированию
