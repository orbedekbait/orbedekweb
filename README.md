# אור בדק בית — אתר טיוטה

זהו אתר HTML סטטי בעברית. כתובות העמודים הציבוריות נקיות מסיומת, למשל `/about`, ולכן התצוגה המקומית משתמשת בשרת הפיתוח המצורף:

```bash
python3 scripts/dev_server.py
```

לאחר מכן פותחים `http://localhost:8000`. השרת ממפה את הכתובות הנקיות לקובצי ה-HTML המקומיים כפי ש-Netlify עושה בפרודקשן.

פרטים שעדיין דרושים מסומנים ב-`placeholders.json` באמצעות `TODO`.

## בדיקות לפני פריסה

כל פריסה ב-Netlify מריצה אוטומטית את בדיקת ה-SEO:

```bash
python3 scripts/seo_audit.py
```

הבדיקה חוסמת פריסה אם נשברים canonical, sitemap, הפניות, קישורים פנימיים,
metadata, JSON-LD, אירועי ההמרה או תמונות הבלוג הרספונסיביות.

## יצירת מאמר חדש

משכפלים את `templates/article-template.html` לשורש הריפו בשם ה-slag באנגלית,
ממלאים את כל ערכי `TODO`, מוסיפים את העמוד ל-`blog.html` ול-`sitemap.xml`,
מחליפים את `noindex, nofollow` ב-`index, follow`, ומעדכנים `lastmod` רק לאחר שינוי מהותי בתוכן.
