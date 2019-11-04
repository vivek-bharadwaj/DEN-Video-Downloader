
# coding: utf-8

# In[1]:


import os
import os.path
import urllib.request
import sys
import time
import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


def page_has_loaded():
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


#wait until a condition is hold or expire seconds has elaspsed
def wait(condition, expire):
    start_time = time.time()
    while time.time() < start_time + expire:
        if condition():
            return True
        else:
            time.sleep(0.1)
    raise Exception('Timeout waiting for {}'.format(condition.__name__))


def download(video_url):
    init_url = video_url
    init_url_prefix = init_url.split('/playlist')[0]
    file_name_parts = init_url.split('/')[6].split('_')
    file_name = file_name_parts[0] + '_' + file_name_parts[1][-8:]

    if os.path.isfile(file_name + ".ts"):
        print('%s.ts already exists, skip download.' % file_name)
        return

    '''Resolve M3U8 playlist attributes.'''
    print()
    sys.stdout.write('INFO: Resolving M3U8 playlist URL ... ')
    with urllib.request.urlopen(init_url) as f:
        m3u8_postfix = f.read().split()[-1].decode('utf-8')
    print("Done!")
    m3u8_url = init_url_prefix + '/' + m3u8_postfix

    '''Resolve video segment attributes.'''
    sys.stdout.write('INFO: Resolving video segment URLs ... ')
    with urllib.request.urlopen(m3u8_url) as f:
        m3u8_contents = f.read().decode('utf-8').split('\n')
    print("Done!")
    num_total_segments = int((len(m3u8_contents) - 6) / 2)
    video_segment_prefix = m3u8_contents[5].split('_ps0_')[0] + '_ps0_'

    '''Download video segments and concatenate together into a whole video.'''
    timestamp = int(time.time() * 100)

    if platform.system() == 'Windows':
        os.system('md temp_%s' % timestamp)
        print('curl -o temp_%s/part_#1.ts %s/%s\[000-%d\].ts'
              % (timestamp, init_url_prefix, video_segment_prefix, num_total_segments - 1))
        os.system('curl -o temp_%s/part_#1.ts %s/%s[000-%d].ts'
              % (timestamp, init_url_prefix, video_segment_prefix, num_total_segments - 1))
        os.system('cd temp_%s && type part_*.ts > ../%s.ts && cd ..' % (timestamp, file_name))
        os.system('rd /s /q temp_%s' % timestamp)
        
    elif platform.system() == 'Linux':
        os.system('mkdir ./temp_%s/' % timestamp)
        os.system('curl -o ./temp_%s/part_#1.ts %s/%s\[000-%d\].ts'
              % (timestamp, init_url_prefix, video_segment_prefix, num_total_segments - 1))
        os.system('cat ./temp_%s/part* > %s.ts' % (timestamp, file_name))
        os.system('rm -rf ./temp_%s/' % timestamp)
    else:
        assert False, 'No valid platform detected.'

    print()
    print("INFO: %s download completed." % file_name)
    print()


if len(sys.argv) != 4:
    print('Usage: python3 ./dendown_all.py Username Password Course')
    print('Username and Password are used to login to DEN.')
    print('Course is the name of the course to download. e.g.: Course=\'CSCI567\'')


driver = webdriver.Chrome()
driver.get("https://courses.uscden.net/d2l/login")
wait(page_has_loaded, 10)

userName = driver.find_element_by_name('userName')
passwd = driver.find_element_by_name('password')
button = driver.find_element_by_css_selector("a.d2l-button")
userName.clear()
passwd.clear()
userName.send_keys(str(sys.argv[1]))
passwd.send_keys(str(sys.argv[2]))
button.send_keys(Keys.RETURN)

wait(page_has_loaded, 10)
try:
    course = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, str(sys.argv[3])))
    )
except TimeoutException:
    raise
course.click()    

wait(page_has_loaded, 10)
try:
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Content"))
    )
except TimeoutException:
    raise
content.click()

wait(page_has_loaded, 10)
try:
    toc = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.d2l-le-TreeAccordionItem-anchor"))
    )
except TimeoutException:
    raise
toc[2].click()

wait(page_has_loaded, 10)
time.sleep(5)
links = driver.find_elements_by_css_selector("a.d2l-link-main")

link_hrefs = []
for link in links:
    link_hrefs.append(link.get_attribute("href"))
    print(link.get_attribute("href"))

for href in link_hrefs:
    driver.get(href)
    time.sleep(10)
    iframe = driver.find_elements_by_css_selector("iframe.d2l-iframe")
    if len(iframe) == 0:
        continue
        
    driver.switch_to_frame(iframe[0])    
    while True:
        try:
            body = driver.find_element_by_tag_name("body")
            videos = body.find_elements_by_css_selector("a.DENVideo")
        except NoSuchElementException:
            time.sleep(5)
            continue
        break

    for video in videos:
        if video.text.find("Android") != -1:
            video_url = video.get_attribute('href')
            print(video.get_attribute('href'))
            download(video_url)
    
driver.close()

