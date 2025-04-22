"""
وحدة جدولة المنشورات
توفر وظائف لجدولة المنشورات على تيك توك
"""

import os
import json
import time
import datetime
import threading
import queue
import logging
from src.account.account_manager import AccountManager

class ScheduleManager:
    """مدير جدولة المنشورات"""
    
    def __init__(self, config_dir=None):
        """
        تهيئة مدير الجدولة
        
        المعلمات:
            config_dir (str, optional): مسار دليل التكوين. إذا كان None، سيتم استخدام المسار الافتراضي
        """
        if config_dir is None:
            self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        else:
            self.config_dir = config_dir
            
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.schedule_file = os.path.join(self.config_dir, 'schedule.json')
        self.schedule = {
            'posts': [],
            'settings': {
                'enabled': True,
                'check_interval': 60,  # بالثواني
                'max_posts_per_day': 10,
                'time_slots': [
                    {'start': '08:00', 'end': '10:00'},
                    {'start': '12:00', 'end': '14:00'},
                    {'start': '18:00', 'end': '20:00'},
                    {'start': '21:00', 'end': '23:00'}
                ]
            }
        }
        
        # إنشاء مدير الحسابات
        self.account_manager = AccountManager()
        
        # تحميل الجدولة
        self._load_schedule()
        
        # إعداد السجل
        self.logger = logging.getLogger('schedule_manager')
        self.logger.setLevel(logging.INFO)
        
        # إضافة معالج للسجل
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'schedule.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
        # إنشاء صف المهام
        self.task_queue = queue.Queue()
        
        # إنشاء قفل للتزامن
        self.lock = threading.Lock()
        
        # إنشاء حدث للإيقاف
        self.stop_event = threading.Event()
    
    def _load_schedule(self):
        """تحميل الجدولة من الملف"""
        if not os.path.exists(self.schedule_file):
            self._save_schedule()
            return
            
        try:
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                self.schedule = json.load(f)
        except Exception as e:
            print(f"خطأ في تحميل الجدولة: {e}")
    
    def _save_schedule(self):
        """حفظ الجدولة إلى الملف"""
        try:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedule, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ الجدولة: {e}")
    
    def add_post(self, username, video_path, description, schedule_time=None, tags=None, mentions=None):
        """
        إضافة منشور إلى الجدولة
        
        المعلمات:
            username (str): اسم المستخدم
            video_path (str): مسار الفيديو
            description (str): وصف المنشور
            schedule_time (str, optional): وقت الجدولة بتنسيق ISO (YYYY-MM-DDTHH:MM:SS)
            tags (list, optional): قائمة الوسوم
            mentions (list, optional): قائمة المستخدمين المذكورين
            
        العوائد:
            str: معرف المنشور أو None إذا فشلت الإضافة
        """
        # التحقق من وجود الحساب
        account = self.account_manager.get_account(username)
        if not account:
            print(f"الحساب غير موجود: {username}")
            return None
        
        # التحقق من وجود الفيديو
        if not os.path.exists(video_path):
            print(f"الفيديو غير موجود: {video_path}")
            return None
        
        # إنشاء معرف فريد للمنشور
        post_id = f"post_{int(time.time())}_{os.path.basename(video_path)}"
        
        # إنشاء المنشور
        post = {
            'id': post_id,
            'username': username,
            'video_path': video_path,
            'description': description,
            'tags': tags or [],
            'mentions': mentions or [],
            'created_at': datetime.datetime.now().isoformat(),
            'schedule_time': schedule_time,
            'status': 'pending',
            'attempts': 0,
            'last_attempt': None,
            'result': None
        }
        
        # إضافة المنشور إلى الجدولة
        with self.lock:
            self.schedule['posts'].append(post)
            self._save_schedule()
        
        self.logger.info(f"تمت إضافة منشور جديد: {post_id}")
        
        return post_id
    
    def remove_post(self, post_id):
        """
        إزالة منشور من الجدولة
        
        المعلمات:
            post_id (str): معرف المنشور
            
        العوائد:
            bool: True إذا تمت الإزالة بنجاح، False خلاف ذلك
        """
        with self.lock:
            for i, post in enumerate(self.schedule['posts']):
                if post['id'] == post_id:
                    del self.schedule['posts'][i]
                    self._save_schedule()
                    self.logger.info(f"تمت إزالة المنشور: {post_id}")
                    return True
        
        return False
    
    def update_post(self, post_id, **kwargs):
        """
        تحديث منشور في الجدولة
        
        المعلمات:
            post_id (str): معرف المنشور
            **kwargs: المعلومات المراد تحديثها
            
        العوائد:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        with self.lock:
            for post in self.schedule['posts']:
                if post['id'] == post_id:
                    for key, value in kwargs.items():
                        if key in post:
                            post[key] = value
                    
                    self._save_schedule()
                    self.logger.info(f"تم تحديث المنشور: {post_id}")
                    return True
        
        return False
    
    def get_post(self, post_id):
        """
        الحصول على منشور من الجدولة
        
        المعلمات:
            post_id (str): معرف المنشور
            
        العوائد:
            dict: المنشور أو None إذا لم يتم العثور على المنشور
        """
        with self.lock:
            for post in self.schedule['posts']:
                if post['id'] == post_id:
                    return post.copy()
        
        return None
    
    def get_all_posts(self):
        """
        الحصول على جميع المنشورات
        
        العوائد:
            list: قائمة المنشورات
        """
        with self.lock:
            return [post.copy() for post in self.schedule['posts']]
    
    def get_pending_posts(self):
        """
        الحصول على المنشورات المعلقة
        
        العوائد:
            list: قائمة المنشورات المعلقة
        """
        with self.lock:
            return [post.copy() for post in self.schedule['posts'] if post['status'] == 'pending']
    
    def get_posts_by_username(self, username):
        """
        الحصول على المنشورات حسب اسم المستخدم
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            list: قائمة المنشورات
        """
        with self.lock:
            return [post.copy() for post in self.schedule['posts'] if post['username'] == username]
    
    def get_posts_by_status(self, status):
        """
        الحصول على المنشورات حسب الحالة
        
        المعلمات:
            status (str): الحالة (pending, processing, completed, failed)
            
        العوائد:
            list: قائمة المنشورات
        """
        with self.lock:
            return [post.copy() for post in self.schedule['posts'] if post['status'] == status]
    
    def update_settings(self, **kwargs):
        """
        تحديث إعدادات الجدولة
        
        المعلمات:
            **kwargs: الإعدادات المراد تحديثها
            
        العوائد:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        with self.lock:
            for key, value in kwargs.items():
                if key in self.schedule['settings']:
                    self.schedule['settings'][key] = value
            
            self._save_schedule()
            self.logger.info(f"تم تحديث إعدادات الجدولة: {kwargs}")
            return True
    
    def get_settings(self):
        """
        الحصول على إعدادات الجدولة
        
        العوائد:
            dict: إعدادات الجدولة
        """
        with self.lock:
            return self.schedule['settings'].copy()
    
    def is_in_time_slot(self, time_str=None):
        """
        التحقق مما إذا كان الوقت الحالي ضمن فترة زمنية مسموح بها
        
        المعلمات:
            time_str (str, optional): الوقت بتنسيق HH:MM. إذا كان None، سيتم استخدام الوقت الحالي
            
        العوائد:
            bool: True إذا كان الوقت ضمن فترة زمنية مسموح بها، False خلاف ذلك
        """
        if not self.schedule['settings']['time_slots']:
            return True
        
        if time_str:
            current_time = datetime.datetime.strptime(time_str, '%H:%M').time()
        else:
            current_time = datetime.datetime.now().time()
        
        for slot in self.schedule['settings']['time_slots']:
            start_time = datetime.datetime.strptime(slot['start'], '%H:%M').time()
            end_time = datetime.datetime.strptime(slot['end'], '%H:%M').time()
            
            if start_time <= current_time <= end_time:
                return True
        
        return False
    
    def get_next_post_time(self):
        """
        الحصول على الوقت المناسب للمنشور التالي
        
        العوائد:
            str: الوقت بتنسيق ISO (YYYY-MM-DDTHH:MM:SS) أو None إذا لم يتم العثور على وقت مناسب
        """
        if not self.schedule['settings']['time_slots']:
            return datetime.datetime.now().isoformat()
        
        current_time = datetime.datetime.now()
        current_date = current_time.date()
        
        # التحقق من عدد المنشورات اليوم
        today_posts = [
            post for post in self.schedule['posts']
            if post['status'] in ['completed', 'processing']
            and post['last_attempt']
            and datetime.datetime.fromisoformat(post['last_attempt']).date() == current_date
        ]
        
        if len(today_posts) >= self.schedule['settings']['max_posts_per_day']:
            # تجاوز الحد الأقصى للمنشورات اليومية، الانتقال إلى اليوم التالي
            current_date = current_date + datetime.timedelta(days=1)
            current_time = datetime.datetime.combine(current_date, datetime.time(0, 0))
        
        # البحث عن الفترة الزمنية المناسبة التالية
        for _ in range(7):  # البحث لمدة أسبوع كحد أقصى
            for slot in self.schedule['settings']['time_slots']:
                start_time = datetime.datetime.strptime(slot['start'], '%H:%M').time()
                end_time = datetime.datetime.strptime(slot['end'], '%H:%M').time()
                
                slot_start = datetime.datetime.combine(current_date, start_time)
                slot_end = datetime.datetime.combine(current_date, end_time)
                
                if current_time < slot_start:
                    # الفترة الزمنية لم تبدأ بعد
                    middle_time = slot_start + (slot_end - slot_start) / 2
                    return middle_time.isoformat()
                elif current_time < slot_end:
                    # الفترة الزمنية الحالية
                    return current_time.isoformat()
            
            # الانتقال إلى اليوم التالي
            current_date = current_date + datetime.timedelta(days=1)
            current_time = datetime.datetime.combine(current_date, datetime.time(0, 0))
        
        return None
    
    def start_scheduler(self):
        """
        بدء تشغيل المجدول
        
        العوائد:
            bool: True إذا تم بدء التشغيل بنجاح، False خلاف ذلك
        """
        if not self.schedule['settings']['enabled']:
            self.logger.warning("المجدول معطل")
            return False
        
        self.stop_event.clear()
        
        # إنشاء مؤشر ترابط للمجدول
        scheduler_thread = threading.Thread(target=self._scheduler_loop)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        self.logger.info("تم بدء تشغيل المجدول")
        
        return True
    
    def stop_scheduler(self):
        """
        إيقاف تشغيل المجدول
        
        العوائد:
            bool: True إذا تم إيقاف التشغيل بنجاح، False خلاف ذلك
        """
        self.stop_event.set()
        self.logger.info("تم إيقاف تشغيل المجدول")
        
        return True
    
    def _scheduler_loop(self):
        """حلقة المجدول"""
        self.logger.info("بدء حلقة المجدول")
        
        while not self.stop_event.is_set():
            try:
                # التحقق من المنشورات المجدولة
                self._check_scheduled_posts()
                
                # الانتظار للفحص التالي
                self.stop_event.wait(self.schedule['settings']['check_interval'])
            except Exception as e:
                self.logger.error(f"خطأ في حلقة المجدول: {e}")
                # الانتظار قبل المحاولة مرة أخرى
                self.stop_event.wait(60)
        
        self.logger.info("انتهاء حلقة المجدول")
    
    def _check_scheduled_posts(self):
        """التحقق من المنشورات المجدولة"""
        current_time = datetime.datetime.now()
        
        with self.lock:
            for post in self.schedule['posts']:
                if post['status'] != 'pending':
                    continue
                
                if post['schedule_time']:
                    # التحقق من وقت الجدولة
                    schedule_time = datetime.datetime.fromisoformat(post['schedule_time'])
                    
                    if current_time >= schedule_time:
                        # حان وقت النشر
                        self._process_post(post)
                elif self.is_in_time_slot():
                    # التحقق من الفترة الزمنية المسموح بها
                    self._process_post(post)
    
    def _process_post(self, post):
        """
        معالجة المنشور
        
        المعلمات:
            post (dict): المنشور
        """
        # تحديث حالة المنشور
        post['status'] = 'processing'
        post['last_attempt'] = datetime.datetime.now().isoformat()
        post['attempts'] += 1
        
        self._save_schedule()
        
        # إضافة المنشور إلى صف المهام
        self.task_queue.put(post)
        
        self.logger.info(f"تمت إضافة المنشور إلى صف المهام: {post['id']}")
    
    def process_task_queue(self, callback):
        """
        معالجة صف المهام
        
        المعلمات:
            callback (function): دالة رد الاتصال لمعالجة المنشور
        """
        while not self.task_queue.empty():
            try:
                # الحصول على المنشور من صف المهام
                post = self.task_queue.get(block=False)
                
                # معالجة المنشور
                result = callback(post)
                
                # تحديث نتيجة المنشور
                with self.lock:
                    for p in self.schedule['posts']:
                        if p['id'] == post['id']:
                            p['status'] = 'completed' if result['success'] else 'failed'
                            p['result'] = result
                            break
                    
                    self._save_schedule()
                
                self.logger.info(f"تمت معالجة المنشور: {post['id']}, النتيجة: {result['success']}")
                
                # إشعار صف المهام بانتهاء المعالجة
                self.task_queue.task_done()
            except queue.Empty:
                break
            except Exception as e:
                self.logger.error(f"خطأ في معالجة صف المهام: {e}")
                break
