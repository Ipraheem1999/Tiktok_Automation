"""
وحدة إدارة حسابات تيك توك
توفر وظائف لإدارة حسابات تيك توك المتعددة
"""

import os
import json
import base64
import hashlib
import random
import time
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.proxy.country_proxy import CountryProxyConfigurator

class AccountManager:
    """مدير حسابات تيك توك"""
    
    def __init__(self, config_dir=None):
        """
        تهيئة مدير الحسابات
        
        المعلمات:
            config_dir (str, optional): مسار دليل التكوين. إذا كان None، سيتم استخدام المسار الافتراضي
        """
        if config_dir is None:
            self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        else:
            self.config_dir = config_dir
            
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.accounts_file = os.path.join(self.config_dir, 'accounts.json')
        self.key_file = os.path.join(self.config_dir, '.key')
        self.accounts = {}
        self.encryption_key = None
        
        # إنشاء مكون تكوين البروكسي
        self.proxy_configurator = CountryProxyConfigurator()
        
        # تحميل الحسابات
        self._load_accounts()
    
    def _generate_encryption_key(self):
        """
        إنشاء مفتاح تشفير جديد
        
        العوائد:
            bytes: مفتاح التشفير
        """
        # إنشاء كلمة مرور عشوائية
        password = os.urandom(32)
        salt = os.urandom(16)
        
        # اشتقاق مفتاح من كلمة المرور
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        
        # حفظ المفتاح والملح
        with open(self.key_file, 'wb') as f:
            f.write(salt + key)
        
        return key
    
    def _load_encryption_key(self):
        """
        تحميل مفتاح التشفير
        
        العوائد:
            bytes: مفتاح التشفير
        """
        if not os.path.exists(self.key_file):
            return self._generate_encryption_key()
        
        with open(self.key_file, 'rb') as f:
            data = f.read()
            
        salt = data[:16]
        key = data[16:]
        
        return key
    
    def _encrypt_password(self, password):
        """
        تشفير كلمة المرور
        
        المعلمات:
            password (str): كلمة المرور
            
        العوائد:
            str: كلمة المرور المشفرة
        """
        if self.encryption_key is None:
            self.encryption_key = self._load_encryption_key()
            
        f = Fernet(self.encryption_key)
        encrypted_password = f.encrypt(password.encode())
        
        return base64.urlsafe_b64encode(encrypted_password).decode()
    
    def _decrypt_password(self, encrypted_password):
        """
        فك تشفير كلمة المرور
        
        المعلمات:
            encrypted_password (str): كلمة المرور المشفرة
            
        العوائد:
            str: كلمة المرور
        """
        if self.encryption_key is None:
            self.encryption_key = self._load_encryption_key()
            
        f = Fernet(self.encryption_key)
        encrypted_password = base64.urlsafe_b64decode(encrypted_password)
        
        return f.decrypt(encrypted_password).decode()
    
    def _load_accounts(self):
        """تحميل الحسابات من الملف"""
        if not os.path.exists(self.accounts_file):
            self.accounts = {}
            return
            
        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                self.accounts = json.load(f)
        except Exception as e:
            print(f"خطأ في تحميل الحسابات: {e}")
            self.accounts = {}
    
    def _save_accounts(self):
        """حفظ الحسابات إلى الملف"""
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ الحسابات: {e}")
    
    def add_account(self, username, password, country_code, nickname=None, cookies=None, user_agent=None, mobile=True):
        """
        إضافة حساب جديد
        
        المعلمات:
            username (str): اسم المستخدم
            password (str): كلمة المرور
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            nickname (str, optional): الاسم المستعار للحساب
            cookies (str, optional): ملفات تعريف الارتباط
            user_agent (str, optional): وكيل المستخدم
            mobile (bool, optional): ما إذا كان الحساب يستخدم محاكاة الأجهزة المحمولة
            
        العوائد:
            bool: True إذا تمت الإضافة بنجاح، False خلاف ذلك
        """
        if username in self.accounts:
            return False
            
        # تشفير كلمة المرور
        encrypted_password = self._encrypt_password(password)
        
        # إنشاء معرف فريد للحساب
        account_id = hashlib.md5(username.encode()).hexdigest()
        
        # إنشاء الحساب
        self.accounts[username] = {
            'id': account_id,
            'username': username,
            'password': encrypted_password,
            'nickname': nickname or username,
            'country_code': country_code,
            'cookies': cookies,
            'user_agent': user_agent,
            'mobile': mobile,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'status': 'active',
            'proxy': None,
            'stats': {
                'posts': 0,
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'saves': 0
            }
        }
        
        self._save_accounts()
        return True
    
    def remove_account(self, username):
        """
        إزالة حساب
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            bool: True إذا تمت الإزالة بنجاح، False خلاف ذلك
        """
        if username not in self.accounts:
            return False
            
        del self.accounts[username]
        self._save_accounts()
        
        return True
    
    def update_account(self, username, **kwargs):
        """
        تحديث معلومات الحساب
        
        المعلمات:
            username (str): اسم المستخدم
            **kwargs: المعلومات المراد تحديثها
            
        العوائد:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        if username not in self.accounts:
            return False
            
        # تحديث المعلومات
        for key, value in kwargs.items():
            if key == 'password':
                # تشفير كلمة المرور الجديدة
                value = self._encrypt_password(value)
                
            if key in self.accounts[username]:
                self.accounts[username][key] = value
        
        self._save_accounts()
        return True
    
    def get_account(self, username):
        """
        الحصول على معلومات الحساب
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            dict: معلومات الحساب أو None إذا لم يتم العثور على الحساب
        """
        if username not in self.accounts:
            return None
            
        account = self.accounts[username].copy()
        
        # فك تشفير كلمة المرور
        try:
            account['password'] = self._decrypt_password(account['password'])
        except Exception:
            account['password'] = '******'
            
        return account
    
    def get_all_accounts(self):
        """
        الحصول على جميع الحسابات
        
        العوائد:
            dict: جميع الحسابات
        """
        accounts = {}
        
        for username, account in self.accounts.items():
            account_copy = account.copy()
            account_copy['password'] = '******'  # إخفاء كلمة المرور
            accounts[username] = account_copy
            
        return accounts
    
    def get_accounts_by_country(self, country_code):
        """
        الحصول على الحسابات حسب الدولة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            dict: الحسابات في الدولة المحددة
        """
        accounts = {}
        
        for username, account in self.accounts.items():
            if account['country_code'] == country_code:
                account_copy = account.copy()
                account_copy['password'] = '******'  # إخفاء كلمة المرور
                accounts[username] = account_copy
                
        return accounts
    
    def set_account_status(self, username, status):
        """
        تعيين حالة الحساب
        
        المعلمات:
            username (str): اسم المستخدم
            status (str): الحالة الجديدة (active, inactive, suspended)
            
        العوائد:
            bool: True إذا تم التعيين بنجاح، False خلاف ذلك
        """
        if username not in self.accounts:
            return False
            
        if status not in ['active', 'inactive', 'suspended']:
            return False
            
        self.accounts[username]['status'] = status
        self._save_accounts()
        
        return True
    
    def update_account_stats(self, username, stats_type, count=1):
        """
        تحديث إحصائيات الحساب
        
        المعلمات:
            username (str): اسم المستخدم
            stats_type (str): نوع الإحصائية (posts, likes, comments, shares, saves)
            count (int, optional): عدد الإحصائية
            
        العوائد:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        if username not in self.accounts:
            return False
            
        if stats_type not in ['posts', 'likes', 'comments', 'shares', 'saves']:
            return False
            
        self.accounts[username]['stats'][stats_type] += count
        self._save_accounts()
        
        return True
    
    def update_last_login(self, username):
        """
        تحديث وقت آخر تسجيل دخول
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        if username not in self.accounts:
            return False
            
        self.accounts[username]['last_login'] = datetime.now().isoformat()
        self._save_accounts()
        
        return True
    
    def assign_proxy_to_account(self, username):
        """
        تعيين بروكسي للحساب
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            str: عنوان البروكسي أو None إذا فشل التعيين
        """
        if username not in self.accounts:
            return None
            
        country_code = self.accounts[username]['country_code']
        proxy = self.proxy_configurator.get_working_proxy(country_code)
        
        if proxy:
            self.accounts[username]['proxy'] = proxy
            self._save_accounts()
            
        return proxy
    
    def get_account_proxy(self, username):
        """
        الحصول على بروكسي الحساب
        
        المعلمات:
            username (str): اسم المستخدم
            
        العوائد:
            str: عنوان البروكسي أو None إذا لم يتم العثور على بروكسي
        """
        if username not in self.accounts:
            return None
            
        proxy = self.accounts[username].get('proxy')
        
        if not proxy:
            # محاولة تعيين بروكسي جديد
            proxy = self.assign_proxy_to_account(username)
            
        return proxy
    
    def import_accounts_from_file(self, file_path):
        """
        استيراد الحسابات من ملف
        
        المعلمات:
            file_path (str): مسار ملف الحسابات
            
        العوائد:
            int: عدد الحسابات المستوردة
        """
        imported_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    parts = line.split(',')
                    if len(parts) >= 3:
                        username = parts[0].strip()
                        password = parts[1].strip()
                        country_code = parts[2].strip()
                        
                        nickname = None
                        if len(parts) >= 4:
                            nickname = parts[3].strip()
                            
                        if username and password and country_code:
                            if self.add_account(username, password, country_code, nickname):
                                imported_count += 1
            
            return imported_count
        except Exception as e:
            print(f"خطأ في استيراد الحسابات من الملف: {e}")
            return 0
    
    def export_accounts_to_file(self, file_path):
        """
        تصدير الحسابات إلى ملف
        
        المعلمات:
            file_path (str): مسار ملف الحسابات
            
        العوائد:
            bool: True إذا تم التصدير بنجاح، False خلاف ذلك
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# username,password,country_code,nickname\n")
                
                for username, account in self.accounts.items():
                    password = self._decrypt_password(account['password'])
                    country_code = account['country_code']
                    nickname = account.get('nickname', '')
                    
                    f.write(f"{username},{password},{country_code},{nickname}\n")
            
            return True
        except Exception as e:
            print(f"خطأ في تصدير الحسابات إلى الملف: {e}")
            return False
