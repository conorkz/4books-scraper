from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import requests
import os
directory = r'your_directory'
roi = 'no info on the website'
url = 'https://4books.com/en/home'
pag = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
sou = BeautifulSoup(pag.content, "html.parser")
for h in sou.find(class_='col only-desktop-flex categories-wrap-desk').find_all('a'):
    url = 'https://4books.com'+ h['href']
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    time.sleep(5)
    while True:
        try:
            ss = driver.find_element(By.CSS_SELECTOR, '.fg-primary')
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fg-primary')))
            driver.execute_script("arguments[0].click();",ss)
            time.sleep(2)
        except:
            break
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for b in soup.find_all(class_='smallcard cme col-6 col-md-3'):
        cover = b.find('img', class_='card-img-top')['src']
        link = 'https://4books.com' + b.find('a')['href']
        author = b.find(class_='f10-700').text.strip()
        title = b.find('h3', class_='f16-700').text.strip()
        catch = b.find(class_='f14-f12-400').text.strip()
        page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        sorpa = BeautifulSoup(page.content, "html.parser")
        if sorpa.find(class_='row button-row text-center mb-4'):
            descrip = sorpa.find(class_='row button-row text-center mb-4').find_previous().find_previous('p').text.strip()
        else:
            descrip = roi
        if sorpa.find('span', string=re.compile('Read in \d+ min')):
            trt = sorpa.find('span', string=re.compile('Read in \d+ min')).get_text()
            read = re.findall(r'\d+', trt)[0]
        else:
            read = roi
        if sorpa.find('span', string=re.compile('Listen in \d+ min')):
            trta = sorpa.find('span', string=re.compile('Listen in \d+ min')).get_text()
            listen = re.findall(r'\d+', trta)[0]
        else:
            listen = roi
        if sorpa.find('h4', class_='stronger', string='The author of the book:'):
            about = sorpa.find('h4', class_='stronger', string='The author of the book:').find_next('p').text.strip()
        else:
            about = roi
        bf = re.sub(r"[^\w\s]", "", title)
        berl = pytz.timezone('Europe/Berlin')
        current_time = datetime.now(berl)
        berlin = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        file_name = os.path.join(directory, f"{bf}.txt")
        suffix = 1
        while os.path.exists(file_name):
            file_name = os.path.join(directory, f"{bf} ({suffix}).txt")
            suffix += 1
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n")
            file.write(f"Author: {author}\n")
            file.write(f"Catchline: {catch}\n")
            file.write(f"Link: {link}\n")
            file.write(f"Book cover: {cover}\n")
            file.write(f"Berlin time: {berlin}\n")
            file.write(f"About the author: {about}\n")
            file.write(f"Time to read(in minutes): {read}\n")
            file.write(f"Time to listen(in minutes): {listen}\n")
            file.write(f"Description: {descrip}\n")
            file.write("Many useful tips to:\n")
            if sorpa.find('h4', class_='stronger', string='Many useful tips to:'):
                for g in sorpa.find('h4', class_='stronger', string='Many useful tips to:').find_next('ul').find_all('li'):
                    file.write(g.text + "\n")
            else:
                file.write(roi + "\n")
        
    
    
    
    
    

