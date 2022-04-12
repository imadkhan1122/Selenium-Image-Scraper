from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time
import os
from datetime import datetime

options = Options()
# options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('disable-avfoundation-overlays')
options.add_argument('disable-internal-flash')
options.add_argument('no-proxy-server')
options.add_argument("disable-notifications")
options.add_argument("disable-popup")
prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)
options.add_argument('--headless')

def download_images(pth, dir_):
    r = requests.get(pth)
    pth, name = os.path.split(pth)
    t = str(datetime.now().time())
    name = dir_+'/'+t+'-'+name
    with open(name,'wb') as f:
        f.write(r.content)
        print(name)
    

def get_images():
    Dir = 'Crystal_data'
    if not os.path.exists(Dir):
        os.mkdir(Dir)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # lst = []
    driver.get('https://www.fossilera.com/minerals-for-sale')
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'fancybox-skin')))
    driver.find_element_by_css_selector('a.fancybox-item.fancybox-close').click()
    time.sleep(2)
    driver.find_element_by_css_selector('div.more-categories-button').click()
    
    cat = driver.find_element_by_css_selector('div#all_categories_block')
    cat_lst = cat.find_elements_by_class_name('group')
    for group in cat_lst:
        time.sleep(3)
        link = group.find_elements_by_tag_name('div')
        try:
            for l in link:
                lnk = l.find_element_by_tag_name('a').get_attribute('href')
                pth, catName = os.path.split(lnk)
                Pth = Dir+'/'+catName
                if not os.path.exists(Pth):
                    os.mkdir(Pth)
                driver.execute_script("window.open('');")
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
                driver.get(lnk)
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.image')))
                footer = driver.find_element_by_css_selector('div.footer')
                actions = ActionChains(driver)
                actions.move_to_element(footer).perform()
                time.sleep(3)
                # Scroll page down to Next Button
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                imgs = soup.find_all('div', attrs={'class':'image'})
                
                for i in imgs:
                    img_url = i.find('img')
                    time.sleep(3)
                    link = 'https:'+img_url.get('src')
                    # print(link)
                    
                    download_images(link, Pth)
                    
                # pagination of all pages
                while len(imgs) > 59:
                    Next = driver.find_element_by_css_selector('span.next')
                    actions = ActionChains(driver)
                    actions.move_to_element(Next).perform()
                    time.sleep(2)
                    Next.click()
                    time.sleep(3)
                    footer = driver.find_element_by_css_selector('div.footer')
                    actions = ActionChains(driver)
                    actions.move_to_element(footer).perform()
                    # Scroll page down to Next Button
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    imgs = soup.find_all('div', attrs={'class':'image'})
                    for i in imgs:
                        img_url = i.find('img')
                        time.sleep(3)
                        link = 'https:'+img_url.get('src')
                        # print(link)
                        
                        download_images(link, Pth)
                        
                driver.close()  
                # Switching to old tab
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass
    time.sleep(5)
    
    driver.quit()
    
get_images()

import subprocess

subprocess.Popen("crystal_img_scraper.py")
