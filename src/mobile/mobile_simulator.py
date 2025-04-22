"""
وحدة محاكاة الأجهزة المحمولة
توفر وظائف لمحاكاة الأجهزة المحمولة عند التفاعل مع تيك توك
"""

import os
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from fake_useragent import UserAgent

class MobileSimulator:
    """محاكي الأجهزة المحمولة"""
    
    # قائمة بأجهزة الهواتف المحمولة الشائعة
    MOBILE_DEVICES = [
        {
            "name": "iPhone X",
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "width": 375,
            "height": 812,
            "pixel_ratio": 3.0,
            "touch": True,
            "mobile": True,
            "platform": "iOS"
        },
        {
            "name": "iPhone 11",
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "width": 414,
            "height": 896,
            "pixel_ratio": 2.0,
            "touch": True,
            "mobile": True,
            "platform": "iOS"
        },
        {
            "name": "iPhone 12",
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "width": 390,
            "height": 844,
            "pixel_ratio": 3.0,
            "touch": True,
            "mobile": True,
            "platform": "iOS"
        },
        {
            "name": "Samsung Galaxy S20",
            "user_agent": "Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
            "width": 360,
            "height": 800,
            "pixel_ratio": 3.0,
            "touch": True,
            "mobile": True,
            "platform": "Android"
        },
        {
            "name": "Samsung Galaxy S21",
            "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
            "width": 360,
            "height": 800,
            "pixel_ratio": 3.0,
            "touch": True,
            "mobile": True,
            "platform": "Android"
        },
        {
            "name": "Google Pixel 5",
            "user_agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
            "width": 393,
            "height": 851,
            "pixel_ratio": 2.75,
            "touch": True,
            "mobile": True,
            "platform": "Android"
        },
        {
            "name": "Xiaomi Mi 11",
            "user_agent": "Mozilla/5.0 (Linux; Android 11; M2011K2G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
            "width": 393,
            "height": 873,
            "pixel_ratio": 3.0,
            "touch": True,
            "mobile": True,
            "platform": "Android"
        },
        {
            "name": "OnePlus 9",
            "user_agent": "Mozilla/5.0 (Linux; Android 11; LE2113) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
            "width": 412,
            "height": 919,
            "pixel_ratio": 2.625,
            "touch": True,
            "mobile": True,
            "platform": "Android"
        }
    ]
    
    # قائمة بوكلاء المستخدم للأجهزة المحمولة
    MOBILE_USER_AGENTS = [
        # iOS
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        
        # Android
        "Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; M2011K2G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; LE2113) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.0 Chrome/87.0.4280.141 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/15.0 Chrome/90.0.4430.210 Mobile Safari/537.36"
    ]
    
    # قائمة بأنواع الأجهزة المحمولة
    DEVICE_TYPES = ["iPhone", "Android"]
    
    def __init__(self, config_dir=None):
        """
        تهيئة محاكي الأجهزة المحمولة
        
        المعلمات:
            config_dir (str, optional): مسار دليل التكوين. إذا كان None، سيتم استخدام المسار الافتراضي
        """
        if config_dir is None:
            self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        else:
            self.config_dir = config_dir
            
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.devices_file = os.path.join(self.config_dir, 'mobile_devices.json')
        
        # تحميل الأجهزة المحمولة
        self._load_devices()
    
    def _load_devices(self):
        """تحميل الأجهزة المحمولة من الملف"""
        if not os.path.exists(self.devices_file):
            # إنشاء ملف الأجهزة المحمولة
            with open(self.devices_file, 'w', encoding='utf-8') as f:
                json.dump(self.MOBILE_DEVICES, f, ensure_ascii=False, indent=2)
    
    def get_random_device(self, platform=None):
        """
        الحصول على جهاز محمول عشوائي
        
        المعلمات:
            platform (str, optional): منصة الجهاز (iOS, Android)
            
        العوائد:
            dict: معلومات الجهاز
        """
        with open(self.devices_file, 'r', encoding='utf-8') as f:
            devices = json.load(f)
        
        if platform:
            devices = [device for device in devices if device['platform'] == platform]
            
        if not devices:
            return random.choice(self.MOBILE_DEVICES)
            
        return random.choice(devices)
    
    def get_random_user_agent(self, platform=None):
        """
        الحصول على وكيل مستخدم عشوائي للأجهزة المحمولة
        
        المعلمات:
            platform (str, optional): منصة الجهاز (iOS, Android)
            
        العوائد:
            str: وكيل المستخدم
        """
        if platform == "iOS":
            ios_agents = [ua for ua in self.MOBILE_USER_AGENTS if "iPhone" in ua or "iPad" in ua]
            return random.choice(ios_agents)
        elif platform == "Android":
            android_agents = [ua for ua in self.MOBILE_USER_AGENTS if "Android" in ua]
            return random.choice(android_agents)
        else:
            return random.choice(self.MOBILE_USER_AGENTS)
    
    def configure_chrome_options(self, device=None, user_agent=None):
        """
        تكوين خيارات Chrome لمحاكاة الأجهزة المحمولة
        
        المعلمات:
            device (dict, optional): معلومات الجهاز
            user_agent (str, optional): وكيل المستخدم
            
        العوائد:
            Options: خيارات Chrome
        """
        options = uc.ChromeOptions()
        
        # إذا لم يتم تحديد جهاز، استخدم جهازًا عشوائيًا
        if not device:
            device = self.get_random_device()
        
        # إذا لم يتم تحديد وكيل مستخدم، استخدم وكيل المستخدم للجهاز
        if not user_agent:
            user_agent = device['user_agent']
        
        # إضافة وكيل المستخدم
        options.add_argument(f'--user-agent={user_agent}')
        
        # إضافة إعدادات محاكاة الجوال
        mobile_emulation = {
            "deviceMetrics": {
                "width": device['width'],
                "height": device['height'],
                "pixelRatio": device['pixel_ratio']
            },
            "userAgent": user_agent
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # إضافة إعدادات إضافية
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        return options
    
    def create_mobile_driver(self, device=None, user_agent=None, proxy=None):
        """
        إنشاء متصفح Selenium لمحاكاة الأجهزة المحمولة
        
        المعلمات:
            device (dict, optional): معلومات الجهاز
            user_agent (str, optional): وكيل المستخدم
            proxy (str, optional): عنوان البروكسي
            
        العوائد:
            webdriver: متصفح Selenium
        """
        # إذا لم يتم تحديد جهاز، استخدم جهازًا عشوائيًا
        if not device:
            device = self.get_random_device()
        
        # إذا لم يتم تحديد وكيل مستخدم، استخدم وكيل المستخدم للجهاز
        if not user_agent:
            user_agent = device['user_agent']
        
        # تكوين خيارات Chrome
        options = self.configure_chrome_options(device, user_agent)
        
        # إضافة البروكسي إذا كان متاحًا
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        
        try:
            # إنشاء متصفح Selenium
            driver = uc.Chrome(options=options)
            driver.set_page_load_timeout(30)
            
            # تعديل سلوك المتصفح لتجنب الكشف
            self._apply_stealth_techniques(driver)
            
            return driver
        except Exception as e:
            print(f"خطأ في إنشاء متصفح Selenium: {e}")
            return None
    
    def _apply_stealth_techniques(self, driver):
        """
        تطبيق تقنيات التخفي لتجنب الكشف
        
        المعلمات:
            driver (webdriver): متصفح Selenium
        """
        # تعديل خصائص navigator
        driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """)
        
        # تعديل خصائص navigator.plugins
        driver.execute_script("""
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        """)
        
        # تعديل خصائص navigator.languages
        driver.execute_script("""
        Object.defineProperty(navigator, 'languages', {
            get: () => ['ar-SA', 'ar', 'en-US', 'en']
        });
        """)
        
        # إضافة سلوك عشوائي
        self._add_random_behavior(driver)
    
    def _add_random_behavior(self, driver):
        """
        إضافة سلوك عشوائي للمتصفح
        
        المعلمات:
            driver (webdriver): متصفح Selenium
        """
        # تمرير الماوس بشكل عشوائي
        driver.execute_script("""
        const randomMove = () => {
            const x = Math.floor(Math.random() * window.innerWidth);
            const y = Math.floor(Math.random() * window.innerHeight);
            
            const event = new MouseEvent('mousemove', {
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': x,
                'clientY': y
            });
            
            document.dispatchEvent(event);
        };
        
        setInterval(randomMove, 2000 + Math.floor(Math.random() * 3000));
        """)
        
        # تمرير الصفحة بشكل عشوائي
        driver.execute_script("""
        const randomScroll = () => {
            if (Math.random() > 0.7) {
                const scrollY = Math.floor(Math.random() * 100);
                window.scrollBy(0, scrollY);
                
                setTimeout(() => {
                    window.scrollBy(0, -scrollY);
                }, 500 + Math.floor(Math.random() * 1000));
            }
        };
        
        setInterval(randomScroll, 5000 + Math.floor(Math.random() * 5000));
        """)
    
    def simulate_human_behavior(self, driver):
        """
        محاكاة سلوك الإنسان
        
        المعلمات:
            driver (webdriver): متصفح Selenium
        """
        # تمرير الصفحة ببطء
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        
        while current_position < scroll_height:
            # تمرير الصفحة بمقدار عشوائي
            scroll_step = random.randint(100, 300)
            current_position += scroll_step
            
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            
            # انتظار فترة عشوائية
            time.sleep(random.uniform(0.5, 2.0))
            
            # تحديث ارتفاع الصفحة
            scroll_height = driver.execute_script("return document.body.scrollHeight")
        
        # التمرير إلى أعلى الصفحة
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.0, 2.0))
    
    def add_device(self, name, user_agent, width, height, pixel_ratio, platform):
        """
        إضافة جهاز محمول جديد
        
        المعلمات:
            name (str): اسم الجهاز
            user_agent (str): وكيل المستخدم
            width (int): عرض الشاشة
            height (int): ارتفاع الشاشة
            pixel_ratio (float): نسبة البكسل
            platform (str): منصة الجهاز (iOS, Android)
            
        العوائد:
            bool: True إذا تمت الإضافة بنجاح، False خلاف ذلك
        """
        try:
            with open(self.devices_file, 'r', encoding='utf-8') as f:
                devices = json.load(f)
            
            # التحقق من وجود الجهاز
            for device in devices:
                if device['name'] == name:
                    return False
            
            # إضافة الجهاز
            devices.append({
                "name": name,
                "user_agent": user_agent,
                "width": width,
                "height": height,
                "pixel_ratio": pixel_ratio,
                "touch": True,
                "mobile": True,
                "platform": platform
            })
            
            # حفظ الأجهزة
            with open(self.devices_file, 'w', encoding='utf-8') as f:
                json.dump(devices, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"خطأ في إضافة الجهاز: {e}")
            return False
    
    def remove_device(self, name):
        """
        إزالة جهاز محمول
        
        المعلمات:
            name (str): اسم الجهاز
            
        العوائد:
            bool: True إذا تمت الإزالة بنجاح، False خلاف ذلك
        """
        try:
            with open(self.devices_file, 'r', encoding='utf-8') as f:
                devices = json.load(f)
            
            # البحث عن الجهاز
            for i, device in enumerate(devices):
                if device['name'] == name:
                    # إزالة الجهاز
                    del devices[i]
                    
                    # حفظ الأجهزة
                    with open(self.devices_file, 'w', encoding='utf-8') as f:
                        json.dump(devices, f, ensure_ascii=False, indent=2)
                    
                    return True
            
            return False
        except Exception as e:
            print(f"خطأ في إزالة الجهاز: {e}")
            return False
    
    def get_all_devices(self):
        """
        الحصول على جميع الأجهزة المحمولة
        
        العوائد:
            list: قائمة الأجهزة المحمولة
        """
        try:
            with open(self.devices_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"خطأ في الحصول على الأجهزة: {e}")
            return []
    
    def get_device(self, name):
        """
        الحصول على جهاز محمول
        
        المعلمات:
            name (str): اسم الجهاز
            
        العوائد:
            dict: معلومات الجهاز أو None إذا لم يتم العثور على الجهاز
        """
        try:
            with open(self.devices_file, 'r', encoding='utf-8') as f:
                devices = json.load(f)
            
            # البحث عن الجهاز
            for device in devices:
                if device['name'] == name:
                    return device
            
            return None
        except Exception as e:
            print(f"خطأ في الحصول على الجهاز: {e}")
            return None
