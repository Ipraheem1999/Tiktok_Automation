"""
وحدة تكوين البروكسي للدول المستهدفة
توفر واجهة لإعداد وإدارة البروكسي للدول المستهدفة (السعودية، الإمارات، الكويت، مصر)
"""

import os
import json
from src.proxy.proxy_manager import ProxyManager
from src.utils.config import TARGET_COUNTRIES

class CountryProxyConfigurator:
    """مكون تكوين البروكسي للدول المستهدفة"""
    
    def __init__(self):
        """تهيئة مكون تكوين البروكسي"""
        self.proxy_manager = ProxyManager()
        self.proxy_manager.load_proxies_from_config()
        self.proxy_configs = {}
        self._load_country_configs()
    
    def _load_country_configs(self):
        """تحميل تكوينات الدول من الملفات"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, 'country_proxies.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.proxy_configs = json.load(f)
            except Exception as e:
                print(f"خطأ في تحميل تكوينات الدول: {e}")
                self._initialize_default_configs()
        else:
            self._initialize_default_configs()
    
    def _initialize_default_configs(self):
        """تهيئة التكوينات الافتراضية للدول"""
        self.proxy_configs = {
            country_code: {
                'enabled': True,
                'proxies': [],
                'current_proxy': None,
                'country_info': country_info
            }
            for country_code, country_info in TARGET_COUNTRIES.items()
        }
        self._save_country_configs()
    
    def _save_country_configs(self):
        """حفظ تكوينات الدول إلى ملف"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, 'country_proxies.json')
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.proxy_configs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ تكوينات الدول: {e}")
    
    def add_proxy(self, country_code, proxy_url):
        """
        إضافة بروكسي لدولة محددة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            proxy_url (str): عنوان البروكسي
            
        العوائد:
            bool: True إذا تمت الإضافة بنجاح، False خلاف ذلك
        """
        if country_code not in self.proxy_configs:
            return False
        
        if proxy_url not in self.proxy_configs[country_code]['proxies']:
            self.proxy_configs[country_code]['proxies'].append(proxy_url)
            self._save_country_configs()
            return True
        
        return False
    
    def remove_proxy(self, country_code, proxy_url):
        """
        إزالة بروكسي من دولة محددة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            proxy_url (str): عنوان البروكسي
            
        العوائد:
            bool: True إذا تمت الإزالة بنجاح، False خلاف ذلك
        """
        if country_code not in self.proxy_configs:
            return False
        
        if proxy_url in self.proxy_configs[country_code]['proxies']:
            self.proxy_configs[country_code]['proxies'].remove(proxy_url)
            
            # إذا كان البروكسي الحالي هو الذي تمت إزالته، قم بإعادة تعيينه إلى None
            if self.proxy_configs[country_code]['current_proxy'] == proxy_url:
                self.proxy_configs[country_code]['current_proxy'] = None
            
            self._save_country_configs()
            return True
        
        return False
    
    def set_country_enabled(self, country_code, enabled):
        """
        تعيين حالة تفعيل الدولة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            enabled (bool): حالة التفعيل
            
        العوائد:
            bool: True إذا تم التعيين بنجاح، False خلاف ذلك
        """
        if country_code not in self.proxy_configs:
            return False
        
        self.proxy_configs[country_code]['enabled'] = enabled
        self._save_country_configs()
        return True
    
    def get_country_proxies(self, country_code):
        """
        الحصول على قائمة البروكسي للدولة المحددة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            list: قائمة البروكسي للدولة المحددة أو قائمة فارغة إذا لم يتم العثور على الدولة
        """
        if country_code not in self.proxy_configs:
            return []
        
        return self.proxy_configs[country_code]['proxies']
    
    def get_enabled_countries(self):
        """
        الحصول على قائمة الدول المفعلة
        
        العوائد:
            list: قائمة رموز الدول المفعلة
        """
        return [
            country_code
            for country_code, config in self.proxy_configs.items()
            if config['enabled']
        ]
    
    def get_country_info(self, country_code):
        """
        الحصول على معلومات الدولة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            dict: معلومات الدولة أو None إذا لم يتم العثور على الدولة
        """
        if country_code not in self.proxy_configs:
            return None
        
        return self.proxy_configs[country_code]['country_info']
    
    def test_country_proxies(self, country_code):
        """
        اختبار جميع البروكسي للدولة المحددة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            dict: نتائج الاختبار لكل بروكسي
        """
        if country_code not in self.proxy_configs:
            return {}
        
        results = {}
        for proxy in self.proxy_configs[country_code]['proxies']:
            result = self.proxy_manager.test_proxy(proxy)
            results[proxy] = result
        
        return results
    
    def get_working_proxy(self, country_code):
        """
        الحصول على بروكسي يعمل للدولة المحددة
        
        المعلمات:
            country_code (str): رمز الدولة (saudi_arabia, uae, kuwait, egypt)
            
        العوائد:
            str: عنوان البروكسي أو None إذا لم يتم العثور على بروكسي يعمل
        """
        if country_code not in self.proxy_configs or not self.proxy_configs[country_code]['enabled']:
            return None
        
        # اختبار البروكسي الحالي أولاً إذا كان موجودًا
        current_proxy = self.proxy_configs[country_code]['current_proxy']
        if current_proxy and self.proxy_manager.test_proxy(current_proxy):
            return current_proxy
        
        # اختبار جميع البروكسي حتى العثور على واحد يعمل
        for proxy in self.proxy_configs[country_code]['proxies']:
            if self.proxy_manager.test_proxy(proxy):
                self.proxy_configs[country_code]['current_proxy'] = proxy
                self._save_country_configs()
                return proxy
        
        return None
    
    def import_proxies_from_file(self, file_path):
        """
        استيراد البروكسي من ملف
        
        المعلمات:
            file_path (str): مسار ملف البروكسي
            
        العوائد:
            dict: عدد البروكسي المستوردة لكل دولة
        """
        results = {country_code: 0 for country_code in self.proxy_configs.keys()}
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split(':', 1)
                    if len(parts) == 2 and parts[0] in self.proxy_configs:
                        country_code = parts[0]
                        proxy_url = parts[1]
                        
                        if proxy_url not in self.proxy_configs[country_code]['proxies']:
                            self.proxy_configs[country_code]['proxies'].append(proxy_url)
                            results[country_code] += 1
            
            self._save_country_configs()
            return results
        except Exception as e:
            print(f"خطأ في استيراد البروكسي من الملف: {e}")
            return results
    
    def export_proxies_to_file(self, file_path):
        """
        تصدير البروكسي إلى ملف
        
        المعلمات:
            file_path (str): مسار ملف البروكسي
            
        العوائد:
            bool: True إذا تم التصدير بنجاح، False خلاف ذلك
        """
        try:
            with open(file_path, 'w') as f:
                for country_code, config in self.proxy_configs.items():
                    for proxy in config['proxies']:
                        f.write(f"{country_code}:{proxy}\n")
            
            return True
        except Exception as e:
            print(f"خطأ في تصدير البروكسي إلى الملف: {e}")
            return False
