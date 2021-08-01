

from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup as BS
from selenium import webdriver

keyword = input("Image Name : ")
i_URL = f'https://www.google.com/search?q={quote_plus(keyword)}&sxsrf=ALeKk00OQamJ34t56QSInnMzwcC5gC344w:1594968011157&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjXs-7t1tPqAhVF7GEKHfM4DqsQ_AUoAXoECBoQAw&biw=1536&bih=754'

driver=webdriver.Chrome('chromedriver.exe') #크롬 드라이버
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver.get(i_URL)

html = driver.page_source
soup = BS(html,features="html.parser")

img = soup.select('img')

i_list = []
count = 1

print("Searching...")
for i in img:
   try:
      i_list.append(i.attrs["src"])
   except KeyError:
      i_list.append(i.attrs["data-src"])

print("Downloading...")
for i in i_list:
   urlretrieve(i,"download/"+keyword+str(count)+".jpg")
   count+=1

driver.close()
print("FINISH")

