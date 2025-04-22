"""
وحدة إدارة البروكسي
تتيح إعداد واستخدام البروكسي للدول المستهدفة
"""

import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from src.utils.config import (
    TARGET_COUNTRIES, PROXY_ENABLED, PROXY_TYPE, PROXY_HOST, 
    PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD
)

class ProxyManager:
    """مدير البروكسي للتحكم في إعدادات البروكسي للدول المستهدفة"""
    
    def __init__(self):
        """تهيئة مدير البروكسي"""
        self.proxies = {
            'saudi_arabia': [],
            'uae': [],
            'kuwait': [],
            'egypt': []
        }
        self.current_proxy = None
        self.current_country = None
        
    def load_proxies_from_config(self):
        """تحميل البروكسي من إعدادات التكوين"""
        if not PROXY_ENABLED:
            return False
            
        if PROXY_HOST and PROXY_PORT:
            proxy_auth = ""
            if PROXY_USERNAME and PROXY_PASSWORD:
                proxy_auth = f"{PROXY_USERNAME}:{PROXY_PASSWORD}@"
                
            proxy_url = f"{PROXY_TYPE}://{proxy_auth}{PROXY_HOST}:{PROXY_PORT}"
            
            # إضافة البروكسي لجميع الدول المستهدفة
            for country in self.proxies.keys():
                self.proxies[country].append(proxy_url)
                
            return True
        return False
    
    def load_proxies_from_file(self, file_path, country=None):
        """
        تحميل البروكسي من ملف
        
        المعلمات:
            file_path (str): مسار ملف البروكسي
            country (str, optional): رمز الدولة. إذا كان None، سيتم تحميل البروكسي لجميع الدول
        
        التنسيق المتوقع للملف:
            country_code:proxy_type://username:password@host:port
            أو
            proxy_type://username:password@host:port (إذا تم تحديد الدولة)
        """
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    if country:
                        # إذا تم تحديد الدولة، فإن كل سطر هو بروكسي لتلك الدولة
                        self.proxies[country].append(line)
                    else:
                        # إذا لم يتم تحديد الدولة، فإن التنسيق هو country_code:proxy
                        parts = line.split(':', 1)
                        if len(parts) == 2 and parts[0] in self.proxies:
                            self.proxies[parts[0]].append(parts[1])
            return True
        except Exception as e:
            print(f"خطأ في تحميل البروكسي من الملف: {e}")
            return False
    
    def get_proxy_for_country(self, country_code):
        """
        الحصول على بروكسي عشوائي لدولة محددة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            str: عنوان البروكسي أو None إذا لم يتم العثور على بروكسي
        """
        if not PROXY_ENABLED:
            return None
            
        if country_code in self.proxies and self.proxies[country_code]:
            self.current_proxy = random.choice(self.proxies[country_code])
            self.current_country = country_code
            return self.current_proxy
        return None
    
    def get_random_proxy(self):
        """
        الحصول على بروكسي عشوائي من أي دولة مستهدفة
        
        العوائد:
            str: عنوان البروكسي أو None إذا لم يتم العثور على بروكسي
        """
        if not PROXY_ENABLED:
            return None
            
        all_proxies = []
        for proxies in self.proxies.values():
            all_proxies.extend(proxies)
            
        if all_proxies:
            self.current_proxy = random.choice(all_proxies)
            return self.current_proxy
        return None
    
    def test_proxy(self, proxy_url=None):
        """
        اختبار اتصال البروكسي
        
        المعلمات:
            proxy_url (str, optional): عنوان البروكسي للاختبار. إذا كان None، سيتم استخدام البروكسي الحالي
            
        العوائد:
            bool: True إذا كان البروكسي يعمل، False خلاف ذلك
        """
        if not proxy_url and not self.current_proxy:
            return False
            
        proxy_to_test = proxy_url or self.current_proxy
        
        try:
            proxies = {
                'http': proxy_to_test,
                'https': proxy_to_test
            }
            
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            if response.status_code == 200:
                return True
        except Exception as e:
            print(f"خطأ في اختبار البروكسي: {e}")
        
        return False
    
    def configure_webdriver_proxy(self, chrome_options=None):
        """
        تكوين البروكسي لـ WebDriver
        
        المعلمات:
            chrome_options (Options, optional): خيارات Chrome. إذا كان None، سيتم إنشاء خيارات جديدة
            
        العوائد:
            Options: خيارات Chrome مع إعدادات البروكسي
        """
        if not PROXY_ENABLED or not self.current_proxy:
            return chrome_options or Options()
            
        options = chrome_options or Options()
        
        # تحليل عنوان البروكسي
        proxy_parts = self.current_proxy.split('://')
        if len(proxy_parts) != 2:
            return options
            
        proxy_type = proxy_parts[0]
        proxy_address = proxy_parts[1]
        
        # إضافة إعدادات البروكسي إلى خيارات Chrome
        if proxy_type in ['http', 'https']:
            options.add_argument(f'--proxy-server={self.current_proxy}')
        elif proxy_type in ['socks4', 'socks5']:
            options.add_argument(f'--proxy-server={proxy_type}://{proxy_address}')
        
        return options
    
    def get_country_info(self, country_code):
        """
        الحصول على معلومات الدولة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            dict: معلومات الدولة أو None إذا لم يتم العثور على الدولة
        """
        return TARGET_COUNTRIES.get(country_code)
