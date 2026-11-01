#!/usr/bin/env python3
"""Build one static landing page per confirmed Google Business Profile service city."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://orbedek.co.il"

# The twenty cities shown in the owner's service-area screenshot, 2026-10-30.
# Each editorial note is an actionable inspection scenario, not a claim about
# local housing stock, previous jobs, an office, or a team in that city.
CITIES = [
    ("אזור", "azor", "ביישוב אזור", "דירה לפני קנייה", "אם הנכס עומד לפני רכישה, בקשו מהמוכר מידע על תיקוני רטיבות ושינויים שבוצעו. השוו את התשובות למצב הגלוי בביקור, ודאגו שתהיה גישה לכל החדרים ולמרפסת אם ישנה. הדוח יעזור להפריד בין ממצא שדורש בירור נוסף לבין עבודת תחזוקה רגילה."),
    ("אלעד", "elad", "באלעד", "התאמת הבדיקה לגודל הדירה", "בדירה עם חדרים רבים או חלוקה פנימית מורכבת, מסרו מראש את מספר החדרים, המרפסות וחדרי הרחצה. כך אפשר להקצות זמן לבדיקת פתחים, גמרים, סימני רטיבות ומערכות נגישות בכל חלקי הנכס."),
    ("חולון", "holon", "בחולון", "בדיקה לפני חתימה על עסקה", "אם אתם שוקלים דירת יד שנייה, תיאום הבדיקה לפני התחייבות סופית מאפשר לכם להבין את מצב הנכס בזמן לקבלת החלטה. הביאו מידע על תיקונים ידועים ושאלו מראש על נגישות לארונות שירות, למרפסת ולנקודות מים."),
    ("בת ים", "bat-yam", "בבת ים", "בדיקה של מרפסת ופתחים", "בדירה עם מרפסת או פתחים רבים, ציינו זאת בעת התיאום. בביקור אפשר לבחון סימנים גלויים ליד מסגרות, שיפועים וניקוז במשטחים נגישים ואת מצב הגמרים. מקור של חדירת מים, אם מתגלה חשד, עשוי לדרוש בירור נוסף."),
    ("הרצליה", "herzliya", "בהרצליה", "בית פרטי או דירת גן", "לבית עם חצר או לדירת גן יש שטחים שחשוב לתאר לפני קביעת ההיקף: משטחים חיצוניים, פתחים, גג נגיש וחדרי שירות. הכינו רשימה של האזורים שתרצו לבדוק, כדי שהצעת המחיר והזמן לביקור יתאימו לנכס."),
    ("רעננה", "raanana", "ברעננה", "מסירת דירה חדשה", "לקראת מסירת דירה מקבלן, הכינו מפרט, תוכניות ומועד ביקור. כדאי לבדוק שהדירה נגישה ושניתן לפתוח ולראות את כל החדרים והמרפסות. תיעוד ממצאים בזמן הבדיקה מסייע בהעברת רשימה מסודרת לקבלן."),
    ("בני ברק", "bnei-brak", "בבני ברק", "דירה בבניין משותף", "אם יש סימן לליקוי שעשוי לערב גם שטח משותף, ציינו זאת מראש. בדיקת הדירה אינה כוללת אוטומטית רכוש משותף; הגדרת השטח הנדרש ותיאום הגישה יעזרו להבין מה ניתן לבדוק במסגרת הביקור."),
    ("אור יהודה", "or-yehuda", "באור יהודה", "בדיקת דירה לאחר שיפוץ", "בדירה שעברה שיפוץ, בקשו פירוט על העבודות והמסמכים הקיימים. בבדיקה אפשר להתייחס לגמרים, לפתחים, לסימני רטיבות ולמערכות נגישות. מסמכי השיפוץ יכולים לסייע להבין אם ממצא קשור לעבודה חדשה או למצב קודם."),
    ("רמת גן", "ramat-gan", "ברמת גן", "בדיקה בדירה בבניין גבוה", "בדירה בבניין גבוה כדאי להבחין בין מה שנמצא בתוך הדירה לבין מערכות ושטחים משותפים. אם חשוב לכם לבדוק גם מחסן, חניה או שטח נוסף, מסרו זאת מראש ובדקו שניתן לקבל גישה בזמן הביקור."),
    ("גבעתיים", "givatayim", "בגבעתיים", "תיאום בדיקה לפני רכישת דירה", "בדירה קיימת כדאי לשאול על תיקוני איטום, נזילות ושינויים שבוצעו לאורך השנים. אם יש מסמכים או תמונות של תקלה קודמת, שלחו אותם לפני הבדיקה. כך אפשר להתייחס למידע הקיים לצד מצב הנכס ביום הביקור."),
    ("כפר סבא", "kfar-saba", "בכפר סבא", "בדיקה לפני מסירה מקבלן", "לקראת מסירת דירה חדשה, רכזו את המפרט וההבטחות הכתובות שקיבלתם. בדיקה שיטתית של גמרים, פתחים, נקודות נגישות וסימני רטיבות מאפשרת להכין דוח מסודר לקראת הפנייה לקבלן."),
    ("קריית אונו", "kiryat-ono", "בקריית אונו", "בחירת היקף הבדיקה", "אם לדירה יש מחסן, חניה, מרפסת או גג נגיש, ציינו אילו מהם נדרשים לבדיקה. היקף שסוכם מראש מונע אי הבנות ביום הביקור ומאפשר להקדיש זמן לכל חלק רלוונטי בנכס."),
    ("פתח תקווה", "petah-tikva", "בפתח תקווה", "בדיקה לפני רכישת דירה יד שנייה", "לפני רכישה, רכזו את השאלות שעלו בסיורים בנכס: כתמים, סדקים, חלון שאינו נסגר או תיקון שתואר בעל פה. הבדיקה מתעדת ממצאים נגישים ויכולה לעזור להחליט אם דרוש בירור נוסף לפני העסקה."),
    ("ראש העין", "rosh-haayin", "בראש העין", "דירה חדשה עם שטחי חוץ", "אם לדירה החדשה יש מרפסת, חצר או גג נגיש, ודאו שהגישה אליהם פתוחה ביום הבדיקה. חשוב לתעד גם מפגשים בין פנים לחוץ, ניקוזים נגישים וגמרים, בהתאם להיקף שסוכם ולמסמכים שנמסרו לכם."),
    ("הוד השרון", "hod-hasharon", "בהוד השרון", "בדיקת בית עם חצר", "בבית עם חצר, ספרו מראש על מספר המפלסים, שטחי החוץ והגג אם הוא נגיש. הבדיקה של חללים פנימיים ושל משטחים חיצוניים דורשת תכנון זמן וגישה; תמונות מוקדמות של אזור שמדאיג אתכם יעזרו במיקוד."),
    ("גבעת שמואל", "givat-shmuel", "בגבעת שמואל", "מסמכים שכדאי להכין", "לקראת בדיקת דירה חדשה, הכינו מפרט ותוכנית אם קיבלתם. לפני בדיקת דירה קיימת, בקשו מידע על תיקונים ושיפוצים. מסמכים אלה אינם מחליפים את הבדיקה בשטח, אך מסייעים להציב שאלות מדויקות ולתעד ממצאים."),
    ("ראשון לציון", "rishon-lezion", "בראשון לציון", "דירה חדשה או יד שנייה", "ציינו כבר בפנייה אם הבדיקה נועדה למסירת דירה חדשה או להחלטה לפני רכישת דירה קיימת. במקרה הראשון כדאי להכין מפרט ומועד מסירה; במקרה השני מידע על תיקונים קודמים וסוגיות שעלו מול המוכר."),
    ("תל אביב-יפו", "tel-aviv-yafo", "בתל אביב-יפו", "בדיקה בדירה קיימת", "בדירה קיימת, שאלו אילו עבודות נעשו בנכס ובקשו גישה לאזורים שבהם התגלו בעבר בעיות. כדאי לציין אם יש מחסן, מרפסת או שטח נוסף שאתם מבקשים לכלול. היקף ברור מראש עוזר להפיק דוח שימושי להחלטה."),
    ("רמת השרון", "ramat-hasharon", "ברמת השרון", "בדיקת נכס עם גג או מרתף", "אם בנכס יש גג, מרתף או חדר שירות, שלחו תיאור ותמונות לפני התיאום. חלקים אלה עשויים לדרוש זמן וגישה נפרדים. בבדיקה ניתן לתעד סימנים גלויים ולציין היכן יש צורך בבירור נוסף."),
    ("יהוד-מונוסון", "yehud-monosson", "ביהוד-מונוסון", "מה לבדוק לפני ביקור בדירה", "דאגו לאפשר גישה לנכס כולו: חדרים, מרפסת, ארונות שירות ושטחים נוספים שסוכמו לבדיקה. הכינו את מועד העסקה או המסירה ותמונות של ממצאים שמטרידים אתכם, כדי להתאים את הביקור לצורך המדויק."),
]


def e(text: str) -> str:
    return escape(text, quote=True)


def header() -> str:
    return '''<header class="site-header"><a class="logo" href="/" aria-label="אור בדק בית, דף הבית"><img src="/public/images/or-bedek-logo-2026.png" alt="לוגו אור בדק בית"></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="פתיחת תפריט"><span></span><span></span></button></header>
<aside class="site-menu" id="site-menu" aria-hidden="true"><div class="menu-top"><img src="/public/images/or-bedek-logo-2026.png" alt="לוגו אור בדק בית"><button class="menu-close" type="button" aria-label="סגירת תפריט">×</button></div><nav aria-label="ניווט ראשי"><a href="/">עמוד הבית</a><a href="/about">קצת עליי</a><a href="/services">שירותים</a><a href="/service-areas">אזורי שירות</a><a href="/faq">שאלות נפוצות</a><a href="/blog">בלוג</a><a href="/contact">צור קשר</a></nav></aside><div class="menu-backdrop" aria-hidden="true"></div>'''


def footer() -> str:
    return '''<footer class="site-footer"><div class="footer-main"><section class="footer-brand" aria-label="אודות אור בדק בית"><a class="logo footer-logo" href="/"><img src="/public/images/or-bedek-logo-2026.png" alt="לוגו אור בדק בית"></a><h2>אור בדק בית</h2><p>בדק בית לדירות חדשות ויד שנייה, איתור ליקויים ודוחות מסודרים.</p></section><nav class="footer-column" aria-label="קישורים מהירים"><h2>קישורים מהירים</h2><a href="/">עמוד הבית</a><a href="/services">כל השירותים</a><a href="/service-areas">אזורי שירות</a><a href="/about">אודות אור דקר</a><a href="/contact">צור קשר</a></nav><nav class="footer-column" aria-label="שירותים מובילים"><h2>שירותים מובילים</h2><a href="/new-apartment-inspection">בדק בית לדירה חדשה</a><a href="/badek-home-before-buying">בדק בית לפני קנייה</a><a href="/moisture-inspection">בדיקת רטיבות</a><a href="/sample-report">דוח לדוגמה</a></nav><section class="footer-column footer-contact"><h2>צור קשר</h2><a href="tel:+972523199403">052-319-9403</a><a class="footer-cta" href="/contact">לתיאום בדיקת דירה</a></section></div><div class="footer-bottom"><span>© <span id="year"></span> אור בדק בית. כל הזכויות שמורות.</span><span>שירות בתיאום לפי מיקום הנכס</span></div></footer><script src="/script.js?v=20261029-1"></script>'''


def document(slug: str, title: str, description: str, body: str, schema: dict) -> str:
    url = f"{BASE}/{slug}"
    return f'''<!doctype html>
<html lang="he-IL" dir="rtl"><head><script src="/consent-init.js"></script>
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-MCD7BSML');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description" content="{e(description)}"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"><link rel="canonical" href="{url}"><link rel="describedby" href="{BASE}/llms.txt" type="text/plain">
<meta property="og:type" content="website"><meta property="og:locale" content="he_IL"><meta property="og:site_name" content="אור בדק בית"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/public/images/or-deker-social-share.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" href="/public/images/or-bedek-logo-2026.png"><title>{e(title)}</title><link rel="stylesheet" href="/styles.css?v=20261029-1"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script></head>
<body><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MCD7BSML" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>{header()}<main>{body}</main>{footer()}</body></html>
'''


def city_links(cities: list[tuple[str, ...]]) -> str:
    return '<div class="area-grid">' + ''.join(
        f'<a class="area-card" href="/home-inspection-{slug}"><strong>בדק בית {e(locative)}</strong><span>{e(name)}</span><b>למידע על השירות בעיר ←</b></a>'
        for name, slug, locative, *_ in cities
    ) + '</div>'


def build_hub() -> None:
    slug = 'service-areas'
    title = 'אזורי שירות בדק בית | אור בדק בית'
    description = 'בדק בית בעשרים ערים באזור המרכז והשרון. בחרו את העיר שלכם למידע על הכנה לבדיקה, שירות לדירה חדשה ולדירת יד שנייה ותיאום ביקור.'
    body = f'''<nav class="area-breadcrumb section" aria-label="פירורי לחם"><a href="/">בית</a><span> / אזורי שירות</span></nav>
<section class="section service-hero area-hero"><p class="eyebrow">אור בדק בית · אזורי שירות</p><h1>בדק בית באזורי השירות</h1><p>בחרו את העיר שבה נמצא הנכס כדי לראות כיצד להתכונן לבדיקה. הרשימה מבוססת על אזורי השירות שהוגדרו לעסק; זמינות ומועד הביקור נקבעים בשיחה לפי הנכס.</p></section>
<section class="section area-section"><h2>בחרו עיר</h2><p>העמודים עוסקים בבדיקת דירה חדשה מקבלן או נכס לפני רכישה. אם העיר שלכם אינה מופיעה, אפשר לפנות אלינו ולברר זמינות.</p>{city_links(CITIES)}</section>
<section class="section area-section area-guide"><h2>מה להכין לפני תיאום?</h2><div class="area-steps"><article><h3>פרטי הנכס</h3><p>כתובת, סוג נכס, גודל משוער ושטחים נוספים שתרצו לכלול בבדיקה.</p></article><article><h3>מועד ומטרה</h3><p>ציינו אם זו דירה חדשה לקראת מסירה או דירה קיימת לפני רכישה ומהו חלון הזמן לביקור.</p></article><article><h3>מסמכים ושאלות</h3><p>הכינו מפרט או תוכניות לדירה חדשה, ומידע על שיפוצים או ליקויים ידועים בנכס קיים.</p></article></div><p>למידע על היקף הבדיקה עברו אל <a href="/services">השירותים</a>; עלויות מוסברות ב<a href="/home-inspection-price">מדריך המחיר</a>.</p><a class="button primary" href="/contact">לבירור זמינות ותיאום</a></section>'''
    schema = {"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":f"{BASE}/{slug}#page","url":f"{BASE}/{slug}","name":title,"inLanguage":"he-IL","about":{"@id":f"{BASE}/#business"}},{"@type":"ItemList","name":"ערי שירות בדק בית","itemListElement":[{"@type":"ListItem","position":i,"name":c[0],"url":f"{BASE}/home-inspection-{c[1]}"} for i,c in enumerate(CITIES,1)]}]}
    (ROOT / f'{slug}.html').write_text(document(slug,title,description,body,schema),encoding='utf-8')


def build_city(index: int, city: tuple[str, ...]) -> None:
    name, city_slug, locative, focus_title, focus = city
    slug = f'home-inspection-{city_slug}'
    title = f'בדק בית {locative} | אור בדק בית'
    description = f'בדק בית {locative} לדירה חדשה או לפני רכישת דירה יד שנייה. מה להכין לפני הבדיקה, מה כולל התיאום וכיצד מקבלים דוח ממצאים ברור.'
    related = [CITIES[(index + offset) % len(CITIES)] for offset in (1, 2, 3)]
    body = f'''<nav class="area-breadcrumb section" aria-label="פירורי לחם"><a href="/">בית</a><span> / </span><a href="/service-areas">אזורי שירות</a><span> / {e(name)}</span></nav>
<section class="section service-hero area-hero"><p class="eyebrow">אזור שירות · {e(name)}</p><h1>בדק בית {e(locative)}</h1><p>אור בדק בית מתאם בדיקות לדירות חדשות ולדירות יד שנייה {e(locative)}. סוג הנכס, שלב העסקה והגישה לשטחים הנבדקים קובעים את היקף הביקור. בשיחה קצרה נגדיר את הצורך ואת המועד המתאים.</p><a class="button primary" href="/contact">לבדיקת זמינות ותיאום</a></section>
<section class="section area-section"><h2>{e(focus_title)}</h2><p>{e(focus)}</p><h2>איך הבדיקה מתנהלת?</h2><p>מתאמים את היקף הבדיקה לפי הנכס; בביקור סוקרים באופן שיטתי גמרים, פתחים, סימני רטיבות ומערכות שנגישות לבדיקה. לאחר מכן מתקבל דוח מסודר עם תיעוד הממצאים והערכת עלויות לפי היקף השירות שסוכם. ממצא שמצריך בדיקה נוספת יצוין בהתאם.</p><p>אם זו דירה חדשה, קראו על <a href="/new-apartment-inspection">בדק בית לפני מסירה</a>. אם זו דירה קיימת, ראו את <a href="/badek-home-before-buying">המדריך לבדיקה לפני קנייה</a> ואת <a href="/sample-report">הדוח לדוגמה</a>.</p></section>
<section class="section area-section area-guide"><h2>מה לשלוח לפני תיאום {e(locative)}?</h2><div class="area-steps"><article><h3>מיקום ונכס</h3><p>כתובת, סוג נכס, גודל משוער, קומה ושטחים נוספים כמו מרפסת, חצר או גג.</p></article><article><h3>שלב העסקה</h3><p>מועד מסירה או רכישה רצוי, ומתי אפשר להיכנס לנכס לביקור.</p></article><article><h3>מידע שכבר קיים</h3><p>מפרט ותוכניות, תיקונים קודמים או תמונות של ליקוי שמדאיג אתכם.</p></article></div><p>המחיר תלוי בגודל הנכס, בסוגו ובהיקף הבדיקה. לאחר קבלת הפרטים אפשר למסור הצעה מותאמת. <a href="/home-inspection-price">למידע על מחיר בדק בית</a>.</p><a class="button primary" href="/contact">לתיאום בדיקה {e(locative)}</a></section>
<section class="section area-section"><h2>ערי שירות נוספות</h2>{city_links(related)}<p><a href="/service-areas">לכל אזורי השירות ←</a></p></section>'''
    schema = {"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":f"{BASE}/{slug}#page","url":f"{BASE}/{slug}","name":title,"description":description,"inLanguage":"he-IL","isPartOf":{"@id":f"{BASE}/#website"},"about":{"@id":f"{BASE}/#business"}},{"@type":"Service","@id":f"{BASE}/{slug}#service","name":f"בדק בית {locative}","serviceType":"בדק בית ובדיקת דירה","provider":{"@id":f"{BASE}/#business"},"areaServed":{"@type":"City","name":name,"address":{"@type":"PostalAddress","addressLocality":name,"addressCountry":"IL"}},"url":f"{BASE}/{slug}"},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"בית","item":f"{BASE}/"},{"@type":"ListItem","position":2,"name":"אזורי שירות","item":f"{BASE}/service-areas"},{"@type":"ListItem","position":3,"name":name,"item":f"{BASE}/{slug}"}]}]}
    (ROOT / f'{slug}.html').write_text(document(slug,title,description,body,schema),encoding='utf-8')


if __name__ == '__main__':
    build_hub()
    for i, item in enumerate(CITIES):
        build_city(i, item)
