#메인 파일
from selenium import webdriver
import time
import pandas as pd
import openpyxl
import numpy
from pandas import  DataFrame
from pandas import Series
from pandas import ExcelFile
from pandas import concat
from pandas import  merge
import xlwt

from selenium.webdriver.support.wait import WebDriverWait

import globall
import os

top500_list ={}
global last_x

def smartstore():
    #스마트스토어
    url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
    header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    #DRIVER_PATH = './user/PycharmProjects/pythonProject/chromedriver_win32/chromedriver.exe'

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    html = driver.page_source
    cate1 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span")
    cate1.click()
    category1 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[2]/a")  # 첫번째 분야에 원하는 목록위치!!!!!!!
    category1.click()
    cate2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span")
    cate2.click()
    category2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[6]/a")  # 두번째 분야에 원하는 목록위치!!!!!!!!!!
    category2.click()
    cate3 = driver.find_element_by_xpath("//*[@ id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span")
    cate3.click()
    category3 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[1]/a")  # 세번째 분야에 원하는 목록위치!!!!!!!
    category3.click()

    while True:
        time.sleep(0.5)

        pagenum = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em").text
        rank_list = driver.find_elements_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li") #아직까지는 아나ㅣㅁ

        for x in rank_list:
            item_num,item_name = x.find_element_by_tag_name('a').text.split('\n')    #['숫자','이름']
            top500_list[item_num] = item_name

        if(int(pagenum) ==1):
            print(top500_list)
            driver.close()
            #os.system("python helpstore.py")
            helpstore(top500_list)
            break

        driver.find_element_by_class_name('btn_page_next').click()


def helpstore(wordlist):
    last_x= 1
    url = "http://helpstore.shop/"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    html = driver.page_source

    login_btn = driver.find_element_by_xpath("/html/body/div[1]/header/nav/div/ul/li[1]/a[2]")
    login_btn.click()
    id_input = driver.find_element_by_xpath("//*[@id='loginId']")
    id_input.send_keys('nanjin2ya')
    pw_input = driver.find_element_by_xpath("//*[@id='loginPw']")
    pw_input.send_keys('jj123@')
    enter_btn = driver.find_element_by_xpath("//*[@id='btnLogin']")
    enter_btn.click()
    keyword_search_btn = driver.find_element_by_xpath("/html/body/div[1]/aside[1]/section/ul/li[4]/a")
    keyword_search_btn.click()
    keyword_single_btn = driver.find_element_by_xpath("/html/body/div[1]/aside[1]/section/ul/li[4]/ul/li[1]/a")
    keyword_single_btn.click()
    driver.implicitly_wait(5)
    popup_btn = driver.find_element_by_xpath("//*[@id='btnHelpNeverShow']")
    popup_btn.click()
    # keyword_copy_start_btn = driver.find_element_by_xpath("//*[@id='relkey_on']/h2/span/i")
    # keyword_real_copy_btn = driver.find_element_by_xpath("//*[@id='myModal']/div/div[1]/span")
    input_text = driver.find_element_by_xpath("//*[@id='q']")
    input_btn = driver.find_element_by_xpath("//*[@id='searchBtn']")
    print(len(wordlist))
    value = wordlist.values()
    valuelist = list(value)


    for y in range(0, len(wordlist)):
        if y == len(wordlist):
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(list(globall.word_list.values()))
            sheet.append(list(globall.statistics_list.values()))
            sheet.append(list(globall.click_list.values()))
            wb.save('keyword_list.xlsx')

        driver.find_element_by_xpath("//*[@id='q']").clear()
        input_text.send_keys(valuelist[y])
        driver.implicitly_wait(1)
        input_btn.click()
        time.sleep(3)
        if(float(driver.find_element_by_xpath("//*[@id='rate']").text)<15.00 and driver.find_element_by_xpath("//*[@id='sumCount']").text.find(',')!= -1):
            globall.word_list[last_x] = driver.find_element_by_xpath("//*[@id='keywordBox']").text
            globall.statistics_list[last_x] = driver.find_element_by_xpath("//*[@id='rate']").text
            globall.click_list[last_x] = driver.find_element_by_xpath("//*[@id='sumCount']").text
            print(driver.find_element_by_xpath("//*[@id='keywordBox']").text)

        # for로 LI의 개수만큼 클릭을 해야함
        def final_input_key():
            wordd= driver.find_element_by_xpath("//*[@id='keywordBox']").text
            statisticss = driver.find_element_by_xpath("//*[@id='rate']").text
            clickk = driver.find_element_by_xpath("//*[@id='sumCount']").text

            if(float(statisticss)<15.00 and clickk.find(',')!= -1):
                print(driver.find_element_by_xpath("//*[@id='keywordBox']").text)
                globall.word_list[last_x + x] = wordd
                globall.statistics_list[last_x + x] = statisticss
                globall.click_list[last_x + x] = clickk



        for x in range(1, 100):
            try:
                num = "{}".format(x)
                keyword = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']/span[" + num + "]")
                # print(globall.word_list[x+1])
                keyword.click()
                driver.implicitly_wait(5)
                time.sleep(7)
                #wait = WebDriverWait(driver,10)
                driver.switch_to_window(driver.window_handles[1])
                # 15미만 1000 이상
                final_input_key()
                # print(globall.statistics_list[x+1])
                driver.close()
                driver.switch_to_window(driver.window_handles[0])

                # print(globall.statistics_list[x+1])

            except Exception as e:
                driver.switch_to_window(driver.window_handles[0])
                #필터링까지 마친 최종리스트 3개!
                print(list(globall.word_list.values()))
                print(list(globall.statistics_list.values()))
                print(list(globall.click_list.values()))
                last_x += int(x)
                break







smartstore()


#//*[@id="keywordBox"]







