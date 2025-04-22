"""
وحدة اختبار تسجيل الدخول إلى تيك توك
توفر واجهة سطر أوامر لاختبار تسجيل الدخول إلى حسابات تيك توك
"""

import argparse
import sys
import os
import time
from src.account.account_manager import AccountManager
from src.account.tiktok_login import TikTokLogin

def main():
    """
    النقطة الرئيسية لتشغيل اختبار تسجيل الدخول
    """
    parser = argparse.ArgumentParser(description='اختبار تسجيل الدخول إلى حسابات تيك توك')
    parser.add_argument('username', help='اسم المستخدم')
    parser.add_argument('--password', help='كلمة المرور (اختياري إذا كان الحساب موجودًا بالفعل)')
    parser.add_argument('--cookies', help='مسار ملف ملفات تعريف الارتباط')
    parser.add_argument('--wait', type=int, default=30, help='وقت الانتظار بالثواني قبل إغلاق المتصفح')
    
    args = parser.parse_args()
    
    # إنشاء مدير الحسابات
    account_manager = AccountManager()
    
    # التحقق من وجود الحساب
    account = account_manager.get_account(args.username)
    if not account and not args.password:
        print(f"الحساب غير موجود: {args.username}")
        print("يجب تحديد كلمة المرور لإضافة حساب جديد")
        return 1
    
    # إنشاء مكون تسجيل الدخول
    login = TikTokLogin(account_manager)
    
    try:
        # تسجيل الدخول
        success = login.login(args.username, args.password, args.cookies)
        
        if success:
            print(f"تم تسجيل الدخول بنجاح: {args.username}")
            
            # الانتظار قبل إغلاق المتصفح
            if args.wait > 0:
                print(f"انتظار {args.wait} ثانية قبل إغلاق المتصفح...")
                time.sleep(args.wait)
            
            # تسجيل الخروج
            login.logout()
            return 0
        else:
            print(f"فشل في تسجيل الدخول: {args.username}")
            return 1
    except Exception as e:
        print(f"خطأ في تسجيل الدخول: {e}")
        return 1
    finally:
        # التأكد من إغلاق المتصفح
        login.close()

if __name__ == "__main__":
    sys.exit(main())
