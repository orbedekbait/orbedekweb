# חיבור ביקורות Google לעמוד הבית

הרכיב בעמוד הבית נטען מ-Google Places API (New) דרך Netlify Function. מפתח ה-API נשאר בצד השרת, והרכיב מוסתר אוטומטית אם החיבור עדיין לא הוגדר או אם השירות אינו זמין.

## הגדרה

1. יוצרים או בוחרים פרויקט ב-[Google Cloud Console](https://console.cloud.google.com/google/maps-apis/overview).
2. מחברים חשבון חיוב ומפעילים את **Places API (New)**.
3. יוצרים API key ומגבילים אותו ל-**Places API (New)** בלבד.
4. מאתרים את ה-Place ID של העסק בעזרת [Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder).
5. ב-Netlify נכנסים ל-**Site configuration → Environment variables** ומוסיפים:
   - `GOOGLE_PLACES_API_KEY`
   - `GOOGLE_PLACE_ID`
6. מבצעים deploy חדש.

לפיתוח מקומי אפשר להעתיק את `.env.example` לקובץ `.env`, למלא את הערכים ולהריץ `netlify dev`.

## הערות חשובות

- Google מחזירה עד חמש ביקורות וממיינת אותן לפי רלוונטיות; אי אפשר לבקש דרך Place Details רשימה ארוכה יותר או לבחור ידנית את סדר התוצאות.
- אין לשמור את תוכן הביקורות במסד נתונים או בקובץ סטטי. הפונקציה מחזירה `Cache-Control: no-store` כדי שהתוכן יישאר עדכני ובהתאם לכללי Google.
- לפני הפעלה באתר חי, יש לוודא שמדיניות הפרטיות ותנאי השימוש של האתר כוללים את השימוש ב-Google Maps Platform ואת הקישורים הנדרשים לתנאי Google ולמדיניות הפרטיות שלה.
- השימוש ב-Places API עשוי להיות כרוך בעלות. מומלץ להגדיר תקציב והתראות חיוב ב-Google Cloud.

מקורות: [Place Details (New)](https://developers.google.com/maps/documentation/places/web-service/place-details), [Policies and attributions](https://developers.google.com/maps/documentation/places/web-service/policies), [Google Maps links](https://developers.google.com/maps/documentation/places/web-service/maps-links).
