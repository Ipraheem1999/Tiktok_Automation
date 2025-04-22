"""
وحدة إنشاء ملف .env للإعدادات البيئية
"""

import os
import argparse
import sys

def create_env_file(file_path, proxy_host=None, proxy_port=None, proxy_username=None, proxy_password=None, 
                   proxy_enabled=True, mobile_simulation=True, headless=False):
    """
    إنشاء ملف .env بالإعدادات المحددة
    
    المعلمات:
        file_path (str): مسار ملف .env
        proxy_host (str): مضيف البروكسي
        proxy_port (str): منفذ البروكسي
        proxy_username (str): اسم مستخدم البروكسي
        proxy_password (str): كلمة مرور البروكسي
        proxy_enabled (bool): تفعيل البروكسي
        mobile_simulation (bool): تفعيل محاكاة الأجهزة المحمولة
        headless (bool): تشغيل المتصفح بدون واجهة رسومية
    """
    env_content = f"""# إعدادات البروكسي
PROXY_ENABLED={str(proxy_enabled).lower()}
PROXY_TYPE=http
PROXY_HOST={proxy_host or ''}
PROXY_PORT={proxy_port or ''}
PROXY_USERNAME={proxy_username or ''}
PROXY_PASSWORD={proxy_password or ''}

# إعدادات المتصفح
HEADLESS={str(headless).lower()}
USER_DATA_DIR=./browser_data
WINDOW_SIZE=1920,1080

# إعدادات محاكاة الجوال
MOBILE_SIMULATION={str(mobile_simulation).lower()}
"""
    
    with open(file_path, 'w') as f:
        f.write(env_content)
    
    print(f"تم إنشاء ملف .env في: {file_path}")

def main():
    """
    النقطة الرئيسية لتشغيل إنشاء ملف .env
    """
    parser = argparse.ArgumentParser(description='إنشاء ملف .env للإعدادات البيئية')
    parser.add_argument('--output', '-o', default='.env', help='مسار ملف الإخراج')
    parser.add_argument('--proxy-host', help='مضيف البروكسي')
    parser.add_argument('--proxy-port', help='منفذ البروكسي')
    parser.add_argument('--proxy-username', help='اسم مستخدم البروكسي')
    parser.add_argument('--proxy-password', help='كلمة مرور البروكسي')
    parser.add_argument('--proxy-enabled', action='store_true', default=True, help='تفعيل البروكسي')
    parser.add_argument('--no-proxy', dest='proxy_enabled', action='store_false', help='تعطيل البروكسي')
    parser.add_argument('--mobile-simulation', action='store_true', default=True, help='تفعيل محاكاة الأجهزة المحمولة')
    parser.add_argument('--no-mobile-simulation', dest='mobile_simulation', action='store_false', help='تعطيل محاكاة الأجهزة المحمولة')
    parser.add_argument('--headless', action='store_true', help='تشغيل المتصفح بدون واجهة رسومية')
    
    args = parser.parse_args()
    
    create_env_file(
        args.output,
        args.proxy_host,
        args.proxy_port,
        args.proxy_username,
        args.proxy_password,
        args.proxy_enabled,
        args.mobile_simulation,
        args.headless
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
