import requests
from bs4 import BeautifulSoup
import os
import re
directory =  r"your_directory"#directory where you've saved all txt files using final.py file
cookies = {'your_cookie'}
session = requests.Session()
session.cookies.update(cookies)
for file_name in os.listdir(directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
            txtlink = re.findall(r"https://4books.com/\S+", contents)
            link = txtlink[0] + '/capitolo/2'
            print(link)
            page = session.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, "html.parser")
            with open(file_path, "a", encoding="utf-8") as txtfile:
                for f in soup.find_all('div', class_='book-chapter'):
                    if f.find('h2', class_='book-chapter-title book-margin'):
                        title = f.find('h2', class_='book-chapter-title book-margin').text.strip()
                        if f.find('div', class_='book-chapter-body'):
                            summary = f.find('div', class_='book-chapter-body').text.strip()
                            txtfile.write(f"\n{title}\n\n")
                            txtfile.write(f"{summary}\n")
    