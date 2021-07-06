# 멀티로 빠르게 뽑기
#네이버 카테고리 조정만 해서 쓰면 됨!
from selenium import webdriver
from selenium.webdriver import ActionChains
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

import globall
import os

top500_list = {}
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
    category2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[1]/a")  # 두번째 분야에 원하는 목록위치!!!!!!!!!!
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

        if (int(pagenum) == 25):
            print(top500_list)
            driver.close()
            # os.system("python helpstore.py")
            helpstore(top500_list)
            break

        driver.find_element_by_class_name('btn_page_next').click()


def helpstore(top500list):
    #스마트스토어에서 톱500키워드 뽑은거 헬프스토어로 넘김
    #헬프스토어
    url = "http://helpstore.shop/"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
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
    input_btn = driver.find_element_by_xpath("//*[@id='searchBtn']")
    print(len(top500list)) #네이버 톱500리스트-딕셔너리형태
    value = top500list.values()
    top500_valuelist = list(value) #벨류리스트: 네이버 톱500리스트의 키워드이름만(500개 딕셔너리형태에서 벨류추출)

    for y in range(0, len(top500list)):#딱 저기 끝이 되면 딱 꺼지는건가?그런거같아보임. 딱 끝이되면 나가짐 실행안되고,, 미만인건가??궁금하네
        print(y)#만약 20개면 y가 19까지는 프린트 되어야함

        driver.switch_to_window(driver.window_handles[0])
        driver.implicitly_wait(1)
        driver.find_element_by_xpath("//*[@id='q']").clear()
        input_text.send_keys(top500_valuelist[y])#톱오백키워드입력칸
        input_btn.click()
        driver.implicitly_wait(3)
        time.sleep(8)

        relword_words = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']").text
        # print(keyword_words)
        relword_list = relword_words.split()#relword_list: 톱500상품이름 검색했을 때 연관검색어들 리스트목록
        if globall.isFirst:
            driver.execute_script('window.open("http://helpstore.shop/mkeyword");')
            driver.switch_to_window(driver.window_handles[1])
            globall.isFirst = False
            time.sleep(0.5)
            driver.implicitly_wait(3)
            popup_btn = driver.find_element_by_xpath("//*[@id='btnHelpNeverShow']")
            popup_btn.click()

        driver.switch_to_window(driver.window_handles[1])
        # driver.switch_to_window(driver.window_handles[1])
        input_relwordlist = driver.find_element_by_xpath("//*[@id='q']")#멀티 키워드 뽑는페이지의 텍스트 입력칸

        for a in range(0, int(len(relword_list)) - 1):
            if (a == int(len(relword_list) - 1)):
                driver.switch_to_window(driver.window_handles[0])
                break
            input_relwordlist.send_keys(relword_list[a])
            driver.find_element_by_xpath("//*[@id='searchBtn']").click()
            input_relwordlist.clear()

        if (y+1) % 5 == 0 and y != 0:
            for a in range(1, 10000):
                try:
                    num = "{}".format(a)
                    stats = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[7]").text
                    click = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[5]").text
                    if float(stats) < 15.00 and click.find(',')!= -1:
                        name = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[2]").text
                        if name not in globall.keywordlist_final:
                            globall.keywordlist_final.append(name) #최종리스트에저장. 필터링 다 거친 단어/경쟁강도/클릭수: 키!
                            globall.keystatslist_final.append(stats)
                            globall.keyclicklist_final.append(click)
                            #print(globall.keywordlist_final)

                except Exception as e:
                    driver.refresh()
                    driver.switch_to_window(driver.window_handles[0])
                    print(globall.keywordlist_final)
                    # 필터링까지 마친 최종리스트 3개!
                    break

        # print(relword_list)
        driver.switch_to_window(driver.window_handles[0])
        # SetList2 = set(relword_list)
        # SetList1 = set(globall.keywordlist_final)
        # difference = list(SetList2.difference(SetList1))
        # globall.keywordlist_final = globall.keywordlist_final+difference
        # print(globall.keywordlist_final)
        # for로 LI의 개수만큼 클릭을 해야함

        if y == (int(len(top500list))-1):
            print("end")
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(globall.keywordlist_final)
            sheet.append(globall.keyclicklist_final)
            sheet.append(globall.keystatslist_final)
            wb.save('keyword_list.xlsx')




smartstore()
# //*[@id="keywordBox"]
