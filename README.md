# دليل استخدام نظام أتمتة تيك توك

## نظرة عامة

نظام أتمتة تيك توك هو برنامج متكامل يتيح لك إدارة حسابات تيك توك بشكل آلي، مع إمكانية:
- تحديد مكان عمل الحسابات عن طريق البروكسي للدول المستهدفة (السعودية، الإمارات، الكويت، مصر)
- محاكاة النشر من الهاتف المحمول وليس من متصفح الويب
- التحكم في التفاعلات (الإعجاب، التعليق، المشاركة، الحفظ)
- جدولة المنشورات على مدار اليوم

## متطلبات النظام

- Python 3.6 أو أحدث
- متصفح Chrome
- الوصول إلى الإنترنت
- المكتبات المطلوبة: selenium, undetected-chromedriver, pyautogui, requests, fake-useragent, python-dotenv

## تثبيت النظام

1. قم بتثبيت المكتبات المطلوبة:
```
pip install selenium undetected-chromedriver pyautogui requests fake-useragent python-dotenv
```

2. تأكد من تثبيت متصفح Chrome على جهازك.

3. قم بتنزيل ملفات النظام وتشغيل البرنامج الرئيسي:
```
chmod +x tiktok_automation.py
```

## هيكل النظام

النظام مقسم إلى عدة وحدات رئيسية:

1. **إدارة البروكسي**: للتحكم في البروكسي للدول المستهدفة.
2. **إدارة الحسابات**: لإدارة حسابات تيك توك وتخزين بيانات الاعتماد بشكل آمن.
3. **محاكاة الأجهزة المحمولة**: لمحاكاة الأجهزة المحمولة عند التفاعل مع تيك توك.
4. **التفاعل**: للتحكم في وظائف الإعجاب والتعليق والمشاركة والحفظ.
5. **الجدولة**: لجدولة المنشورات على مدار اليوم.

## استخدام النظام

### إدارة البروكسي

#### إضافة بروكسي
```
./tiktok_automation.py proxy add saudi_arabia 123.45.67.89:8080
```

#### إزالة بروكسي
```
./tiktok_automation.py proxy remove saudi_arabia 123.45.67.89:8080
```

#### عرض البروكسيات
```
./tiktok_automation.py proxy list
```

#### اختبار البروكسي
```
./tiktok_automation.py proxy test --proxy 123.45.67.89:8080
```

### إدارة الحسابات

#### إضافة حساب
```
./tiktok_automation.py account add username password saudi_arabia --proxy 123.45.67.89:8080
```

#### إزالة حساب
```
./tiktok_automation.py account remove username
```

#### تحديث حساب
```
./tiktok_automation.py account update username --password newpassword --country uae --proxy 123.45.67.89:8080
```

#### عرض الحسابات
```
./tiktok_automation.py account list
```

#### اختبار الحساب
```
./tiktok_automation.py account test username
```

### محاكاة الأجهزة المحمولة

#### إضافة جهاز
```
./tiktok_automation.py mobile add "iPhone 13" "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1" 390 844 3.0 iOS
```

#### إزالة جهاز
```
./tiktok_automation.py mobile remove "iPhone 13"
```

#### عرض الأجهزة
```
./tiktok_automation.py mobile list
```

#### اختبار محاكاة الأجهزة المحمولة
```
./tiktok_automation.py mobile test --device "iPhone 13" --country saudi_arabia
```

### التفاعل

#### اختبار التفاعل
```
./tiktok_automation.py engagement test username --video-url https://www.tiktok.com/@username/video/1234567890 --action like
```

#### إدارة التعليقات
```
./tiktok_automation.py engagement comment add general "تعليق جديد"
./tiktok_automation.py engagement comment list
```

### الجدولة

#### إضافة منشور مجدول
```
./tiktok_automation.py schedule add username /path/to/video.mp4 "وصف الفيديو" "2025-04-21 12:00:00" --tags "tag1,tag2,tag3"
```

#### إزالة منشور مجدول
```
./tiktok_automation.py schedule remove post_id
```

#### عرض المنشورات المجدولة
```
./tiktok_automation.py schedule list
```

#### تنفيذ المنشورات المجدولة
```
./tiktok_automation.py schedule execute
```

### تشغيل النظام

#### تنفيذ المنشورات المجدولة والتفاعل العشوائي
```
./tiktok_automation.py run --username username --execute-posts --random-engagement --engagement-count 10 --engagement-interval 120
```

## ملاحظات هامة

1. **أمان الحسابات**: يتم تشفير كلمات المرور وتخزينها بشكل آمن.
2. **محاكاة الأجهزة المحمولة**: تأكد من استخدام محاكاة الأجهزة المحمولة لتجنب اكتشاف الأتمتة.
3. **البروكسي**: استخدم بروكسي موثوق للدول المستهدفة.
4. **جدولة المنشورات**: قم بتوزيع المنشورات على مدار اليوم لتجنب الحظر.
5. **التفاعل**: استخدم التفاعل العشوائي لمحاكاة سلوك المستخدم الحقيقي.

## استكشاف الأخطاء وإصلاحها

1. **مشاكل تسجيل الدخول**: تأكد من صحة بيانات الاعتماد والبروكسي.
2. **مشاكل البروكسي**: تأكد من أن البروكسي يعمل بشكل صحيح.
3. **مشاكل محاكاة الأجهزة المحمولة**: تأكد من تثبيت متصفح Chrome بشكل صحيح.
4. **مشاكل التفاعل**: تأكد من تسجيل الدخول بنجاح قبل محاولة التفاعل.
5. **مشاكل الجدولة**: تأكد من صحة تنسيق وقت الجدولة.

## الدعم

إذا واجهت أي مشاكل أو كان لديك أي استفسارات، يرجى الاتصال بفريق الدعم.
