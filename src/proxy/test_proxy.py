"""
وحدة اختبار البروكسي
توفر واجهة سطر أوامر لاختبار إعدادات البروكسي للدول المستهدفة
"""

import argparse
import sys
import os
import json
from src.proxy.proxy_manager import ProxyManager

def main():
    """
    النقطة الرئيسية لتشغيل اختبار البروكسي
    """
    parser = argparse.ArgumentParser(description='اختبار إعدادات البروكسي للدول المستهدفة')
    parser.add_argument('--country', '-c', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt', 'all'],
                        default='all', help='الدولة المستهدفة لاختبار البروكسي')
    parser.add_argument('--proxy-file', '-f', help='مسار ملف البروكسي')
    parser.add_argument('--proxy', '-p', help='عنوان البروكسي للاختبار مباشرة')
    parser.add_argument('--test', '-t', action='store_true', help='اختبار اتصال البروكسي')
    
    args = parser.parse_args()
    
    # إنشاء مدير البروكسي
    proxy_manager = ProxyManager()
    
    # تحميل البروكسي من ملف التكوين
    config_loaded = proxy_manager.load_proxies_from_config()
    
    # تحميل البروكسي من ملف إذا تم تحديده
    if args.proxy_file:
        if args.country != 'all':
            file_loaded = proxy_manager.load_proxies_from_file(args.proxy_file, args.country)
        else:
            file_loaded = proxy_manager.load_proxies_from_file(args.proxy_file)
            
        if not file_loaded:
            print(f"فشل في تحميل البروكسي من الملف: {args.proxy_file}")
            return 1
    
    # اختبار بروكسي محدد مباشرة
    if args.proxy:
        print(f"اختبار البروكسي: {args.proxy}")
        result = proxy_manager.test_proxy(args.proxy)
        print(f"نتيجة الاختبار: {'ناجح' if result else 'فاشل'}")
        return 0 if result else 1
    
    # اختبار البروكسي للدولة المحددة
    if args.test:
        if args.country == 'all':
            # اختبار البروكسي لجميع الدول
            results = {}
            for country in proxy_manager.proxies.keys():
                proxy = proxy_manager.get_proxy_for_country(country)
                if proxy:
                    result = proxy_manager.test_proxy()
                    results[country] = {
                        'proxy': proxy,
                        'result': result
                    }
                else:
                    results[country] = {
                        'proxy': None,
                        'result': False
                    }
            
            print(json.dumps(results, indent=2, ensure_ascii=False))
            # التحقق مما إذا كان هناك بروكسي واحد على الأقل يعمل
            return 0 if any(r['result'] for r in results.values()) else 1
        else:
            # اختبار البروكسي للدولة المحددة
            proxy = proxy_manager.get_proxy_for_country(args.country)
            if proxy:
                result = proxy_manager.test_proxy()
                print(f"البروكسي للدولة {args.country}: {proxy}")
                print(f"نتيجة الاختبار: {'ناجح' if result else 'فاشل'}")
                return 0 if result else 1
            else:
                print(f"لم يتم العثور على بروكسي للدولة: {args.country}")
                return 1
    
    # عرض معلومات البروكسي المتاحة
    if args.country == 'all':
        for country, proxies in proxy_manager.proxies.items():
            print(f"البروكسي للدولة {country}:")
            if proxies:
                for i, proxy in enumerate(proxies, 1):
                    print(f"  {i}. {proxy}")
            else:
                print("  لا يوجد بروكسي متاح")
    else:
        proxies = proxy_manager.proxies.get(args.country, [])
        print(f"البروكسي للدولة {args.country}:")
        if proxies:
            for i, proxy in enumerate(proxies, 1):
                print(f"  {i}. {proxy}")
        else:
            print("  لا يوجد بروكسي متاح")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
