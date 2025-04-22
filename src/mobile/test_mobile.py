"""
وحدة اختبار محاكاة الأجهزة المحمولة
توفر وظائف لاختبار محاكاة الأجهزة المحمولة مع تيك توك
"""

import argparse
import sys
import os
import time
import random
from src.mobile.mobile_simulator import MobileSimulator
from src.proxy.proxy_manager import ProxyManager

def main():
    """
    النقطة الرئيسية لتشغيل اختبار محاكاة الأجهزة المحمولة
    """
    parser = argparse.ArgumentParser(description='اختبار محاكاة الأجهزة المحمولة مع تيك توك')
    parser.add_argument('--device', help='اسم الجهاز المحمول')
    parser.add_argument('--platform', choices=['iOS', 'Android'], help='منصة الجهاز')
    parser.add_argument('--proxy', help='عنوان البروكسي')
    parser.add_argument('--country', choices=['saudi_arabia', 'uae', 'kuwait', 'egypt'], help='الدولة المستهدفة للبروكسي')
    parser.add_argument('--wait', type=int, default=30, help='وقت الانتظار بالثواني قبل إغلاق المتصفح')
    
    args = parser.parse_args()
    
    # إنشاء محاكي الأجهزة المحمولة
    mobile_simulator = MobileSimulator()
    
    # إنشاء مدير البروكسي
    proxy_manager = ProxyManager()
    
    # تحديد الجهاز
    device = None
    if args.device:
        device = mobile_simulator.get_device(args.device)
        if not device:
            print(f"لم يتم العثور على الجهاز: {args.device}")
            return 1
    else:
        device = mobile_simulator.get_random_device(args.platform)
    
    # تحديد البروكسي
    proxy = args.proxy
    if not proxy and args.country:
        proxy = proxy_manager.get_random_proxy(args.country)
        if not proxy:
            print(f"لم يتم العثور على بروكسي للدولة: {args.country}")
            return 1
    
    print(f"استخدام الجهاز: {device['name']}")
    if proxy:
        print(f"استخدام البروكسي: {proxy}")
    
    # إنشاء متصفح Selenium
    driver = mobile_simulator.create_mobile_driver(device, None, proxy)
    if not driver:
        print("فشل في إنشاء متصفح Selenium")
        return 1
    
    try:
        # فتح صفحة تيك توك
        print("فتح صفحة تيك توك...")
        driver.get('https://www.tiktok.com/')
        time.sleep(5)
        
        # محاكاة سلوك الإنسان
        print("محاكاة سلوك الإنسان...")
        mobile_simulator.simulate_human_behavior(driver)
        
        # التفاعل مع الصفحة
        print("التفاعل مع الصفحة...")
        interact_with_page(driver)
        
        # الانتظار قبل إغلاق المتصفح
        if args.wait > 0:
            print(f"انتظار {args.wait} ثانية قبل إغلاق المتصفح...")
            time.sleep(args.wait)
        
        return 0
    except Exception as e:
        print(f"خطأ في اختبار محاكاة الأجهزة المحمولة: {e}")
        return 1
    finally:
        # إغلاق المتصفح
        if driver:
            driver.quit()

def interact_with_page(driver):
    """
    التفاعل مع صفحة تيك توك
    
    المعلمات:
        driver (webdriver): متصفح Selenium
    """
    # البحث عن عناصر الصفحة
    try:
        # النقر على زر البحث
        search_button = driver.find_element_by_xpath("//span[contains(@data-e2e, 'search')]")
        search_button.click()
        time.sleep(2)
        
        # إدخال نص البحث
        search_input = driver.find_element_by_xpath("//input[@type='search']")
        search_terms = ['funny', 'dance', 'challenge', 'food', 'travel', 'music', 'pets', 'sports']
        search_term = random.choice(search_terms)
        
        for char in search_term:
            search_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        time.sleep(1)
        search_input.submit()
        time.sleep(5)
        
        # التمرير لأسفل
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(random.uniform(1.0, 3.0))
        
        # محاولة النقر على فيديو
        try:
            videos = driver.find_elements_by_xpath("//div[contains(@class, 'video-feed-item')]")
            if videos:
                random.choice(videos).click()
                time.sleep(5)
                
                # التفاعل مع الفيديو
                try:
                    # الإعجاب بالفيديو
                    like_button = driver.find_element_by_xpath("//span[contains(@data-e2e, 'like-icon')]")
                    like_button.click()
                    time.sleep(2)
                    
                    # إلغاء الإعجاب
                    like_button.click()
                    time.sleep(1)
                except:
                    pass
                
                # العودة للصفحة السابقة
                driver.back()
                time.sleep(3)
        except:
            pass
        
        # التمرير لأعلى
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # النقر على الصفحة الرئيسية
        try:
            home_button = driver.find_element_by_xpath("//span[contains(@data-e2e, 'home')]")
            home_button.click()
            time.sleep(3)
        except:
            pass
    except Exception as e:
        print(f"خطأ في التفاعل مع الصفحة: {e}")

if __name__ == "__main__":
    sys.exit(main())
