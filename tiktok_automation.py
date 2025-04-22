#!/usr/bin/env python3
"""
البرنامج الرئيسي لنظام أتمتة تيك توك
يوفر واجهة سطر أوامر للتحكم في جميع وظائف النظام
"""

import argparse
import sys
import os
import time
import logging
import json
from src.proxy.proxy_manager import ProxyManager
from src.account.account_manager import AccountManager
from src.account.tiktok_login import TikTokLogin
from src.mobile.mobile_simulator import MobileSimulator
from src.engagement.tiktok_engagement import TikTokEngagement
from src.scheduler.schedule_manager import ScheduleManager
from src.scheduler.post_executor import PostExecutor

# إعداد السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'logs', 'tiktok_automation.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('tiktok_automation')

def setup_directories():
    """إنشاء الدلائل اللازمة"""
    base_dir = os.path.dirname(__file__)
    dirs = ['logs', 'config', 'data', 'videos', 'cookies']
    
    for dir_name in dirs:
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def proxy_command(args):
    """تنفيذ أوامر البروكسي"""
    proxy_manager = ProxyManager()
    
    if args.proxy_action == 'add':
        success = proxy_manager.add_proxy(args.country, args.proxy)
        if success:
            print(f"تمت إضافة البروكسي بنجاح: {args.proxy} (الدولة: {args.country})")
        else:
            print(f"فشل في إضافة البروكسي: {args.proxy}")
            return 1
    
    elif args.proxy_action == 'remove':
        success = proxy_manager.remove_proxy(args.country, args.proxy)
        if success:
            print(f"تمت إزالة البروكسي بنجاح: {args.proxy} (الدولة: {args.country})")
        else:
            print(f"فشل في إزالة البروكسي: {args.proxy}")
            return 1
    
    elif args.proxy_action == 'list':
        if args.country:
            proxies = proxy_manager.get_proxies(args.country)
            print(f"البروكسيات للدولة {args.country}:")
            
            if not proxies:
                print("  لا توجد بروكسيات")
            else:
                for i, proxy in enumerate(proxies, 1):
                    print(f"  {i}. {proxy}")
        else:
            countries = ['saudi_arabia', 'uae', 'kuwait', 'egypt']
            for country in countries:
                proxies = proxy_manager.get_proxies(country)
                print(f"البروكسيات للدولة {country}:")
                
                if not proxies:
                    print("  لا توجد بروكسيات")
                else:
                    for i, proxy in enumerate(proxies, 1):
                        print(f"  {i}. {proxy}")
    
    elif args.proxy_action == 'test':
        if args.proxy:
            result = proxy_manager.test_proxy(args.proxy)
            if result['success']:
                print(f"البروكسي يعمل بشكل صحيح: {args.proxy}")
                print(f"الدولة: {result['country']}")
                print(f"عنوان IP: {result['ip']}")
            else:
                print(f"البروكسي لا يعمل: {args.proxy}")
                print(f"الخطأ: {result['error']}")
        else:
            if args.country:
                proxy = proxy_manager.get_random_proxy(args.country)
                if not proxy:
                    print(f"لم يتم العثور على بروكسي للدولة: {args.country}")
                    return 1
                
                result = proxy_manager.test_proxy(proxy)
                if result['success']:
                    print(f"البروكسي يعمل بشكل صحيح: {proxy}")
                    print(f"الدولة: {result['country']}")
                    print(f"عنوان IP: {result['ip']}")
                else:
                    print(f"البروكسي لا يعمل: {proxy}")
                    print(f"الخطأ: {result['error']}")
            else:
                print("يجب تحديد البروكسي أو الدولة")
                return 1
    
    return 0

def account_command(args):
    """تنفيذ أوامر الحسابات"""
    account_manager = AccountManager()
    
    if args.account_action == 'add':
        success = account_manager.add_account(
            args.username,
            args.password,
            args.country,
            args.proxy
        )
        
        if success:
            print(f"تمت إضافة الحساب بنجاح: {args.username}")
        else:
            print(f"فشل في إضافة الحساب: {args.username}")
            return 1
    
    elif args.account_action == 'remove':
        success = account_manager.remove_account(args.username)
        
        if success:
            print(f"تمت إزالة الحساب بنجاح: {args.username}")
        else:
            print(f"فشل في إزالة الحساب: {args.username}")
            return 1
    
    elif args.account_action == 'update':
        success = account_manager.update_account(
            args.username,
            args.password,
            args.country,
            args.proxy
        )
        
        if success:
            print(f"تم تحديث الحساب بنجاح: {args.username}")
        else:
            print(f"فشل في تحديث الحساب: {args.username}")
            return 1
    
    elif args.account_action == 'list':
        accounts = account_manager.get_all_accounts()
        
        if args.country:
            accounts = [account for account in accounts if account['country'] == args.country]
            print(f"الحسابات للدولة {args.country}:")
        else:
            print("جميع الحسابات:")
            
        if not accounts:
            print("  لا توجد حسابات")
        else:
            for account in accounts:
                print(f"  {account['username']} - الدولة: {account['country']}, البروكسي: {account['proxy'] or 'لا يوجد'}")
    
    elif args.account_action == 'test':
        login = TikTokLogin(account_manager)
        
        try:
            print(f"اختبار تسجيل الدخول للحساب: {args.username}")
            success = login.login(args.username)
            
            if success:
                print(f"تم تسجيل الدخول بنجاح: {args.username}")
                
                # الانتظار قبل تسجيل الخروج
                if args.wait > 0:
                    print(f"انتظار {args.wait} ثانية...")
                    time.sleep(args.wait)
            else:
                print(f"فشل في تسجيل الدخول: {args.username}")
                return 1
        finally:
            login.logout()
    
    return 0

def mobile_command(args):
    """تنفيذ أوامر محاكاة الأجهزة المحمولة"""
    mobile_simulator = MobileSimulator()
    
    if args.mobile_action == 'add':
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
    
    elif args.mobile_action == 'remove':
        success = mobile_simulator.remove_device(args.name)
        
        if success:
            print(f"تمت إزالة الجهاز بنجاح: {args.name}")
        else:
            print(f"فشل في إزالة الجهاز: {args.name}")
            return 1
    
    elif args.mobile_action == 'list':
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
    
    elif args.mobile_action == 'test':
        from src.mobile.test_mobile import main as test_mobile_main
        
        test_args = []
        
        if args.device:
            test_args.extend(['--device', args.device])
        
        if args.platform:
            test_args.extend(['--platform', args.platform])
        
        if args.proxy:
            test_args.extend(['--proxy', args.proxy])
        
        if args.country:
            test_args.extend(['--country', args.country])
        
        if args.wait:
            test_args.extend(['--wait', str(args.wait)])
        
        # تنفيذ اختبار محاكاة الأجهزة المحمولة
        sys.argv = ['test_mobile.py'] + test_args
        return test_mobile_main()
    
    return 0

def engagement_command(args):
    """تنفيذ أوامر التفاعل"""
    if args.engagement_action == 'test':
        from src.engagement.test_engagement import main as test_engagement_main
        
        test_args = [args.username]
        
        if args.video_url:
            test_args.extend(['--video-url', args.video_url])
        
        if args.profile_url:
            test_args.extend(['--profile-url', args.profile_url])
        
        if args.action:
            test_args.extend(['--action', args.action])
        
        if args.comment:
            test_args.extend(['--comment', args.comment])
        
        if args.comment_category:
            test_args.extend(['--comment-category', args.comment_category])
        
        if args.share_type:
            test_args.extend(['--share-type', args.share_type])
        
        if args.wait:
            test_args.extend(['--wait', str(args.wait)])
        
        if args.mobile:
            test_args.append('--mobile')
        
        # تنفيذ اختبار التفاعل
        sys.argv = ['test_engagement.py'] + test_args
        return test_engagement_main()
    
    elif args.engagement_action == 'comment':
        from src.engagement.manage_comments import main as manage_comments_main
        
        comment_args = [args.comment_action]
        
        if args.comment_action in ['add', 'remove', 'show']:
            comment_args.append(args.category)
        
        if args.comment_action in ['add', 'remove']:
            comment_args.append(args.comment)
        
        if args.comment_action == 'list' and args.category:
            comment_args.extend(['--category', args.category])
        
        # تنفيذ إدارة التعليقات
        sys.argv = ['manage_comments.py'] + comment_args
        return manage_comments_main()
    
    return 0

def schedule_command(args):
    """تنفيذ أوامر الجدولة"""
    schedule_manager = ScheduleManager()
    
    if args.schedule_action == 'add':
        success = schedule_manager.add_post(
            args.username,
            args.video_path,
            args.caption,
            args.schedule_time,
            args.tags
        )
        
        if success:
            print(f"تمت إضافة المنشور المجدول بنجاح: {args.video_path}")
        else:
            print(f"فشل في إضافة المنشور المجدول: {args.video_path}")
            return 1
    
    elif args.schedule_action == 'remove':
        success = schedule_manager.remove_post(args.post_id)
        
        if success:
            print(f"تمت إزالة المنشور المجدول بنجاح: {args.post_id}")
        else:
            print(f"فشل في إزالة المنشور المجدول: {args.post_id}")
            return 1
    
    elif args.schedule_action == 'list':
        if args.username:
            posts = schedule_manager.get_posts_by_username(args.username)
            print(f"المنشورات المجدولة للحساب {args.username}:")
        else:
            posts = schedule_manager.get_all_posts()
            print("جميع المنشورات المجدولة:")
            
        if not posts:
            print("  لا توجد منشورات مجدولة")
        else:
            for post in posts:
                print(f"  معرف: {post['id']}, الحساب: {post['username']}, الوقت: {post['schedule_time']}, الفيديو: {post['video_path']}")
    
    elif args.schedule_action == 'execute':
        post_executor = PostExecutor(schedule_manager, AccountManager())
        
        if args.post_id:
            print(f"تنفيذ المنشور المجدول: {args.post_id}")
            success = post_executor.execute_post(args.post_id)
            
            if success:
                print(f"تم تنفيذ المنشور المجدول بنجاح: {args.post_id}")
            else:
                print(f"فشل في تنفيذ المنشور المجدول: {args.post_id}")
                return 1
        else:
            print("تنفيذ جميع المنشورات المجدولة المستحقة")
            executed_posts = post_executor.execute_due_posts()
            
            if executed_posts:
                print(f"تم تنفيذ {len(executed_posts)} منشور مجدول بنجاح")
                for post_id in executed_posts:
                    print(f"  {post_id}")
            else:
                print("لا توجد منشورات مجدولة مستحقة")
    
    return 0

def run_command(args):
    """تنفيذ أمر التشغيل"""
    account_manager = AccountManager()
    schedule_manager = ScheduleManager()
    post_executor = PostExecutor(schedule_manager, account_manager)
    
    # التحقق من وجود الحساب
    if args.username:
        account = account_manager.get_account(args.username)
        if not account:
            print(f"الحساب غير موجود: {args.username}")
            return 1
    
    # تنفيذ المنشورات المجدولة
    if args.execute_posts:
        print("تنفيذ المنشورات المجدولة المستحقة")
        
        if args.username:
            executed_posts = post_executor.execute_due_posts_for_user(args.username)
        else:
            executed_posts = post_executor.execute_due_posts()
        
        if executed_posts:
            print(f"تم تنفيذ {len(executed_posts)} منشور مجدول بنجاح")
            for post_id in executed_posts:
                print(f"  {post_id}")
        else:
            print("لا توجد منشورات مجدولة مستحقة")
    
    # تنفيذ التفاعل العشوائي
    if args.random_engagement:
        if not args.username:
            print("يجب تحديد اسم المستخدم للتفاعل العشوائي")
            return 1
        
        print(f"تنفيذ التفاعل العشوائي للحساب: {args.username}")
        
        # تسجيل الدخول
        login = TikTokLogin(account_manager)
        
        try:
            success = login.login(args.username)
            
            if not success:
                print(f"فشل في تسجيل الدخول: {args.username}")
                return 1
            
            # إنشاء مكون التفاعل
            engagement = TikTokEngagement(login.driver)
            
            # تنفيذ التفاعل العشوائي
            for _ in range(args.engagement_count):
                # البحث عن فيديو عشوائي
                login.driver.get("https://www.tiktok.com/foryou")
                time.sleep(5)
                
                # تنفيذ التفاعل العشوائي
                results = engagement.perform_random_engagement()
                print(f"نتيجة التفاعل العشوائي: {results}")
                
                # الانتظار قبل التفاعل التالي
                time.sleep(args.engagement_interval)
        finally:
            login.logout()
    
    return 0

def main():
    """النقطة الرئيسية لتشغيل البرنامج"""
    # إنشاء الدلائل اللازمة
    setup_directories()
    
    # إنشاء محلل الأوامر
    parser = argparse.ArgumentParser(description='نظام أتمتة تيك توك')
    subparsers = parser.add_subparsers(dest='command', help='الأمر المراد تنفيذه')
    
    # أمر البروكسي
    proxy_parser = subparsers.add_parser('proxy', help='إدارة البروكسيات')
    proxy_subparsers = proxy_parser.add_subparsers(dest='proxy_action', help='إجراء البروكسي')
    
    # إضافة بروكسي
    proxy_add_parser = proxy_subparsers.add_parser('add', help='إضافة بروكسي')
    proxy_add_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    proxy_add_parser.add_argument('proxy', help='عنوان البروكسي')
    
    # إزالة بروكسي
    proxy_remove_parser = proxy_subparsers.add_parser('remove', help='إزالة بروكسي')
    proxy_remove_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    proxy_remove_parser.add_argument('proxy', help='عنوان البروكسي')
    
    # عرض البروكسيات
    proxy_list_parser = proxy_subparsers.add_parser('list', help='عرض البروكسيات')
    proxy_list_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    
    # اختبار البروكسي
    proxy_test_parser = proxy_subparsers.add_parser('test', help='اختبار البروكسي')
    proxy_test_parser.add_argument('--proxy', help='عنوان البروكسي')
    proxy_test_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    
    # أمر الحساب
    account_parser = subparsers.add_parser('account', help='إدارة الحسابات')
    account_subparsers = account_parser.add_subparsers(dest='account_action', help='إجراء الحساب')
    
    # إضافة حساب
    account_add_parser = account_subparsers.add_parser('add', help='إضافة حساب')
    account_add_parser.add_argument('username', help='اسم المستخدم')
    account_add_parser.add_argument('password', help='كلمة المرور')
    account_add_parser.add_argument('country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    account_add_parser.add_argument('--proxy', help='عنوان البروكسي')
    
    # إزالة حساب
    account_remove_parser = account_subparsers.add_parser('remove', help='إزالة حساب')
    account_remove_parser.add_argument('username', help='اسم المستخدم')
    
    # تحديث حساب
    account_update_parser = account_subparsers.add_parser('update', help='تحديث حساب')
    account_update_parser.add_argument('username', help='اسم المستخدم')
    account_update_parser.add_argument('--password', help='كلمة المرور')
    account_update_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    account_update_parser.add_argument('--proxy', help='عنوان البروكسي')
    
    # عرض الحسابات
    account_list_parser = account_subparsers.add_parser('list', help='عرض الحسابات')
    account_list_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    
    # اختبار الحساب
    account_test_parser = account_subparsers.add_parser('test', help='اختبار الحساب')
    account_test_parser.add_argument('username', help='اسم المستخدم')
    account_test_parser.add_argument('--wait', type=int, default=10, help='وقت الانتظار بالثواني')
    
    # أمر محاكاة الأجهزة المحمولة
    mobile_parser = subparsers.add_parser('mobile', help='إدارة محاكاة الأجهزة المحمولة')
    mobile_subparsers = mobile_parser.add_subparsers(dest='mobile_action', help='إجراء محاكاة الأجهزة المحمولة')
    
    # إضافة جهاز
    mobile_add_parser = mobile_subparsers.add_parser('add', help='إضافة جهاز')
    mobile_add_parser.add_argument('name', help='اسم الجهاز')
    mobile_add_parser.add_argument('user_agent', help='وكيل المستخدم')
    mobile_add_parser.add_argument('width', type=int, help='عرض الشاشة')
    mobile_add_parser.add_argument('height', type=int, help='ارتفاع الشاشة')
    mobile_add_parser.add_argument('pixel_ratio', type=float, help='نسبة البكسل')
    mobile_add_parser.add_argument('platform', choices=['iOS', 'Android'], help='منصة الجهاز')
    
    # إزالة جهاز
    mobile_remove_parser = mobile_subparsers.add_parser('remove', help='إزالة جهاز')
    mobile_remove_parser.add_argument('name', help='اسم الجهاز')
    
    # عرض الأجهزة
    mobile_list_parser = mobile_subparsers.add_parser('list', help='عرض الأجهزة')
    mobile_list_parser.add_argument('--platform', choices=['iOS', 'Android'], help='منصة الجهاز')
    
    # اختبار محاكاة الأجهزة المحمولة
    mobile_test_parser = mobile_subparsers.add_parser('test', help='اختبار محاكاة الأجهزة المحمولة')
    mobile_test_parser.add_argument('--device', help='اسم الجهاز')
    mobile_test_parser.add_argument('--platform', choices=['iOS', 'Android'], help='منصة الجهاز')
    mobile_test_parser.add_argument('--proxy', help='عنوان البروكسي')
    mobile_test_parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة')
    mobile_test_parser.add_argument('--wait', type=int, default=30, help='وقت الانتظار بالثواني')
    
    # أمر التفاعل
    engagement_parser = subparsers.add_parser('engagement', help='إدارة التفاعل')
    engagement_subparsers = engagement_parser.add_subparsers(dest='engagement_action', help='إجراء التفاعل')
    
    # اختبار التفاعل
    engagement_test_parser = engagement_subparsers.add_parser('test', help='اختبار التفاعل')
    engagement_test_parser.add_argument('username', help='اسم المستخدم')
    engagement_test_parser.add_argument('--video-url', help='رابط الفيديو')
    engagement_test_parser.add_argument('--profile-url', help='رابط الملف الشخصي')
    engagement_test_parser.add_argument('--action', choices=['like', 'comment', 'share', 'save', 'follow', 'random'], default='random', help='نوع التفاعل')
    engagement_test_parser.add_argument('--comment', help='نص التعليق')
    engagement_test_parser.add_argument('--comment-category', help='فئة التعليق العشوائي')
    engagement_test_parser.add_argument('--share-type', choices=['copy_link', 'facebook', 'twitter', 'whatsapp', 'telegram'], default='copy_link', help='نوع المشاركة')
    engagement_test_parser.add_argument('--wait', type=int, default=30, help='وقت الانتظار بالثواني')
    engagement_test_parser.add_argument('--mobile', action='store_true', help='استخدام محاكاة الأجهزة المحمولة')
    
    # إدارة التعليقات
    engagement_comment_parser = engagement_subparsers.add_parser('comment', help='إدارة التعليقات')
    engagement_comment_parser.add_argument('comment_action', choices=['add', 'remove', 'list', 'show', 'add-category'], help='إجراء التعليق')
    engagement_comment_parser.add_argument('category', nargs='?', help='فئة التعليق')
    engagement_comment_parser.add_argument('comment', nargs='?', help='نص التعليق')
    
    # أمر الجدولة
    schedule_parser = subparsers.add_parser('schedule', help='إدارة الجدولة')
    schedule_subparsers = schedule_parser.add_subparsers(dest='schedule_action', help='إجراء الجدولة')
    
    # إضافة منشور مجدول
    schedule_add_parser = schedule_subparsers.add_parser('add', help='إضافة منشور مجدول')
    schedule_add_parser.add_argument('username', help='اسم المستخدم')
    schedule_add_parser.add_argument('video_path', help='مسار الفيديو')
    schedule_add_parser.add_argument('caption', help='وصف الفيديو')
    schedule_add_parser.add_argument('schedule_time', help='وقت الجدولة (YYYY-MM-DD HH:MM:SS)')
    schedule_add_parser.add_argument('--tags', help='الوسوم (مفصولة بفواصل)')
    
    # إزالة منشور مجدول
    schedule_remove_parser = schedule_subparsers.add_parser('remove', help='إزالة منشور مجدول')
    schedule_remove_parser.add_argument('post_id', help='معرف المنشور')
    
    # عرض المنشورات المجدولة
    schedule_list_parser = schedule_subparsers.add_parser('list', help='عرض المنشورات المجدولة')
    schedule_list_parser.add_argument('--username', help='اسم المستخدم')
    
    # تنفيذ المنشورات المجدولة
    schedule_execute_parser = schedule_subparsers.add_parser('execute', help='تنفيذ المنشورات المجدولة')
    schedule_execute_parser.add_argument('--post-id', help='معرف المنشور')
    
    # أمر التشغيل
    run_parser = subparsers.add_parser('run', help='تشغيل النظام')
    run_parser.add_argument('--username', help='اسم المستخدم')
    run_parser.add_argument('--execute-posts', action='store_true', help='تنفيذ المنشورات المجدولة')
    run_parser.add_argument('--random-engagement', action='store_true', help='تنفيذ التفاعل العشوائي')
    run_parser.add_argument('--engagement-count', type=int, default=5, help='عدد التفاعلات العشوائية')
    run_parser.add_argument('--engagement-interval', type=int, default=60, help='الفاصل الزمني بين التفاعلات بالثواني')
    
    # تحليل الأوامر
    args = parser.parse_args()
    
    # تنفيذ الأمر المناسب
    if args.command == 'proxy':
        if args.proxy_action:
            return proxy_command(args)
        else:
            proxy_parser.print_help()
    
    elif args.command == 'account':
        if args.account_action:
            return account_command(args)
        else:
            account_parser.print_help()
    
    elif args.command == 'mobile':
        if args.mobile_action:
            return mobile_command(args)
        else:
            mobile_parser.print_help()
    
    elif args.command == 'engagement':
        if args.engagement_action:
            return engagement_command(args)
        else:
            engagement_parser.print_help()
    
    elif args.command == 'schedule':
        if args.schedule_action:
            return schedule_command(args)
        else:
            schedule_parser.print_help()
    
    elif args.command == 'run':
        return run_command(args)
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
