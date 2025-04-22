"""
وحدة إدارة ملفات التعليقات
توفر واجهة سطر أوامر لإدارة التعليقات المستخدمة في التفاعل مع تيك توك
"""

import argparse
import sys
import os
import json
from src.engagement.tiktok_engagement import TikTokEngagement

def main():
    """
    النقطة الرئيسية لتشغيل إدارة ملفات التعليقات
    """
    parser = argparse.ArgumentParser(description='إدارة التعليقات المستخدمة في التفاعل مع تيك توك')
    subparsers = parser.add_subparsers(dest='command', help='الأمر المراد تنفيذه')
    
    # أمر إضافة تعليق
    add_parser = subparsers.add_parser('add', help='إضافة تعليق جديد')
    add_parser.add_argument('category', help='فئة التعليق')
    add_parser.add_argument('comment', help='نص التعليق')
    
    # أمر إزالة تعليق
    remove_parser = subparsers.add_parser('remove', help='إزالة تعليق')
    remove_parser.add_argument('category', help='فئة التعليق')
    remove_parser.add_argument('comment', help='نص التعليق')
    
    # أمر عرض التعليقات
    list_parser = subparsers.add_parser('list', help='عرض التعليقات')
    list_parser.add_argument('--category', help='فئة التعليق')
    
    # أمر إضافة فئة
    add_category_parser = subparsers.add_parser('add-category', help='إضافة فئة جديدة')
    add_category_parser.add_argument('category', help='اسم الفئة')
    
    args = parser.parse_args()
    
    # إنشاء مكون التفاعل
    engagement = TikTokEngagement()
    
    if args.command == 'add':
        success = engagement.add_comment(args.category, args.comment)
        
        if success:
            print(f"تمت إضافة التعليق بنجاح: {args.comment} (الفئة: {args.category})")
        else:
            print(f"فشل في إضافة التعليق: {args.comment}")
            return 1
    
    elif args.command == 'remove':
        success = engagement.remove_comment(args.category, args.comment)
        
        if success:
            print(f"تمت إزالة التعليق بنجاح: {args.comment} (الفئة: {args.category})")
        else:
            print(f"فشل في إزالة التعليق: {args.comment}")
            return 1
    
    elif args.command == 'list':
        if args.category:
            comments = engagement.get_comments(args.category)
            print(f"التعليقات في الفئة {args.category}:")
            
            if not comments:
                print("  لا توجد تعليقات")
            else:
                for i, comment in enumerate(comments, 1):
                    print(f"  {i}. {comment}")
        else:
            comments = engagement.get_comments()
            print("جميع التعليقات:")
            
            if not comments:
                print("  لا توجد تعليقات")
            else:
                for category, category_comments in comments.items():
                    print(f"الفئة: {category}")
                    for i, comment in enumerate(category_comments, 1):
                        print(f"  {i}. {comment}")
    
    elif args.command == 'add-category':
        comments = engagement.get_comments()
        
        if args.category in comments:
            print(f"الفئة موجودة بالفعل: {args.category}")
            return 1
        
        success = engagement.add_comment(args.category, "تعليق تجريبي")
        if success:
            success = engagement.remove_comment(args.category, "تعليق تجريبي")
            
            if success:
                print(f"تمت إضافة الفئة بنجاح: {args.category}")
            else:
                print(f"فشل في إضافة الفئة: {args.category}")
                return 1
        else:
            print(f"فشل في إضافة الفئة: {args.category}")
            return 1
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
