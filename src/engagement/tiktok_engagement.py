"""
وحدة التفاعل مع تيك توك
توفر وظائف للتفاعل مع المحتوى على تيك توك (الإعجاب، التعليق، المشاركة، الحفظ)
"""

import os
import time
import random
import logging
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

class TikTokEngagement:
    """مكون التفاعل مع تيك توك"""
    
    def __init__(self, driver=None):
        """
        تهيئة مكون التفاعل
        
        المعلمات:
            driver (webdriver, optional): متصفح Selenium
        """
        self.driver = driver
        
        # إعداد السجل
        self.logger = logging.getLogger('tiktok_engagement')
        self.logger.setLevel(logging.INFO)
        
        # إضافة معالج للسجل
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'engagement.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
        # تحميل التعليقات العشوائية
        self.comments_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'comments.json')
        self._load_comments()
    
    def _load_comments(self):
        """تحميل التعليقات العشوائية"""
        if not os.path.exists(self.comments_file):
            # إنشاء ملف التعليقات العشوائية
            comments = {
                "general": [
                    "رائع! 👏",
                    "أحب هذا المحتوى 😍",
                    "محتوى مميز 🔥",
                    "استمر في النشر 👍",
                    "أعجبني كثيرًا ❤️",
                    "محتوى رائع كالعادة",
                    "شكرًا على المشاركة",
                    "تستحق المتابعة 👌",
                    "من أفضل ما رأيت اليوم",
                    "أبدعت! 🌟"
                ],
                "funny": [
                    "هههههه 😂",
                    "أضحكتني كثيرًا 🤣",
                    "لم أضحك هكذا منذ فترة طويلة",
                    "نكتة رائعة 😆",
                    "استمر في نشر المحتوى المضحك"
                ],
                "food": [
                    "يبدو لذيذًا جدًا 😋",
                    "أريد تجربة هذه الوصفة",
                    "شهيتني للطعام 🍔",
                    "وصفة رائعة سأجربها",
                    "طعام يفتح النفس 👨‍🍳"
                ],
                "travel": [
                    "مكان جميل جدًا 🏝️",
                    "أتمنى زيارة هذا المكان",
                    "صور رائعة للسفر ✈️",
                    "أين هذا المكان الجميل؟",
                    "أضفت هذا المكان لقائمة أماكن السفر الخاصة بي"
                ],
                "music": [
                    "أغنية رائعة 🎵",
                    "صوت جميل جدًا 🎤",
                    "أحب هذه الأغنية",
                    "موسيقى تريح الأعصاب 🎶",
                    "أداء مميز"
                ],
                "dance": [
                    "رقصة رائعة 💃",
                    "حركات مميزة",
                    "أداء احترافي في الرقص",
                    "رقصة جميلة جدًا 🕺",
                    "أعجبتني الكوريوغرافيا"
                ]
            }
            
            with open(self.comments_file, 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=2)
            
            self.comments = comments
        else:
            with open(self.comments_file, 'r', encoding='utf-8') as f:
                self.comments = json.load(f)
    
    def set_driver(self, driver):
        """
        تعيين متصفح Selenium
        
        المعلمات:
            driver (webdriver): متصفح Selenium
        """
        self.driver = driver
    
    def _wait_and_find_element(self, by, value, timeout=10):
        """
        انتظار وإيجاد عنصر
        
        المعلمات:
            by (By): طريقة البحث
            value (str): قيمة البحث
            timeout (int, optional): مهلة الانتظار بالثواني
            
        العوائد:
            WebElement: العنصر أو None إذا لم يتم العثور على العنصر
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"لم يتم العثور على العنصر: {by}={value}")
            return None
    
    def _wait_and_find_elements(self, by, value, timeout=10):
        """
        انتظار وإيجاد عناصر
        
        المعلمات:
            by (By): طريقة البحث
            value (str): قيمة البحث
            timeout (int, optional): مهلة الانتظار بالثواني
            
        العوائد:
            list: قائمة العناصر أو قائمة فارغة إذا لم يتم العثور على عناصر
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            self.logger.warning(f"لم يتم العثور على عناصر: {by}={value}")
            return []
    
    def _random_wait(self, min_seconds=1, max_seconds=3):
        """
        انتظار عشوائي
        
        المعلمات:
            min_seconds (float, optional): الحد الأدنى للانتظار بالثواني
            max_seconds (float, optional): الحد الأقصى للانتظار بالثواني
        """
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def like_video(self, video_url=None):
        """
        الإعجاب بفيديو
        
        المعلمات:
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            bool: True إذا تم الإعجاب بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # البحث عن زر الإعجاب
            like_button = None
            
            # محاولة العثور على زر الإعجاب باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//span[contains(@data-e2e, 'like-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'like-icon')]"),
                (By.XPATH, "//span[contains(@class, 'like-icon')]"),
                (By.XPATH, "//div[contains(@class, 'like-icon')]")
            ]
            
            for by, selector in selectors:
                like_button = self._wait_and_find_element(by, selector)
                if like_button:
                    break
            
            if not like_button:
                self.logger.error("لم يتم العثور على زر الإعجاب")
                return False
            
            # التحقق مما إذا كان تم الإعجاب بالفعل
            is_liked = "active" in like_button.get_attribute("class") or "filled" in like_button.get_attribute("class")
            
            if is_liked:
                self.logger.info("تم الإعجاب بالفيديو بالفعل")
                return True
            
            # النقر على زر الإعجاب
            like_button.click()
            self._random_wait()
            
            self.logger.info("تم الإعجاب بالفيديو بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في الإعجاب بالفيديو: {str(e)}")
            return False
    
    def unlike_video(self, video_url=None):
        """
        إلغاء الإعجاب بفيديو
        
        المعلمات:
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            bool: True إذا تم إلغاء الإعجاب بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # البحث عن زر الإعجاب
            like_button = None
            
            # محاولة العثور على زر الإعجاب باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//span[contains(@data-e2e, 'like-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'like-icon')]"),
                (By.XPATH, "//span[contains(@class, 'like-icon')]"),
                (By.XPATH, "//div[contains(@class, 'like-icon')]")
            ]
            
            for by, selector in selectors:
                like_button = self._wait_and_find_element(by, selector)
                if like_button:
                    break
            
            if not like_button:
                self.logger.error("لم يتم العثور على زر الإعجاب")
                return False
            
            # التحقق مما إذا كان تم الإعجاب بالفعل
            is_liked = "active" in like_button.get_attribute("class") or "filled" in like_button.get_attribute("class")
            
            if not is_liked:
                self.logger.info("لم يتم الإعجاب بالفيديو بالفعل")
                return True
            
            # النقر على زر الإعجاب لإلغاء الإعجاب
            like_button.click()
            self._random_wait()
            
            self.logger.info("تم إلغاء الإعجاب بالفيديو بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إلغاء الإعجاب بالفيديو: {str(e)}")
            return False
    
    def comment_on_video(self, comment=None, video_url=None, category=None):
        """
        التعليق على فيديو
        
        المعلمات:
            comment (str, optional): نص التعليق. إذا كان None، سيتم استخدام تعليق عشوائي
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            category (str, optional): فئة التعليق العشوائي
            
        العوائد:
            bool: True إذا تم التعليق بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # اختيار تعليق عشوائي إذا لم يتم تحديد تعليق
            if not comment:
                if category and category in self.comments:
                    comment = random.choice(self.comments[category])
                else:
                    comment = random.choice(self.comments["general"])
            
            # البحث عن زر التعليق
            comment_button = None
            
            # محاولة العثور على زر التعليق باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//span[contains(@data-e2e, 'comment-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'comment-icon')]"),
                (By.XPATH, "//span[contains(@class, 'comment-icon')]"),
                (By.XPATH, "//div[contains(@class, 'comment-icon')]")
            ]
            
            for by, selector in selectors:
                comment_button = self._wait_and_find_element(by, selector)
                if comment_button:
                    break
            
            if not comment_button:
                self.logger.error("لم يتم العثور على زر التعليق")
                return False
            
            # النقر على زر التعليق
            comment_button.click()
            self._random_wait()
            
            # البحث عن حقل التعليق
            comment_input = None
            
            # محاولة العثور على حقل التعليق باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//div[contains(@data-e2e, 'comment-input')]"),
                (By.XPATH, "//div[contains(@class, 'comment-input')]"),
                (By.XPATH, "//div[contains(@placeholder, 'Add comment')]"),
                (By.XPATH, "//div[contains(@contenteditable, 'true')]")
            ]
            
            for by, selector in selectors:
                comment_input = self._wait_and_find_element(by, selector)
                if comment_input:
                    break
            
            if not comment_input:
                self.logger.error("لم يتم العثور على حقل التعليق")
                return False
            
            # إدخال التعليق
            comment_input.clear()
            
            # إدخال التعليق حرفًا بحرف
            for char in comment:
                comment_input.send_keys(char)
                self._random_wait(0.05, 0.15)
            
            self._random_wait()
            
            # البحث عن زر النشر
            post_button = None
            
            # محاولة العثور على زر النشر باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//button[contains(text(), 'Post')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'comment-post')]"),
                (By.XPATH, "//button[contains(@class, 'post-button')]")
            ]
            
            for by, selector in selectors:
                post_button = self._wait_and_find_element(by, selector)
                if post_button:
                    break
            
            if not post_button:
                self.logger.error("لم يتم العثور على زر النشر")
                return False
            
            # النقر على زر النشر
            post_button.click()
            self._random_wait(2, 4)
            
            self.logger.info(f"تم التعليق على الفيديو بنجاح: {comment}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في التعليق على الفيديو: {str(e)}")
            return False
    
    def share_video(self, video_url=None, share_type="copy_link"):
        """
        مشاركة فيديو
        
        المعلمات:
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            share_type (str, optional): نوع المشاركة (copy_link, facebook, twitter, whatsapp, telegram)
            
        العوائد:
            bool: True إذا تمت المشاركة بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # البحث عن زر المشاركة
            share_button = None
            
            # محاولة العثور على زر المشاركة باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//span[contains(@data-e2e, 'share-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'share-icon')]"),
                (By.XPATH, "//span[contains(@class, 'share-icon')]"),
                (By.XPATH, "//div[contains(@class, 'share-icon')]")
            ]
            
            for by, selector in selectors:
                share_button = self._wait_and_find_element(by, selector)
                if share_button:
                    break
            
            if not share_button:
                self.logger.error("لم يتم العثور على زر المشاركة")
                return False
            
            # النقر على زر المشاركة
            share_button.click()
            self._random_wait()
            
            # اختيار نوع المشاركة
            share_option = None
            
            if share_type == "copy_link":
                # البحث عن خيار نسخ الرابط
                selectors = [
                    (By.XPATH, "//div[contains(text(), 'Copy link')]"),
                    (By.XPATH, "//span[contains(text(), 'Copy link')]")
                ]
            elif share_type == "facebook":
                # البحث عن خيار مشاركة على فيسبوك
                selectors = [
                    (By.XPATH, "//div[contains(text(), 'Facebook')]"),
                    (By.XPATH, "//span[contains(text(), 'Facebook')]")
                ]
            elif share_type == "twitter":
                # البحث عن خيار مشاركة على تويتر
                selectors = [
                    (By.XPATH, "//div[contains(text(), 'Twitter')]"),
                    (By.XPATH, "//span[contains(text(), 'Twitter')]")
                ]
            elif share_type == "whatsapp":
                # البحث عن خيار مشاركة على واتساب
                selectors = [
                    (By.XPATH, "//div[contains(text(), 'WhatsApp')]"),
                    (By.XPATH, "//span[contains(text(), 'WhatsApp')]")
                ]
            elif share_type == "telegram":
                # البحث عن خيار مشاركة على تيليجرام
                selectors = [
                    (By.XPATH, "//div[contains(text(), 'Telegram')]"),
                    (By.XPATH, "//span[contains(text(), 'Telegram')]")
                ]
            else:
                # البحث عن خيار نسخ الرابط كخيار افتراضي
                selectors = [
                    (By.XPATH, "//div[contains(text(), 'Copy link')]"),
                    (By.XPATH, "//span[contains(text(), 'Copy link')]")
                ]
            
            for by, selector in selectors:
                share_option = self._wait_and_find_element(by, selector)
                if share_option:
                    break
            
            if not share_option:
                self.logger.error(f"لم يتم العثور على خيار المشاركة: {share_type}")
                return False
            
            # النقر على خيار المشاركة
            share_option.click()
            self._random_wait(2, 4)
            
            self.logger.info(f"تمت مشاركة الفيديو بنجاح: {share_type}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في مشاركة الفيديو: {str(e)}")
            return False
    
    def save_video(self, video_url=None):
        """
        حفظ فيديو
        
        المعلمات:
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            bool: True إذا تم الحفظ بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # البحث عن زر الحفظ
            save_button = None
            
            # محاولة العثور على زر الحفظ باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//span[contains(@data-e2e, 'save-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'save-icon')]"),
                (By.XPATH, "//span[contains(@class, 'save-icon')]"),
                (By.XPATH, "//div[contains(@class, 'save-icon')]"),
                (By.XPATH, "//span[contains(@data-e2e, 'bookmark-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'bookmark-icon')]")
            ]
            
            for by, selector in selectors:
                save_button = self._wait_and_find_element(by, selector)
                if save_button:
                    break
            
            if not save_button:
                self.logger.error("لم يتم العثور على زر الحفظ")
                return False
            
            # التحقق مما إذا كان تم الحفظ بالفعل
            is_saved = "active" in save_button.get_attribute("class") or "filled" in save_button.get_attribute("class")
            
            if is_saved:
                self.logger.info("تم حفظ الفيديو بالفعل")
                return True
            
            # النقر على زر الحفظ
            save_button.click()
            self._random_wait()
            
            self.logger.info("تم حفظ الفيديو بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الفيديو: {str(e)}")
            return False
    
    def unsave_video(self, video_url=None):
        """
        إلغاء حفظ فيديو
        
        المعلمات:
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            bool: True إذا تم إلغاء الحفظ بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # البحث عن زر الحفظ
            save_button = None
            
            # محاولة العثور على زر الحفظ باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//span[contains(@data-e2e, 'save-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'save-icon')]"),
                (By.XPATH, "//span[contains(@class, 'save-icon')]"),
                (By.XPATH, "//div[contains(@class, 'save-icon')]"),
                (By.XPATH, "//span[contains(@data-e2e, 'bookmark-icon')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'bookmark-icon')]")
            ]
            
            for by, selector in selectors:
                save_button = self._wait_and_find_element(by, selector)
                if save_button:
                    break
            
            if not save_button:
                self.logger.error("لم يتم العثور على زر الحفظ")
                return False
            
            # التحقق مما إذا كان تم الحفظ بالفعل
            is_saved = "active" in save_button.get_attribute("class") or "filled" in save_button.get_attribute("class")
            
            if not is_saved:
                self.logger.info("لم يتم حفظ الفيديو بالفعل")
                return True
            
            # النقر على زر الحفظ لإلغاء الحفظ
            save_button.click()
            self._random_wait()
            
            self.logger.info("تم إلغاء حفظ الفيديو بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إلغاء حفظ الفيديو: {str(e)}")
            return False
    
    def follow_user(self, username=None, profile_url=None):
        """
        متابعة مستخدم
        
        المعلمات:
            username (str, optional): اسم المستخدم
            profile_url (str, optional): رابط الملف الشخصي. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            bool: True إذا تمت المتابعة بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الملف الشخصي إذا تم تحديد رابط
            if profile_url:
                self.driver.get(profile_url)
                self._random_wait(3, 5)
            elif username:
                self.driver.get(f"https://www.tiktok.com/@{username}")
                self._random_wait(3, 5)
            
            # البحث عن زر المتابعة
            follow_button = None
            
            # محاولة العثور على زر المتابعة باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//button[contains(text(), 'Follow')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'follow-button')]"),
                (By.XPATH, "//button[contains(@class, 'follow-button')]")
            ]
            
            for by, selector in selectors:
                follow_button = self._wait_and_find_element(by, selector)
                if follow_button:
                    break
            
            if not follow_button:
                self.logger.error("لم يتم العثور على زر المتابعة")
                return False
            
            # التحقق مما إذا كان تم المتابعة بالفعل
            is_following = "Following" in follow_button.text or "Unfollow" in follow_button.text
            
            if is_following:
                self.logger.info("تمت متابعة المستخدم بالفعل")
                return True
            
            # النقر على زر المتابعة
            follow_button.click()
            self._random_wait()
            
            self.logger.info(f"تمت متابعة المستخدم بنجاح: {username or profile_url}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في متابعة المستخدم: {str(e)}")
            return False
    
    def unfollow_user(self, username=None, profile_url=None):
        """
        إلغاء متابعة مستخدم
        
        المعلمات:
            username (str, optional): اسم المستخدم
            profile_url (str, optional): رابط الملف الشخصي. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            bool: True إذا تم إلغاء المتابعة بنجاح، False خلاف ذلك
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return False
        
        try:
            # الانتقال إلى صفحة الملف الشخصي إذا تم تحديد رابط
            if profile_url:
                self.driver.get(profile_url)
                self._random_wait(3, 5)
            elif username:
                self.driver.get(f"https://www.tiktok.com/@{username}")
                self._random_wait(3, 5)
            
            # البحث عن زر المتابعة
            follow_button = None
            
            # محاولة العثور على زر المتابعة باستخدام عدة طرق
            selectors = [
                (By.XPATH, "//button[contains(text(), 'Following')]"),
                (By.XPATH, "//button[contains(text(), 'Unfollow')]"),
                (By.XPATH, "//button[contains(@data-e2e, 'follow-button')]"),
                (By.XPATH, "//button[contains(@class, 'follow-button')]")
            ]
            
            for by, selector in selectors:
                follow_button = self._wait_and_find_element(by, selector)
                if follow_button:
                    break
            
            if not follow_button:
                self.logger.error("لم يتم العثور على زر المتابعة")
                return False
            
            # التحقق مما إذا كان تم المتابعة بالفعل
            is_following = "Following" in follow_button.text or "Unfollow" in follow_button.text
            
            if not is_following:
                self.logger.info("لم تتم متابعة المستخدم بالفعل")
                return True
            
            # النقر على زر المتابعة لإلغاء المتابعة
            follow_button.click()
            self._random_wait()
            
            # تأكيد إلغاء المتابعة إذا ظهر مربع حوار
            confirm_button = self._wait_and_find_element(By.XPATH, "//button[contains(text(), 'Unfollow')]", 3)
            if confirm_button:
                confirm_button.click()
                self._random_wait()
            
            self.logger.info(f"تم إلغاء متابعة المستخدم بنجاح: {username or profile_url}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إلغاء متابعة المستخدم: {str(e)}")
            return False
    
    def perform_random_engagement(self, video_url=None):
        """
        تنفيذ تفاعل عشوائي
        
        المعلمات:
            video_url (str, optional): رابط الفيديو. إذا كان None، سيتم استخدام الصفحة الحالية
            
        العوائد:
            dict: نتائج التفاعل
        """
        if not self.driver:
            self.logger.error("لم يتم تعيين متصفح Selenium")
            return {"success": False, "actions": []}
        
        try:
            # الانتقال إلى صفحة الفيديو إذا تم تحديد رابط
            if video_url:
                self.driver.get(video_url)
                self._random_wait(3, 5)
            
            # تحديد الإجراءات العشوائية
            actions = []
            results = {"success": True, "actions": []}
            
            # الإعجاب بالفيديو (احتمالية 80%)
            if random.random() < 0.8:
                like_result = self.like_video()
                actions.append({"action": "like", "success": like_result})
            
            # التعليق على الفيديو (احتمالية 30%)
            if random.random() < 0.3:
                comment_result = self.comment_on_video()
                actions.append({"action": "comment", "success": comment_result})
            
            # مشاركة الفيديو (احتمالية 20%)
            if random.random() < 0.2:
                share_result = self.share_video()
                actions.append({"action": "share", "success": share_result})
            
            # حفظ الفيديو (احتمالية 40%)
            if random.random() < 0.4:
                save_result = self.save_video()
                actions.append({"action": "save", "success": save_result})
            
            # متابعة المستخدم (احتمالية 10%)
            if random.random() < 0.1:
                follow_result = self.follow_user()
                actions.append({"action": "follow", "success": follow_result})
            
            results["actions"] = actions
            
            self.logger.info(f"تم تنفيذ تفاعل عشوائي: {actions}")
            return results
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ تفاعل عشوائي: {str(e)}")
            return {"success": False, "actions": []}
    
    def add_comment(self, category, comment):
        """
        إضافة تعليق إلى قائمة التعليقات
        
        المعلمات:
            category (str): فئة التعليق
            comment (str): نص التعليق
            
        العوائد:
            bool: True إذا تمت الإضافة بنجاح، False خلاف ذلك
        """
        try:
            if category not in self.comments:
                self.comments[category] = []
            
            self.comments[category].append(comment)
            
            with open(self.comments_file, 'w', encoding='utf-8') as f:
                json.dump(self.comments, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إضافة تعليق: {str(e)}")
            return False
    
    def remove_comment(self, category, comment):
        """
        إزالة تعليق من قائمة التعليقات
        
        المعلمات:
            category (str): فئة التعليق
            comment (str): نص التعليق
            
        العوائد:
            bool: True إذا تمت الإزالة بنجاح، False خلاف ذلك
        """
        try:
            if category not in self.comments:
                return False
            
            if comment not in self.comments[category]:
                return False
            
            self.comments[category].remove(comment)
            
            with open(self.comments_file, 'w', encoding='utf-8') as f:
                json.dump(self.comments, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إزالة تعليق: {str(e)}")
            return False
    
    def get_comments(self, category=None):
        """
        الحصول على التعليقات
        
        المعلمات:
            category (str, optional): فئة التعليق
            
        العوائد:
            dict or list: التعليقات
        """
        if category:
            if category in self.comments:
                return self.comments[category]
            return []
        
        return self.comments
