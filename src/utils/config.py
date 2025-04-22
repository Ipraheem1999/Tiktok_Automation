"""
وحدة التكوين الرئيسية للنظام
تحتوي على الإعدادات والثوابت المستخدمة في جميع أنحاء التطبيق
"""

import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env إذا كان موجودًا
load_dotenv()

# الدول المستهدفة
TARGET_COUNTRIES = {
    'saudi_arabia': {
        'name': 'المملكة العربية السعودية',
        'code': 'SA',
        'language': 'ar',
        'timezone': 'Asia/Riyadh'
    },
    'uae': {
        'name': 'الإمارات العربية المتحدة',
        'code': 'AE',
        'language': 'ar',
        'timezone': 'Asia/Dubai'
    },
    'kuwait': {
        'name': 'الكويت',
        'code': 'KW',
        'language': 'ar',
        'timezone': 'Asia/Kuwait'
    },
    'egypt': {
        'name': 'مصر',
        'code': 'EG',
        'language': 'ar',
        'timezone': 'Africa/Cairo'
    }
}

# إعدادات المتصفح
BROWSER_SETTINGS = {
    'headless': os.getenv('HEADLESS', 'False').lower() == 'true',
    'user_data_dir': os.getenv('USER_DATA_DIR', './browser_data'),
    'window_size': os.getenv('WINDOW_SIZE', '1920,1080'),
    'disable_gpu': True,
    'no_sandbox': True,
    'disable_dev_shm_usage': True,
}

# إعدادات البروكسي
PROXY_ENABLED = os.getenv('PROXY_ENABLED', 'False').lower() == 'true'
PROXY_TYPE = os.getenv('PROXY_TYPE', 'http')  # http, socks4, socks5
PROXY_HOST = os.getenv('PROXY_HOST', '')
PROXY_PORT = os.getenv('PROXY_PORT', '')
PROXY_USERNAME = os.getenv('PROXY_USERNAME', '')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', '')

# إعدادات محاكاة الجوال
MOBILE_SIMULATION = os.getenv('MOBILE_SIMULATION', 'True').lower() == 'true'

# قائمة وكلاء المستخدم للأجهزة المحمولة
MOBILE_USER_AGENTS = [
    # Android - Samsung Galaxy
    'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    # Android - Google Pixel
    'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    # iOS - iPhone
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/112.0.5615.46 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/112.0.5615.46 Mobile/15E148 Safari/604.1',
]

# إعدادات TikTok
TIKTOK_URL = 'https://www.tiktok.com/'
TIKTOK_LOGIN_URL = 'https://www.tiktok.com/login'
TIKTOK_UPLOAD_URL = 'https://www.tiktok.com/upload'

# إعدادات الجدولة
DEFAULT_SCHEDULE_INTERVAL = 3600  # بالثواني (ساعة واحدة)
MIN_SCHEDULE_INTERVAL = 900  # بالثواني (15 دقيقة)

# إعدادات التفاعل
DEFAULT_LIKE_PROBABILITY = 0.7  # احتمالية الإعجاب بمنشور
DEFAULT_COMMENT_PROBABILITY = 0.3  # احتمالية التعليق على منشور
DEFAULT_SHARE_PROBABILITY = 0.2  # احتمالية مشاركة منشور
DEFAULT_SAVE_PROBABILITY = 0.4  # احتمالية حفظ منشور

# قائمة التعليقات الافتراضية (يمكن تخصيصها لكل حساب)
DEFAULT_COMMENTS = [
    "رائع! 👏",
    "محتوى مميز 🔥",
    "استمر في النشر 👍",
    "أعجبني كثيرًا ❤️",
    "شكرًا على المشاركة 🙏",
]
