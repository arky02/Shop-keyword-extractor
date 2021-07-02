from selenium import webdriver
import time
import globall
import os

#스마트스토어
url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
#DRIVER_PATH = './user/PycharmProjects/pythonProject/chromedriver_win32/chromedriver.exe'

driver = webdriver.Chrome()

driver.implicitly_wait(3)
driver.get(url)
html = driver.page_source

while True:
    time.sleep(0.5)
    pagenum = driver.find_element_by_xpath(
        "//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em").text
    rank_list = driver.find_elements_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li") #아직까지는 아나ㅣㅁ

    for x in rank_list:
        item_num,item_name = x.find_element_by_tag_name('a').text.split('\n')    #['숫자','이름']
        globall.top500_list[item_num] = item_name

    if(int(pagenum) ==25):
        print(globall.top500_list)
        driver.close()
        os.system("python helpstore.py")
        break

    driver.find_element_by_class_name('btn_page_next').click()



