# 📱 TikTok Automation System

نظام أتمتة تيك توك للتحكم الكامل بالحسابات، التفاعل، الجدولة، والمحاكاة، عبر واجهة سطر الأوامر.

---

## ⚙️ تشغيل البرنامج

```bash
python tiktok_automation.py <command> <subcommand> [options]
```

---

## 🧭 أوامر النظام

### 1. `proxy` - إدارة البروكسيات

#### إضافة بروكسي

```bash
python tiktok_automation.py proxy add saudi_arabia 192.168.0.1:8080
```

#### إزالة بروكسي

```bash
python tiktok_automation.py proxy remove uae 192.168.0.2:8080
```

#### عرض البروكسيات

```bash
python tiktok_automation.py proxy list --country egypt
```

#### اختبار بروكسي

```bash
python tiktok_automation.py proxy test --proxy 192.168.0.3:9090
```

---

### 2. `account` - إدارة الحسابات

#### إضافة حساب

```bash
python tiktok_automation.py account add user1 pass123 saudi_arabia --proxy 192.168.0.1:8080
```

#### إزالة حساب

```bash
python tiktok_automation.py account remove user1
```

#### تحديث حساب

```bash
python tiktok_automation.py account update user1 --password newpass --proxy 192.168.0.5:9090
```

#### عرض الحسابات

```bash
python tiktok_automation.py account list --country uae
```

#### اختبار تسجيل الدخول

```bash
python tiktok_automation.py account test user1 --wait 15
```

---

### 3. `mobile` - محاكاة الأجهزة

#### إضافة جهاز

```bash
python tiktok_automation.py mobile add Pixel5 "Mozilla UA" 1080 2340 2.5 Android
```

#### إزالة جهاز

```bash
python tiktok_automation.py mobile remove Pixel5
```

#### عرض الأجهزة

```bash
python tiktok_automation.py mobile list --platform Android
```

#### اختبار محاكاة

```bash
python tiktok_automation.py mobile test --device Pixel5 --country saudi_arabia --wait 20
```

---

### 4. `engagement` - التفاعل

#### تنفيذ تفاعل

```bash
python tiktok_automation.py engagement test user1 --action like --video-url https://www.tiktok.com/@user/video/xyz
```

#### إدارة التعليقات

```bash
python tiktok_automation.py engagement comment add funny "هههه ممتاز"
```

---

### 5. `schedule` - الجدولة

#### إضافة منشور

```bash
python tiktok_automation.py schedule add user1 ./videos/vid1.mp4 "وصف الفيديو" "2025-05-01 14:00:00" --tags "fun,trend"
```

#### إزالة منشور

```bash
python tiktok_automation.py schedule remove 123456
```

#### عرض المنشورات

```bash
python tiktok_automation.py schedule list --username user1
```

#### تنفيذ المنشورات

```bash
python tiktok_automation.py schedule execute
```

---

### 6. `run` - تشغيل النظام

#### تنفيذ المنشورات والتفاعل

```bash
python tiktok_automation.py run --username user1 --execute-posts --random-engagement --engagement-count 3 --engagement-interval 60
```

---

## 🌍 الدول المدعومة

- saudi\_arabia
- uae
- kuwait
- egypt

---

## 💡 ملاحظات

- تم إنشاء مجلدات `logs`, `config`, `data`, `videos`, `cookies` تلقائيا عند أول تشغيل.
- تم حفظ السجلات في `logs/tiktok_automation.log`

