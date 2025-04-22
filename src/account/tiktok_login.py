"""
وحدة تسجيل الدخول إلى تيك توك
توفر وظائف لتسجيل الدخول إلى حسابات تيك توك باستخدام Selenium
"""

import os
import time
import random
import json
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

from src.account.account_manager import AccountManager
from src.proxy.proxy_manager import ProxyManager
from src.utils.config import TIKTOK_URL, TIKTOK_LOGIN_URL, MOBILE_USER_AGENTS, BROWSER_SETTINGS

class TikTokLogin:
    """مكون تسجيل الدخول إلى تيك توك"""
    
    def __init__(self, account_manager=None, proxy_manager=None):
        """
        تهيئة مكون تسجيل الدخول
        
        المعلمات:
            account_manager (AccountManager, optional): مدير الحسابات
            proxy_manager (ProxyManager, optional): مدير البروكسي
        """
        self.account_manager = account_manager or AccountManager()
        self.proxy_manager = proxy_manager or ProxyManager()
        self.driver = None
        self.current_username = None
    
    def _setup_driver(self, username):
        """
        إعداد متصفح Selenium
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            webdriver: متصفح Selenium أو None إذا فشل الإعداد
        """
        account = self.account_manager.get_account(username)
        if not account:
            print(f"لم يتم العثور على الحساب: {username}")
            return None
        
        # الحصول على بروكسي للحساب
        proxy = self.account_manager.get_account_proxy(username)
        
        # إعداد خيارات Chrome
        options = uc.ChromeOptions()
        
        # إضافة إعدادات المتصفح
        if BROWSER_SETTINGS['headless']:
            options.add_argument('--headless')
            
        options.add_argument(f'--window-size={BROWSER_SETTINGS["window_size"]}')
        
        if BROWSER_SETTINGS['disable_gpu']:
            options.add_argument('--disable-gpu')
            
        if BROWSER_SETTINGS['no_sandbox']:
            options.add_argument('--no-sandbox')
            
        if BROWSER_SETTINGS['disable_dev_shm_usage']:
            options.add_argument('--disable-dev-shm-usage')
        
        # إعداد وكيل المستخدم للأجهزة المحمولة إذا كان مطلوبًا
        if account['mobile']:
            user_agent = account.get('user_agent')
            if not user_agent:
                user_agent = random.choice(MOBILE_USER_AGENTS)
                self.account_manager.update_account(username, user_agent=user_agent)
                
            options.add_argument(f'--user-agent={user_agent}')
            
            # إضافة إعدادات محاكاة الجوال
            mobile_emulation = {
                "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
                "userAgent": user_agent
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # إعداد البروكسي إذا كان متاحًا
        if proxy:
            if self.proxy_manager.test_proxy(proxy):
                options = self.proxy_manager.configure_webdriver_proxy(options)
            else:
                print(f"البروكسي غير صالح للحساب {username}: {proxy}")
        
        # إنشاء دليل لتخزين ملفات تعريف الارتباط
        cookies_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cookies')
        os.makedirs(cookies_dir, exist_ok=True)
        
        # إنشاء دليل لبيانات المستخدم
        user_data_dir = os.path.join(BROWSER_SETTINGS['user_data_dir'], username)
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f'--user-data-dir={user_data_dir}')
        
        try:
            # إنشاء متصفح Selenium
            driver = uc.Chrome(options=options)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            print(f"خطأ في إعداد متصفح Selenium: {e}")
            return None
    
    def login(self, username, password=None, cookies_path=None):
        """
        تسجيل الدخول إلى حساب تيك توك
        
        المعلمات:
            username (str): اسم المستخدم
            password (str, optional): كلمة المرور. إذا كانت None، سيتم استخدام كلمة المرور المخزنة
            cookies_path (str, optional): مسار ملف ملفات تعريف الارتباط
            
        العوائد:
            bool: True إذا تم تسجيل الدخول بنجاح، False خلاف ذلك
        """
        account = self.account_manager.get_account(username)
        if not account:
            print(f"لم يتم العثور على الحساب: {username}")
            return False
        
        # استخدام كلمة المرور المخزنة إذا لم يتم تحديد كلمة مرور
        if not password:
            password = account['password']
        
        # إعداد متصفح Selenium
        self.driver = self._setup_driver(username)
        if not self.driver:
            return False
        
        try:
            # محاولة تسجيل الدخول باستخدام ملفات تعريف الارتباط أولاً
            if self._login_with_cookies(username, cookies_path):
                self.current_username = username
                self.account_manager.update_last_login(username)
                return True
            
            # إذا فشل تسجيل الدخول باستخدام ملفات تعريف الارتباط، حاول تسجيل الدخول باستخدام اسم المستخدم وكلمة المرور
            if self._login_with_credentials(username, password):
                self.current_username = username
                self.account_manager.update_last_login(username)
                return True
            
            return False
        except Exception as e:
            print(f"خطأ في تسجيل الدخول: {e}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            return False
    
    def _login_with_cookies(self, username, cookies_path=None):
        """
        تسجيل الدخول باستخدام ملفات تعريف الارتباط
        
        المعلمات:
            username (str): اسم المستخدم
            cookies_path (str, optional): مسار ملف ملفات تعريف الارتباط
            
        العوائد:
            bool: True إذا تم تسجيل الدخول بنجاح، False خلاف ذلك
        """
        # تحديد مسار ملف ملفات تعريف الارتباط
        if not cookies_path:
            cookies_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cookies')
            cookies_path = os.path.join(cookies_dir, f"{username}.cookies")
        
        # التحقق من وجود ملف ملفات تعريف الارتباط
        if not os.path.exists(cookies_path):
            account = self.account_manager.get_account(username)
            if not account or not account.get('cookies'):
                return False
                
            # حفظ ملفات تعريف الارتباط من الحساب إلى ملف
            try:
                cookies = json.loads(account['cookies'])
                with open(cookies_path, 'wb') as f:
                    pickle.dump(cookies, f)
            except Exception as e:
                print(f"خطأ في حفظ ملفات تعريف الارتباط: {e}")
                return False
        
        try:
            # فتح صفحة تيك توك
            self.driver.get(TIKTOK_URL)
            time.sleep(3)
            
            # تحميل ملفات تعريف الارتباط
            with open(cookies_path, 'rb') as f:
                cookies = pickle.load(f)
                
            # إضافة ملفات تعريف الارتباط إلى المتصفح
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                self.driver.add_cookie(cookie)
            
            # إعادة تحميل الصفحة
            self.driver.get(TIKTOK_URL)
            time.sleep(5)
            
            # التحقق من تسجيل الدخول
            if self._is_logged_in():
                print(f"تم تسجيل الدخول بنجاح باستخدام ملفات تعريف الارتباط: {username}")
                return True
            
            return False
        except Exception as e:
            print(f"خطأ في تسجيل الدخول باستخدام ملفات تعريف الارتباط: {e}")
            return False
    
    def _login_with_credentials(self, username, password):
        """
        تسجيل الدخول باستخدام اسم المستخدم وكلمة المرور
        
        المعلمات:
            username (str): اسم المستخدم
            password (str): كلمة المرور
            
        العوائد:
            bool: True إذا تم تسجيل الدخول بنجاح، False خلاف ذلك
        """
        try:
            # فتح صفحة تسجيل الدخول
            self.driver.get(TIKTOK_LOGIN_URL)
            time.sleep(5)
            
            # انتظار ظهور عناصر تسجيل الدخول
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
                )
            except TimeoutException:
                print("لم يتم العثور على عناصر تسجيل الدخول")
                return False
            
            # إدخال اسم المستخدم وكلمة المرور
            username_input = self.driver.find_element(By.XPATH, "//input[@name='username']")
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            # مسح الحقول وإدخال البيانات
            username_input.clear()
            self._type_like_human(username_input, username)
            
            password_input.clear()
            self._type_like_human(password_input, password)
            
            # النقر على زر تسجيل الدخول
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # انتظار تسجيل الدخول
            time.sleep(10)
            
            # التحقق من تسجيل الدخول
            if self._is_logged_in():
                print(f"تم تسجيل الدخول بنجاح باستخدام اسم المستخدم وكلمة المرور: {username}")
                
                # حفظ ملفات تعريف الارتباط
                self._save_cookies(username)
                
                return True
            
            return False
        except Exception as e:
            print(f"خطأ في تسجيل الدخول باستخدام اسم المستخدم وكلمة المرور: {e}")
            return False
    
    def _is_logged_in(self):
        """
        التحقق مما إذا كان المستخدم قد سجل الدخول
        
        العوائد:
            bool: True إذا كان المستخدم قد سجل الدخول، False خلاف ذلك
        """
        try:
            # التحقق من وجود عناصر تظهر فقط بعد تسجيل الدخول
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@data-e2e, 'profile-icon')]"))
            )
            return True
        except TimeoutException:
            return False
    
    def _save_cookies(self, username):
        """
        حفظ ملفات تعريف الارتباط
        
        المعلمات:
            username (str): اسم المستخدم
        """
        try:
            # الحصول على ملفات تعريف الارتباط
            cookies = self.driver.get_cookies()
            
            # حفظ ملفات تعريف الارتباط إلى ملف
            cookies_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cookies')
            os.makedirs(cookies_dir, exist_ok=True)
            
            cookies_path = os.path.join(cookies_dir, f"{username}.cookies")
            with open(cookies_path, 'wb') as f:
                pickle.dump(cookies, f)
            
            # تحديث ملفات تعريف الارتباط في الحساب
            self.account_manager.update_account(username, cookies=json.dumps(cookies))
            
            print(f"تم حفظ ملفات تعريف الارتباط بنجاح: {username}")
        except Exception as e:
            print(f"خطأ في حفظ ملفات تعريف الارتباط: {e}")
    
    def _type_like_human(self, element, text):
        """
        كتابة النص بطريقة تشبه الإنسان
        
        المعلمات:
            element: عنصر الإدخال
            text (str): النص المراد كتابته
        """
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
    
    def logout(self):
        """
        تسجيل الخروج من الحساب الحالي
        
        العوائد:
            bool: True إذا تم تسجيل الخروج بنجاح، False خلاف ذلك
        """
        if not self.driver:
            return False
        
        try:
            # فتح صفحة تيك توك
            self.driver.get(TIKTOK_URL)
            time.sleep(3)
            
            # النقر على أيقونة الملف الشخصي
            profile_icon = self.driver.find_element(By.XPATH, "//span[contains(@data-e2e, 'profile-icon')]")
            profile_icon.click()
            time.sleep(2)
            
            # النقر على زر تسجيل الخروج
            logout_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Log out')]")
            logout_button.click()
            time.sleep(2)
            
            # تأكيد تسجيل الخروج
            confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log out')]")
            confirm_button.click()
            time.sleep(5)
            
            self.current_username = None
            return True
        except Exception as e:
            print(f"خطأ في تسجيل الخروج: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def close(self):
        """إغلاق متصفح Selenium"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.current_username = None
