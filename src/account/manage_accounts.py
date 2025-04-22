"""
وحدة إدارة ملفات الحسابات
توفر واجهة سطر أوامر لإدارة حسابات تيك توك
"""

import argparse
import sys
import os
import json
from src.account.account_manager import AccountManager

def main():
    """
    النقطة الرئيسية لتشغيل إدارة ملفات الحسابات
    """
    parser = argparse.ArgumentParser(description='إدارة حسابات تيك توك')
    subparsers = parser.add_subparsers(dest='command', help='الأمر المراد تنفيذه')
    
    # أمر إضافة حساب
    add_parser = subparsers.add_parser('add', help='إضافة حساب جديد')
    add_parser.add_argument('username', help='اسم المستخدم')
    add_parser.add_argument('password', help='كلمة المرور')
    add_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة المستهدفة')
    add_parser.add_argument('--nickname', help='الاسم المستعار للحساب')
    add_parser.add_argument('--cookies', help='مسار ملف ملفات تعريف الارتباط')
    add_parser.add_argument('--user-agent', help='وكيل المستخدم')
    add_parser.add_argument('--no-mobile', dest='mobile', action='store_false', help='تعطيل محاكاة الأجهزة المحمولة')
    
    # أمر إزالة حساب
    remove_parser = subparsers.add_parser('remove', help='إزالة حساب')
    remove_parser.add_argument('username', help='اسم المستخدم')
    
    # أمر تحديث حساب
    update_parser = subparsers.add_parser('update', help='تحديث معلومات الحساب')
    update_parser.add_argument('username', help='اسم المستخدم')
    update_parser.add_argument('--password', help='كلمة المرور الجديدة')
    update_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة المستهدفة الجديدة')
    update_parser.add_argument('--nickname', help='الاسم المستعار الجديد للحساب')
    update_parser.add_argument('--cookies', help='مسار ملف ملفات تعريف الارتباط الجديد')
    update_parser.add_argument('--user-agent', help='وكيل المستخدم الجديد')
    update_parser.add_argument('--mobile', dest='mobile', action='store_true', help='تفعيل محاكاة الأجهزة المحمولة')
    update_parser.add_argument('--no-mobile', dest='mobile', action='store_false', help='تعطيل محاكاة الأجهزة المحمولة')
    
    # أمر عرض حساب
    show_parser = subparsers.add_parser('show', help='عرض معلومات الحساب')
    show_parser.add_argument('username', help='اسم المستخدم')
    
    # أمر عرض جميع الحسابات
    list_parser = subparsers.add_parser('list', help='عرض جميع الحسابات')
    list_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='تصفية حسب الدولة')
    
    # أمر تعيين حالة الحساب
    status_parser = subparsers.add_parser('status', help='تعيين حالة الحساب')
    status_parser.add_argument('username', help='اسم المستخدم')
    status_parser.add_argument('status', choices=['active', 'inactive', 'suspended'], help='الحالة الجديدة')
    
    # أمر تعيين بروكسي للحساب
    proxy_parser = subparsers.add_parser('proxy', help='تعيين بروكسي للحساب')
    proxy_parser.add_argument('username', help='اسم المستخدم')
    
    # أمر استيراد الحسابات
    import_parser = subparsers.add_parser('import', help='استيراد الحسابات من ملف')
    import_parser.add_argument('file', help='مسار ملف الحسابات')
    
    # أمر تصدير الحسابات
    export_parser = subparsers.add_parser('export', help='تصدير الحسابات إلى ملف')
    export_parser.add_argument('file', help='مسار ملف الحسابات')
    
    args = parser.parse_args()
    
    # إنشاء مدير الحسابات
    account_manager = AccountManager()
    
    if args.command == 'add':
        cookies = None
        if args.cookies:
            try:
                with open(args.cookies, 'r') as f:
                    cookies = f.read()
            except Exception as e:
                print(f"خطأ في قراءة ملف ملفات تعريف الارتباط: {e}")
                return 1
                
        success = account_manager.add_account(
            args.username,
            args.password,
            args.country,
            args.nickname,
            cookies,
            args.user_agent,
            args.mobile
        )
        
        if success:
            print(f"تمت إضافة الحساب بنجاح: {args.username}")
        else:
            print(f"فشل في إضافة الحساب: {args.username}")
            return 1
    
    elif args.command == 'remove':
        success = account_manager.remove_account(args.username)
        
        if success:
            print(f"تمت إزالة الحساب بنجاح: {args.username}")
        else:
            print(f"فشل في إزالة الحساب: {args.username}")
            return 1
    
    elif args.command == 'update':
        update_data = {}
        
        if args.password:
            update_data['password'] = args.password
            
        if args.country:
            update_data['country_code'] = args.country
            
        if args.nickname:
            update_data['nickname'] = args.nickname
            
        if args.cookies:
            try:
                with open(args.cookies, 'r') as f:
                    update_data['cookies'] = f.read()
            except Exception as e:
                print(f"خطأ في قراءة ملف ملفات تعريف الارتباط: {e}")
                return 1
                
        if args.user_agent:
            update_data['user_agent'] = args.user_agent
            
        if args.mobile is not None:
            update_data['mobile'] = args.mobile
            
        if not update_data:
            print("لم يتم تحديد أي معلومات للتحديث")
            return 1
            
        success = account_manager.update_account(args.username, **update_data)
        
        if success:
            print(f"تم تحديث الحساب بنجاح: {args.username}")
        else:
            print(f"فشل في تحديث الحساب: {args.username}")
            return 1
    
    elif args.command == 'show':
        account = account_manager.get_account(args.username)
        
        if account:
            print(f"معلومات الحساب: {args.username}")
            print(json.dumps(account, ensure_ascii=False, indent=2))
        else:
            print(f"لم يتم العثور على الحساب: {args.username}")
            return 1
    
    elif args.command == 'list':
        if args.country:
            accounts = account_manager.get_accounts_by_country(args.country)
            print(f"الحسابات في الدولة {args.country}:")
        else:
            accounts = account_manager.get_all_accounts()
            print("جميع الحسابات:")
            
        if not accounts:
            print("  لا توجد حسابات")
        else:
            for username, account in accounts.items():
                status = account['status']
                country = account['country_code']
                nickname = account.get('nickname', '')
                last_login = account.get('last_login', 'لم يتم تسجيل الدخول بعد')
                
                print(f"  {username} ({nickname}) - الدولة: {country}, الحالة: {status}, آخر تسجيل دخول: {last_login}")
    
    elif args.command == 'status':
        success = account_manager.set_account_status(args.username, args.status)
        
        if success:
            print(f"تم تعيين حالة الحساب بنجاح: {args.username} -> {args.status}")
        else:
            print(f"فشل في تعيين حالة الحساب: {args.username}")
            return 1
    
    elif args.command == 'proxy':
        proxy = account_manager.assign_proxy_to_account(args.username)
        
        if proxy:
            print(f"تم تعيين البروكسي بنجاح للحساب {args.username}: {proxy}")
        else:
            print(f"فشل في تعيين البروكسي للحساب: {args.username}")
            return 1
    
    elif args.command == 'import':
        count = account_manager.import_accounts_from_file(args.file)
        
        if count > 0:
            print(f"تم استيراد {count} حساب بنجاح")
        else:
            print("لم يتم استيراد أي حساب")
            return 1
    
    elif args.command == 'export':
        success = account_manager.export_accounts_to_file(args.file)
        
        if success:
            print(f"تم تصدير الحسابات بنجاح إلى: {args.file}")
        else:
            print("فشل في تصدير الحسابات")
            return 1
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
