"""
وحدة اختبار التفاعل مع تيك توك
توفر وظائف لاختبار التفاعل مع المحتوى على تيك توك
"""

import argparse
import sys
import os
import time
import random
from src.engagement.tiktok_engagement import TikTokEngagement
from src.account.tiktok_login import TikTokLogin
from src.account.account_manager import AccountManager
from src.mobile.mobile_simulator import MobileSimulator

def main():
    """
    النقطة الرئيسية لتشغيل اختبار التفاعل مع تيك توك
    """
    parser = argparse.ArgumentParser(description='اختبار التفاعل مع المحتوى على تيك توك')
    parser.add_argument('username', help='اسم المستخدم')
    parser.add_argument('--video-url', help='رابط الفيديو')
    parser.add_argument('--profile-url', help='رابط الملف الشخصي')
    parser.add_argument('--action', choices=['like', 'comment', 'share', 'save', 'follow', 'random'], default='random', help='نوع التفاعل')
    parser.add_argument('--comment', help='نص التعليق')
    parser.add_argument('--comment-category', help='فئة التعليق العشوائي')
    parser.add_argument('--share-type', choices=['copy_link', 'facebook', 'twitter', 'whatsapp', 'telegram'], default='copy_link', help='نوع المشاركة')
    parser.add_argument('--wait', type=int, default=30, help='وقت الانتظار بالثواني قبل إغلاق المتصفح')
    parser.add_argument('--mobile', action='store_true', help='استخدام محاكاة الأجهزة المحمولة')
    
    args = parser.parse_args()
    
    # إنشاء مدير الحسابات
    account_manager = AccountManager()
    
    # التحقق من وجود الحساب
    account = account_manager.get_account(args.username)
    if not account:
        print(f"الحساب غير موجود: {args.username}")
        return 1
    
    # إنشاء مكون تسجيل الدخول
    login = TikTokLogin(account_manager)
    
    # إنشاء محاكي الأجهزة المحمولة إذا كان مطلوبًا
    if args.mobile:
        mobile_simulator = MobileSimulator()
        device = mobile_simulator.get_random_device()
        print(f"استخدام جهاز محمول: {device['name']}")
    
    try:
        # تسجيل الدخول
        print(f"تسجيل الدخول باستخدام الحساب: {args.username}")
        success = login.login(args.username)
        
        if not success:
            print(f"فشل في تسجيل الدخول: {args.username}")
            return 1
        
        # إنشاء مكون التفاعل
        engagement = TikTokEngagement(login.driver)
        
        # الانتقال إلى صفحة الفيديو أو الملف الشخصي
        if args.video_url:
            print(f"الانتقال إلى صفحة الفيديو: {args.video_url}")
            login.driver.get(args.video_url)
            time.sleep(5)
        elif args.profile_url:
            print(f"الانتقال إلى صفحة الملف الشخصي: {args.profile_url}")
            login.driver.get(args.profile_url)
            time.sleep(5)
        
        # تنفيذ التفاعل
        if args.action == 'like':
            print("تنفيذ الإعجاب بالفيديو...")
            success = engagement.like_video()
            print(f"نتيجة الإعجاب: {'نجاح' if success else 'فشل'}")
        
        elif args.action == 'comment':
            print("تنفيذ التعليق على الفيديو...")
            success = engagement.comment_on_video(args.comment, category=args.comment_category)
            print(f"نتيجة التعليق: {'نجاح' if success else 'فشل'}")
        
        elif args.action == 'share':
            print(f"تنفيذ مشاركة الفيديو ({args.share_type})...")
            success = engagement.share_video(share_type=args.share_type)
            print(f"نتيجة المشاركة: {'نجاح' if success else 'فشل'}")
        
        elif args.action == 'save':
            print("تنفيذ حفظ الفيديو...")
            success = engagement.save_video()
            print(f"نتيجة الحفظ: {'نجاح' if success else 'فشل'}")
        
        elif args.action == 'follow':
            print("تنفيذ متابعة المستخدم...")
            success = engagement.follow_user()
            print(f"نتيجة المتابعة: {'نجاح' if success else 'فشل'}")
        
        elif args.action == 'random':
            print("تنفيذ تفاعل عشوائي...")
            results = engagement.perform_random_engagement()
            print(f"نتيجة التفاعل العشوائي: {results}")
        
        # تحديث إحصائيات الحساب
        if args.action == 'like':
            account_manager.update_account_stats(args.username, 'likes')
        elif args.action == 'comment':
            account_manager.update_account_stats(args.username, 'comments')
        elif args.action == 'share':
            account_manager.update_account_stats(args.username, 'shares')
        elif args.action == 'save':
            account_manager.update_account_stats(args.username, 'saves')
        
        # الانتظار قبل إغلاق المتصفح
        if args.wait > 0:
            print(f"انتظار {args.wait} ثانية قبل إغلاق المتصفح...")
            time.sleep(args.wait)
        
        return 0
    except Exception as e:
        print(f"خطأ في اختبار التفاعل: {e}")
        return 1
    finally:
        # تسجيل الخروج
        login.logout()

if __name__ == "__main__":
    sys.exit(main())
