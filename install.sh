#!/bin/bash
# نص تثبيت نظام أتمتة تيك توك

echo "بدء تثبيت نظام أتمتة تيك توك..."


# إنشاء بيئة افتراضية
echo "إنشاء بيئة افتراضية..."
if [ ! -d "venv" ]; then
    echo "تثبيت Python 3.9..."
    sudo apt-get update
    sudo apt-get install python3.9 python3.9-venv -y
else
    echo "بيئة افتراضية موجودة بالفعل."
fi
# التحقق من وجود Python 3.9
if ! command -v python3.9 &> /dev/null
then
    echo "Python 3.9 غير مثبت. يرجى تثبيته أولاً."
    exit
fi
python3.9 -m venv venv
source venv/bin/activate
echo "تفعيل البيئة الافتراضية..."
# تثبيت المتطلبات
echo "تثبيت المتطلبات..."
pip install selenium undetected-chromedriver pyautogui requests fake-useragent python-dotenv cryptography distutils

# إنشاء الدلائل اللازمة
echo "إنشاء الدلائل اللازمة..."
mkdir -m 777 -p logs config data videos cookies

# تعيين صلاحيات التنفيذ للبرنامج الرئيسي
echo "تعيين صلاحيات التنفيذ للبرنامج الرئيسي..."
chmod +x tiktok_automation.py

echo "تم تثبيت نظام أتمتة تيك توك بنجاح!"
echo "لبدء استخدام النظام، قم بتشغيل البرنامج الرئيسي باستخدام الأمر:"
echo "./tiktok_automation.py"
echo "للحصول على مزيد من المعلومات، راجع ملف README.md"
