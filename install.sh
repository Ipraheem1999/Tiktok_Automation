#!/bin/bash
# نص تثبيت نظام أتمتة تيك توك

echo "بدء تثبيت نظام أتمتة تيك توك..."

# التأكد من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "خطأ: Python3 غير مثبت. الرجاء تثبيت Python3 أولاً."
    exit 1
fi

# التأكد من وجود pip
if ! command -v pip3 &> /dev/null; then
    echo "خطأ: pip3 غير مثبت. الرجاء تثبيت pip3 أولاً."
    exit 1
fi

# تثبيت المكتبات المطلوبة
echo "تثبيت المكتبات المطلوبة..."
pip3 install selenium undetected-chromedriver pyautogui requests fake-useragent python-dotenv

# إنشاء الدلائل اللازمة
echo "إنشاء الدلائل اللازمة..."
mkdir -p logs config data videos cookies

# تعيين صلاحيات التنفيذ للبرنامج الرئيسي
echo "تعيين صلاحيات التنفيذ للبرنامج الرئيسي..."
chmod +x tiktok_automation.py

echo "تم تثبيت نظام أتمتة تيك توك بنجاح!"
echo "لبدء استخدام النظام، قم بتشغيل البرنامج الرئيسي باستخدام الأمر:"
echo "./tiktok_automation.py"
echo "للحصول على مزيد من المعلومات، راجع ملف README.md"
