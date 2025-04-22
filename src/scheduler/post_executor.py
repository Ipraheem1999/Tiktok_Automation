"""
وحدة تنفيذ المنشورات المجدولة
توفر وظائف لتنفيذ المنشورات المجدولة على تيك توك
"""

import os
import time
import logging
import datetime
from src.scheduler.schedule_manager import ScheduleManager
from src.account.tiktok_login import TikTokLogin
from src.account.account_manager import AccountManager

class PostExecutor:
    """منفذ المنشورات المجدولة"""
    
    def __init__(self):
        """تهيئة منفذ المنشورات"""
        # إنشاء مدير الجدولة
        self.schedule_manager = ScheduleManager()
        
        # إنشاء مدير الحسابات
        self.account_manager = AccountManager()
        
        # إعداد السجل
        self.logger = logging.getLogger('post_executor')
        self.logger.setLevel(logging.INFO)
        
        # إضافة معالج للسجل
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'post_executor.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def start(self):
        """
        بدء تنفيذ المنشورات المجدولة
        
        العوائد:
            bool: True إذا تم بدء التنفيذ بنجاح، False خلاف ذلك
        """
        # بدء تشغيل المجدول
        if not self.schedule_manager.start_scheduler():
            self.logger.error("فشل في بدء تشغيل المجدول")
            return False
        
        self.logger.info("تم بدء تنفيذ المنشورات المجدولة")
        
        # معالجة صف المهام
        self.schedule_manager.process_task_queue(self.execute_post)
        
        return True
    
    def stop(self):
        """
        إيقاف تنفيذ المنشورات المجدولة
        
        العوائد:
            bool: True إذا تم إيقاف التنفيذ بنجاح، False خلاف ذلك
        """
        # إيقاف تشغيل المجدول
        if not self.schedule_manager.stop_scheduler():
            self.logger.error("فشل في إيقاف تشغيل المجدول")
            return False
        
        self.logger.info("تم إيقاف تنفيذ المنشورات المجدولة")
        
        return True
    
    def execute_post(self, post):
        """
        تنفيذ المنشور
        
        المعلمات:
            post (dict): المنشور
            
        العوائد:
            dict: نتيجة التنفيذ
        """
        self.logger.info(f"بدء تنفيذ المنشور: {post['id']}")
        
        result = {
            'success': False,
            'message': '',
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        try:
            # التحقق من وجود الحساب
            username = post['username']
            account = self.account_manager.get_account(username)
            
            if not account:
                result['message'] = f"الحساب غير موجود: {username}"
                self.logger.error(result['message'])
                return result
            
            # التحقق من وجود الفيديو
            video_path = post['video_path']
            if not os.path.exists(video_path):
                result['message'] = f"الفيديو غير موجود: {video_path}"
                self.logger.error(result['message'])
                return result
            
            # إنشاء مكون تسجيل الدخول
            login = TikTokLogin(self.account_manager)
            
            try:
                # تسجيل الدخول
                if not login.login(username):
                    result['message'] = f"فشل في تسجيل الدخول: {username}"
                    self.logger.error(result['message'])
                    return result
                
                # تحميل الفيديو
                if self._upload_video(login, post):
                    result['success'] = True
                    result['message'] = "تم تحميل الفيديو بنجاح"
                    
                    # تحديث إحصائيات الحساب
                    self.account_manager.update_account_stats(username, 'posts')
                else:
                    result['message'] = "فشل في تحميل الفيديو"
            finally:
                # تسجيل الخروج
                login.logout()
        except Exception as e:
            result['message'] = f"خطأ في تنفيذ المنشور: {str(e)}"
            self.logger.error(result['message'], exc_info=True)
        
        self.logger.info(f"انتهاء تنفيذ المنشور: {post['id']}, النتيجة: {result['success']}")
        
        return result
    
    def _upload_video(self, login, post):
        """
        تحميل الفيديو إلى تيك توك
        
        المعلمات:
            login (TikTokLogin): مكون تسجيل الدخول
            post (dict): المنشور
            
        العوائد:
            bool: True إذا تم التحميل بنجاح، False خلاف ذلك
        """
        try:
            # الانتقال إلى صفحة التحميل
            login.driver.get('https://www.tiktok.com/upload')
            time.sleep(5)
            
            # انتظار ظهور زر التحميل
            upload_button = login.driver.find_element_by_xpath("//input[@type='file']")
            
            # تحميل الفيديو
            upload_button.send_keys(post['video_path'])
            time.sleep(10)
            
            # إدخال الوصف
            description = post['description']
            
            # إضافة الوسوم
            if post['tags']:
                for tag in post['tags']:
                    if not tag.startswith('#'):
                        tag = f"#{tag}"
                    description += f" {tag}"
            
            # إضافة المستخدمين المذكورين
            if post['mentions']:
                for mention in post['mentions']:
                    if not mention.startswith('@'):
                        mention = f"@{mention}"
                    description += f" {mention}"
            
            # إدخال الوصف
            description_input = login.driver.find_element_by_xpath("//div[@contenteditable='true']")
            description_input.clear()
            login._type_like_human(description_input, description)
            
            # النقر على زر النشر
            post_button = login.driver.find_element_by_xpath("//button[contains(text(), 'Post')]")
            post_button.click()
            
            # انتظار اكتمال التحميل
            time.sleep(30)
            
            # التحقق من نجاح التحميل
            success_message = login.driver.find_elements_by_xpath("//div[contains(text(), 'Your video is being uploaded to TikTok!')]")
            
            return len(success_message) > 0
        except Exception as e:
            self.logger.error(f"خطأ في تحميل الفيديو: {str(e)}", exc_info=True)
            return False
