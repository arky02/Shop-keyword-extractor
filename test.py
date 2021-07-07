# 멀티로 빠르게 뽑기
#네이버 카테고리 조정만 해서 쓰면 됨!
from selenium import webdriver
import time
import pandas as pd
import openpyxl
import numpy
from pandas import DataFrame
from pandas import Series
from pandas import ExcelFile
from pandas import concat
from pandas import merge
import xlwt

from selenium.webdriver.support.wait import WebDriverWait

import Global
import os

top500_list = {"파자마"}
global last_x


def smartstore():
    # 스마트스토어
    url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # DRIVER_PATH = './user/PycharmProjects/pythonProject/chromedriver_win32/chromedriver.exe'

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    try:
        result = driver.switch_to.alert()
        result.accept()
        result.dismiss()

    except:
        "There is no alert"
    html = driver.page_source
    driver.maximize_window()
    cate1 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span") #첫번째 카테고리 선택위해 누르기
    cate1.click()
    #*** 첫번째 카테고리 - 맨마지막 li[] 부분만 바꾸면됨. list index(순서에맞춰서)
    category1 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[1]/a")  # 첫번째 분야에 원하는 목록위치!!!!!!!
    category1.click()
    cate2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span") #두번째 카테고리 선택위해 누르기
    cate2.click()
    #*** 두번째 카테고리 - 맨마지막 li[] 부분만 바꾸면됨. list index(순서에맞춰서)
    category2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[2]/a")  # 두번째 분야에 원하는 목록위치!!!!!!!!!!
    category2.click()
    #cate3 = driver.find_element_by_xpath("//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span") #세번째 카테고리 선택위해 누르기
    #cate3.click()
    #*** 세번째 카테고리 - 맨마지막 li[] 부분만 바꾸면됨. list index(순서에맞춰서)
    #category3 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[1]/a")  # 세번째 분야에 원하는 목록위치!!!!!!!
    #category3.click()
    btn = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/a")
    btn.click()

    while True:
        time.sleep(0.5)

        pagenum = driver.find_element_by_xpath(
            "//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em").text
        rank_list = driver.find_elements_by_xpath(
            "//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li")  # 아직까지는 아나ㅣㅁ

        for x in rank_list:
            item_num, item_name = x.find_element_by_tag_name('a').text.split('\n')  # ['숫자','이름']
            top500_list[item_num] = item_name

        if (int(pagenum) == 1):
            print(top500_list)
            driver.close()
            # os.system("python helpstore.py")
            helpstore(top500_list)
            break

        driver.find_element_by_class_name('btn_page_next').click()


def helpstore():
    #스마트스토어에서 톱500키워드 뽑은거 헬프스토어로 넘김
    #헬프스토어
    global relword_list
    url = "http://helpstore.shop/"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    try:
        result = driver.switch_to.alert()
        result.accept()
        result.dismiss()

    except:
        "There is no alert"
    html = driver.page_source
    driver.maximize_window()

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
    time.sleep(0.5)
    driver.implicitly_wait(3)
    popup_btn = driver.find_element_by_xpath("//*[@id='btnHelpNeverShow']")
    popup_btn.click()
    # keyword_copy_start_btn = driver.find_element_by_xpath("//*[@id='relkey_on']/h2/span/i")
    # keyword_real_copy_btn = driver.find_element_by_xpath("//*[@id='myModal']/div/div[1]/span")
    input_text = driver.find_element_by_xpath("//*[@id='q']")
    input_btn = driver.find_element_by_xpath("//*[@id='searchBtn']") #벨류리스트: 네이버 톱500리스트의 키워드이름만(500개 딕셔너리형태에서 벨류추출)

    driver.switch_to.window(driver.window_handles[0])
    driver.implicitly_wait(1)
        #기존의 입력칸 지우고 톱500 단어리스트 하나하나씩 입력 - 싱글모
    input_text.send_keys("파자마")  # 톱오백키워드입력칸
    input_btn.click()
    time.sleep(0.5)
    relword_words = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']").text
    relword_list = relword_words.split()
    print(relword_list)
    print(len(relword_list))




helpstore()
# //*[@id="keywordBox"]
