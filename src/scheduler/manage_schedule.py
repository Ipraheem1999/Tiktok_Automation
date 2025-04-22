"""
وحدة إدارة ملفات الجدولة
توفر واجهة سطر أوامر لإدارة جدولة المنشورات على تيك توك
"""

import argparse
import sys
import os
import json
import datetime
from src.scheduler.schedule_manager import ScheduleManager

def main():
    """
    النقطة الرئيسية لتشغيل إدارة ملفات الجدولة
    """
    parser = argparse.ArgumentParser(description='إدارة جدولة المنشورات على تيك توك')
    subparsers = parser.add_subparsers(dest='command', help='الأمر المراد تنفيذه')
    
    # أمر إضافة منشور
    add_parser = subparsers.add_parser('add', help='إضافة منشور جديد')
    add_parser.add_argument('username', help='اسم المستخدم')
    add_parser.add_argument('video', help='مسار الفيديو')
    add_parser.add_argument('description', help='وصف المنشور')
    add_parser.add_argument('--schedule', help='وقت الجدولة بتنسيق YYYY-MM-DDTHH:MM:SS')
    add_parser.add_argument('--tags', nargs='+', help='قائمة الوسوم')
    add_parser.add_argument('--mentions', nargs='+', help='قائمة المستخدمين المذكورين')
    
    # أمر إزالة منشور
    remove_parser = subparsers.add_parser('remove', help='إزالة منشور')
    remove_parser.add_argument('post_id', help='معرف المنشور')
    
    # أمر تحديث منشور
    update_parser = subparsers.add_parser('update', help='تحديث معلومات المنشور')
    update_parser.add_argument('post_id', help='معرف المنشور')
    update_parser.add_argument('--description', help='وصف المنشور الجديد')
    update_parser.add_argument('--schedule', help='وقت الجدولة الجديد بتنسيق YYYY-MM-DDTHH:MM:SS')
    update_parser.add_argument('--tags', nargs='+', help='قائمة الوسوم الجديدة')
    update_parser.add_argument('--mentions', nargs='+', help='قائمة المستخدمين المذكورين الجديدة')
    update_parser.add_argument('--status', choices=['pending', 'processing', 'completed', 'failed'], help='الحالة الجديدة')
    
    # أمر عرض منشور
    show_parser = subparsers.add_parser('show', help='عرض معلومات المنشور')
    show_parser.add_argument('post_id', help='معرف المنشور')
    
    # أمر عرض جميع المنشورات
    list_parser = subparsers.add_parser('list', help='عرض جميع المنشورات')
    list_parser.add_argument('--username', help='تصفية حسب اسم المستخدم')
    list_parser.add_argument('--status', choices=['pending', 'processing', 'completed', 'failed'], help='تصفية حسب الحالة')
    
    # أمر تحديث إعدادات الجدولة
    settings_parser = subparsers.add_parser('settings', help='تحديث إعدادات الجدولة')
    settings_parser.add_argument('--enabled', type=lambda x: x.lower() == 'true', help='تفعيل/تعطيل المجدول')
    settings_parser.add_argument('--check-interval', type=int, help='فترة الفحص بالثواني')
    settings_parser.add_argument('--max-posts-per-day', type=int, help='الحد الأقصى للمنشورات اليومية')
    
    # أمر إدارة الفترات الزمنية
    time_slots_parser = subparsers.add_parser('time-slots', help='إدارة الفترات الزمنية')
    time_slots_subparsers = time_slots_parser.add_subparsers(dest='time_slots_command', help='الأمر المراد تنفيذه')
    
    # أمر إضافة فترة زمنية
    add_slot_parser = time_slots_subparsers.add_parser('add', help='إضافة فترة زمنية')
    add_slot_parser.add_argument('start', help='وقت البداية بتنسيق HH:MM')
    add_slot_parser.add_argument('end', help='وقت النهاية بتنسيق HH:MM')
    
    # أمر إزالة فترة زمنية
    remove_slot_parser = time_slots_subparsers.add_parser('remove', help='إزالة فترة زمنية')
    remove_slot_parser.add_argument('index', type=int, help='رقم الفترة الزمنية')
    
    # أمر عرض الفترات الزمنية
    list_slots_parser = time_slots_subparsers.add_parser('list', help='عرض الفترات الزمنية')
    
    # أمر الحصول على الوقت المناسب للمنشور التالي
    next_time_parser = subparsers.add_parser('next-time', help='الحصول على الوقت المناسب للمنشور التالي')
    
    args = parser.parse_args()
    
    # إنشاء مدير الجدولة
    schedule_manager = ScheduleManager()
    
    if args.command == 'add':
        post_id = schedule_manager.add_post(
            args.username,
            args.video,
            args.description,
            args.schedule,
            args.tags,
            args.mentions
        )
        
        if post_id:
            print(f"تمت إضافة المنشور بنجاح: {post_id}")
        else:
            print("فشل في إضافة المنشور")
            return 1
    
    elif args.command == 'remove':
        success = schedule_manager.remove_post(args.post_id)
        
        if success:
            print(f"تمت إزالة المنشور بنجاح: {args.post_id}")
        else:
            print(f"فشل في إزالة المنشور: {args.post_id}")
            return 1
    
    elif args.command == 'update':
        update_data = {}
        
        if args.description:
            update_data['description'] = args.description
            
        if args.schedule:
            update_data['schedule_time'] = args.schedule
            
        if args.tags:
            update_data['tags'] = args.tags
            
        if args.mentions:
            update_data['mentions'] = args.mentions
            
        if args.status:
            update_data['status'] = args.status
            
        if not update_data:
            print("لم يتم تحديد أي معلومات للتحديث")
            return 1
            
        success = schedule_manager.update_post(args.post_id, **update_data)
        
        if success:
            print(f"تم تحديث المنشور بنجاح: {args.post_id}")
        else:
            print(f"فشل في تحديث المنشور: {args.post_id}")
            return 1
    
    elif args.command == 'show':
        post = schedule_manager.get_post(args.post_id)
        
        if post:
            print(f"معلومات المنشور: {args.post_id}")
            print(json.dumps(post, ensure_ascii=False, indent=2))
        else:
            print(f"لم يتم العثور على المنشور: {args.post_id}")
            return 1
    
    elif args.command == 'list':
        if args.username:
            posts = schedule_manager.get_posts_by_username(args.username)
            print(f"المنشورات للمستخدم {args.username}:")
        elif args.status:
            posts = schedule_manager.get_posts_by_status(args.status)
            print(f"المنشورات بحالة {args.status}:")
        else:
            posts = schedule_manager.get_all_posts()
            print("جميع المنشورات:")
            
        if not posts:
            print("  لا توجد منشورات")
        else:
            for post in posts:
                status = post['status']
                username = post['username']
                schedule_time = post['schedule_time'] or 'غير مجدول'
                
                print(f"  {post['id']} - المستخدم: {username}, الحالة: {status}, الجدولة: {schedule_time}")
    
    elif args.command == 'settings':
        update_data = {}
        
        if args.enabled is not None:
            update_data['enabled'] = args.enabled
            
        if args.check_interval:
            update_data['check_interval'] = args.check_interval
            
        if args.max_posts_per_day:
            update_data['max_posts_per_day'] = args.max_posts_per_day
            
        if update_data:
            success = schedule_manager.update_settings(**update_data)
            
            if success:
                print("تم تحديث إعدادات الجدولة بنجاح")
            else:
                print("فشل في تحديث إعدادات الجدولة")
                return 1
        
        # عرض الإعدادات الحالية
        settings = schedule_manager.get_settings()
        print("إعدادات الجدولة الحالية:")
        print(json.dumps(settings, ensure_ascii=False, indent=2))
    
    elif args.command == 'time-slots':
        settings = schedule_manager.get_settings()
        
        if args.time_slots_command == 'add':
            try:
                # التحقق من صحة تنسيق الوقت
                start_time = datetime.datetime.strptime(args.start, '%H:%M').time()
                end_time = datetime.datetime.strptime(args.end, '%H:%M').time()
                
                if start_time >= end_time:
                    print("خطأ: وقت البداية يجب أن يكون قبل وقت النهاية")
                    return 1
                
                # إضافة الفترة الزمنية
                settings['time_slots'].append({
                    'start': args.start,
                    'end': args.end
                })
                
                success = schedule_manager.update_settings(time_slots=settings['time_slots'])
                
                if success:
                    print(f"تمت إضافة الفترة الزمنية بنجاح: {args.start} - {args.end}")
                else:
                    print("فشل في إضافة الفترة الزمنية")
                    return 1
            except ValueError:
                print("خطأ: تنسيق الوقت غير صحيح. يجب أن يكون بتنسيق HH:MM")
                return 1
        
        elif args.time_slots_command == 'remove':
            if args.index < 0 or args.index >= len(settings['time_slots']):
                print(f"خطأ: رقم الفترة الزمنية غير صحيح. يجب أن يكون بين 0 و {len(settings['time_slots']) - 1}")
                return 1
            
            removed_slot = settings['time_slots'].pop(args.index)
            
            success = schedule_manager.update_settings(time_slots=settings['time_slots'])
            
            if success:
                print(f"تمت إزالة الفترة الزمنية بنجاح: {removed_slot['start']} - {removed_slot['end']}")
            else:
                print("فشل في إزالة الفترة الزمنية")
                return 1
        
        elif args.time_slots_command == 'list' or not args.time_slots_command:
            print("الفترات الزمنية الحالية:")
            
            if not settings['time_slots']:
                print("  لا توجد فترات زمنية")
            else:
                for i, slot in enumerate(settings['time_slots']):
                    print(f"  {i}: {slot['start']} - {slot['end']}")
        
        else:
            time_slots_parser.print_help()
    
    elif args.command == 'next-time':
        next_time = schedule_manager.get_next_post_time()
        
        if next_time:
            print(f"الوقت المناسب للمنشور التالي: {next_time}")
        else:
            print("لم يتم العثور على وقت مناسب للمنشور التالي")
            return 1
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
