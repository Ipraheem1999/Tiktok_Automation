"""
وحدة إدارة ملفات البروكسي
توفر واجهة سطر أوامر لإدارة ملفات البروكسي للدول المستهدفة
"""

import argparse
import sys
import os
import json
from src.proxy.country_proxy import CountryProxyConfigurator

def main():
    """
    النقطة الرئيسية لتشغيل إدارة ملفات البروكسي
    """
    parser = argparse.ArgumentParser(description='إدارة ملفات البروكسي للدول المستهدفة')
    subparsers = parser.add_subparsers(dest='command', help='الأمر المراد تنفيذه')
    
    # أمر استيراد البروكسي
    import_parser = subparsers.add_parser('import', help='استيراد البروكسي من ملف')
    import_parser.add_argument('file', help='مسار ملف البروكسي')
    
    # أمر تصدير البروكسي
    export_parser = subparsers.add_parser('export', help='تصدير البروكسي إلى ملف')
    export_parser.add_argument('file', help='مسار ملف البروكسي')
    
    # أمر إضافة بروكسي
    add_parser = subparsers.add_parser('add', help='إضافة بروكسي لدولة محددة')
    add_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة المستهدفة')
    add_parser.add_argument('proxy', help='عنوان البروكسي')
    
    # أمر إزالة بروكسي
    remove_parser = subparsers.add_parser('remove', help='إزالة بروكسي من دولة محددة')
    remove_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة المستهدفة')
    remove_parser.add_argument('proxy', help='عنوان البروكسي')
    
    # أمر تفعيل/تعطيل دولة
    enable_parser = subparsers.add_parser('enable', help='تفعيل/تعطيل دولة')
    enable_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt', 'all'], help='الدولة المستهدفة')
    enable_parser.add_argument('--disable', action='store_true', help='تعطيل الدولة بدلاً من تفعيلها')
    
    # أمر اختبار البروكسي
    test_parser = subparsers.add_parser('test', help='اختبار البروكسي للدولة المحددة')
    test_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt', 'all'], help='الدولة المستهدفة')
    
    # أمر عرض البروكسي
    list_parser = subparsers.add_parser('list', help='عرض البروكسي للدولة المحددة')
    list_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt', 'all'], help='الدولة المستهدفة')
    
    args = parser.parse_args()
    
    # إنشاء مكون تكوين البروكسي
    configurator = CountryProxyConfigurator()
    
    if args.command == 'import':
        results = configurator.import_proxies_from_file(args.file)
        print("نتائج الاستيراد:")
        for country, count in results.items():
            print(f"  {country}: {count} بروكسي")
    
    elif args.command == 'export':
        success = configurator.export_proxies_to_file(args.file)
        if success:
            print(f"تم تصدير البروكسي بنجاح إلى: {args.file}")
        else:
            print("فشل في تصدير البروكسي")
            return 1
    
    elif args.command == 'add':
        success = configurator.add_proxy(args.country, args.proxy)
        if success:
            print(f"تمت إضافة البروكسي بنجاح للدولة: {args.country}")
        else:
            print("فشل في إضافة البروكسي")
            return 1
    
    elif args.command == 'remove':
        success = configurator.remove_proxy(args.country, args.proxy)
        if success:
            print(f"تمت إزالة البروكسي بنجاح من الدولة: {args.country}")
        else:
            print("فشل في إزالة البروكسي")
            return 1
    
    elif args.command == 'enable':
        if args.country == 'all':
            for country in ['saudi_arabia', 'uae', 'kuwait', 'egypt']:
                configurator.set_country_enabled(country, not args.disable)
            print(f"تم {'تعطيل' if args.disable else 'تفعيل'} جميع الدول بنجاح")
        else:
            success = configurator.set_country_enabled(args.country, not args.disable)
            if success:
                print(f"تم {'تعطيل' if args.disable else 'تفعيل'} الدولة بنجاح: {args.country}")
            else:
                print("فشل في تغيير حالة الدولة")
                return 1
    
    elif args.command == 'test':
        if args.country == 'all':
            for country in ['saudi_arabia', 'uae', 'kuwait', 'egypt']:
                results = configurator.test_country_proxies(country)
                print(f"نتائج اختبار البروكسي للدولة {country}:")
                if not results:
                    print("  لا يوجد بروكسي متاح")
                else:
                    for proxy, result in results.items():
                        print(f"  {proxy}: {'ناجح' if result else 'فاشل'}")
        else:
            results = configurator.test_country_proxies(args.country)
            print(f"نتائج اختبار البروكسي للدولة {args.country}:")
            if not results:
                print("  لا يوجد بروكسي متاح")
            else:
                for proxy, result in results.items():
                    print(f"  {proxy}: {'ناجح' if result else 'فاشل'}")
    
    elif args.command == 'list':
        if args.country == 'all':
            for country in ['saudi_arabia', 'uae', 'kuwait', 'egypt']:
                proxies = configurator.get_country_proxies(country)
                country_info = configurator.get_country_info(country)
                print(f"البروكسي للدولة {country} ({country_info['name']}):")
                if not proxies:
                    print("  لا يوجد بروكسي متاح")
                else:
                    for i, proxy in enumerate(proxies, 1):
                        print(f"  {i}. {proxy}")
        else:
            proxies = configurator.get_country_proxies(args.country)
            country_info = configurator.get_country_info(args.country)
            print(f"البروكسي للدولة {args.country} ({country_info['name']}):")
            if not proxies:
                print("  لا يوجد بروكسي متاح")
            else:
                for i, proxy in enumerate(proxies, 1):
                    print(f"  {i}. {proxy}")
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
