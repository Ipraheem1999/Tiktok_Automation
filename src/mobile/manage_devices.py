"""
وحدة إدارة ملفات الأجهزة المحمولة
توفر واجهة سطر أوامر لإدارة الأجهزة المحمولة المحاكاة
"""

import argparse
import sys
import os
import json
from src.mobile.mobile_simulator import MobileSimulator

def main():
    """
    النقطة الرئيسية لتشغيل إدارة ملفات الأجهزة المحمولة
    """
    parser = argparse.ArgumentParser(description='إدارة الأجهزة المحمولة المحاكاة')
    subparsers = parser.add_subparsers(dest='command', help='الأمر المراد تنفيذه')
    
    # أمر إضافة جهاز
    add_parser = subparsers.add_parser('add', help='إضافة جهاز محمول جديد')
    add_parser.add_argument('name', help='اسم الجهاز')
    add_parser.add_argument('user_agent', help='وكيل المستخدم')
    add_parser.add_argument('width', type=int, help='عرض الشاشة')
    add_parser.add_argument('height', type=int, help='ارتفاع الشاشة')
    add_parser.add_argument('pixel_ratio', type=float, help='نسبة البكسل')
    add_parser.add_argument('platform', choices=['iOS', 'Android'], help='منصة الجهاز')
    
    # أمر إزالة جهاز
    remove_parser = subparsers.add_parser('remove', help='إزالة جهاز محمول')
    remove_parser.add_argument('name', help='اسم الجهاز')
    
    # أمر عرض جهاز
    show_parser = subparsers.add_parser('show', help='عرض معلومات الجهاز')
    show_parser.add_argument('name', help='اسم الجهاز')
    
    # أمر عرض جميع الأجهزة
    list_parser = subparsers.add_parser('list', help='عرض جميع الأجهزة')
    list_parser.add_argument('--platform', choices=['iOS', 'Android'], help='تصفية حسب المنصة')
    
    # أمر الحصول على جهاز عشوائي
    random_parser = subparsers.add_parser('random', help='الحصول على جهاز عشوائي')
    random_parser.add_argument('--platform', choices=['iOS', 'Android'], help='تصفية حسب المنصة')
    
    # أمر الحصول على وكيل مستخدم عشوائي
    user_agent_parser = subparsers.add_parser('user-agent', help='الحصول على وكيل مستخدم عشوائي')
    user_agent_parser.add_argument('--platform', choices=['iOS', 'Android'], help='تصفية حسب المنصة')
    
    args = parser.parse_args()
    
    # إنشاء محاكي الأجهزة المحمولة
    mobile_simulator = MobileSimulator()
    
    if args.command == 'add':
        success = mobile_simulator.add_device(
            args.name,
            args.user_agent,
            args.width,
            args.height,
            args.pixel_ratio,
            args.platform
        )
        
        if success:
            print(f"تمت إضافة الجهاز بنجاح: {args.name}")
        else:
            print(f"فشل في إضافة الجهاز: {args.name}")
            return 1
    
    elif args.command == 'remove':
        success = mobile_simulator.remove_device(args.name)
        
        if success:
            print(f"تمت إزالة الجهاز بنجاح: {args.name}")
        else:
            print(f"فشل في إزالة الجهاز: {args.name}")
            return 1
    
    elif args.command == 'show':
        device = mobile_simulator.get_device(args.name)
        
        if device:
            print(f"معلومات الجهاز: {args.name}")
            print(json.dumps(device, ensure_ascii=False, indent=2))
        else:
            print(f"لم يتم العثور على الجهاز: {args.name}")
            return 1
    
    elif args.command == 'list':
        devices = mobile_simulator.get_all_devices()
        
        if args.platform:
            devices = [device for device in devices if device['platform'] == args.platform]
            print(f"الأجهزة المحمولة لمنصة {args.platform}:")
        else:
            print("جميع الأجهزة المحمولة:")
            
        if not devices:
            print("  لا توجد أجهزة")
        else:
            for device in devices:
                print(f"  {device['name']} - المنصة: {device['platform']}, الأبعاد: {device['width']}x{device['height']}")
    
    elif args.command == 'random':
        device = mobile_simulator.get_random_device(args.platform)
        
        print(f"جهاز عشوائي:")
        print(json.dumps(device, ensure_ascii=False, indent=2))
    
    elif args.command == 'user-agent':
        user_agent = mobile_simulator.get_random_user_agent(args.platform)
        
        print(f"وكيل مستخدم عشوائي:")
        print(user_agent)
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
