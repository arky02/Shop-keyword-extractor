# 멀티로 빠르게 뽑기
#네이버 카테고리 조정만 해서 쓰면 됨!
#조정해야할 것 : mode, cat1, cat2

from selenium import webdriver
import time
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import Global
import os

top500_list = {}
global last_x
#cat1-cat2(mode) 형태로 저장됨
cat1 = 0
cat2 = 0
mode = 0

#TODO 내일  didWorkWell불리언 만들어서 로딩안되서 그냥 막 넘어가는거 제대로 work안된거면  sleep하도록 하기
def smartstore():

    # 스마트스토어
    url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # DRIVER_PATH = './user/PycharmProjects/pythonProject/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    chracters = "/\?"

    if mode == 1:
        pagenum_mode = 12
    else:
        pagenum_mode = 25

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

    #TODO 1. 카테고리체인지
    #*** 첫번째 카테고리 - 맨마지막 li[] 부분만 바꾸면됨. list index(순서에맞춰서)
    cat1_address = "//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li["+str(cat1)+"]/a"
    category1 = driver.find_element_by_xpath(cat1_address)  # 첫번째 분야에 원하는 목록위치!!!!!!!
    category1.click()
    cate2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span") #두번째 카테고리 선택위해 누르기
    cate2.click()
    #*** 두번째 카테고리 - 맨마지막 li[] 부분만 바꾸면됨. list index(순서에맞춰서)
    cat2_address = "//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li["+str(cat2)+"]/a"
    category2 = driver.find_element_by_xpath(cat2_address)  # 두번째 분야에 원하는 목록위치!!!!!!!!!!
    category2.click()
    #cate3 = driver.find_element_by_xpath("//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span") #세번째 카테고리 선택위해 누르기
    #cate3.click()
    #*** 세번째 카테고리 - 맨마지막 li[] 부분만 바꾸면됨. list index(순서에맞춰서)
    #category3 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li["+cate3+"]/a")  # 세번째 분야에 원하는 목록위치!!!!!!!
    #category3.click()
    btn = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/a")
    btn.click()

    #TODO 2(1). 1-25페이지 start 범위정하기(12/13: 1-12/13-25)
    if mode == 2:
        start_btn = driver.find_element_by_xpath("//*[@id ='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]")
        for x in range(1, 14):  # 건너 뛸 곳/ 처음(1-12)일때: 주석처리하기, 두번째(13-25)일때: range(1,13)
            time.sleep(0.1)
            start_btn.click()

    while True:
        time.sleep(0.5)

        pagenum = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em").text
        rank_list = driver.find_elements_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li")  # 아직까지는 아나ㅣㅁ

        for x in rank_list:
            item_num, item_name = x.find_element_by_tag_name('a').text.split('\n')  # ['숫자','이름']

            for y in range(len(chracters)):
                item_name = item_name.replace(chracters[y], "")

            top500_list[item_num] = item_name

        # TODO 2(2). 1-25페이지 end 범위정하기(12/13: 1-12/13-25)
        if (int(pagenum) == pagenum_mode): #첫번째: 12, 두번째: 25
            print(top500_list)
            driver.close()
            # os.system("python helpstore.py")
            helpstore(top500_list)
            break

        driver.find_element_by_class_name('btn_page_next').click()

def helpstore(top500list):
    #스마트스토어에서 톱500키워드 뽑은거 헬프스토어로 넘김
    #헬프스토어
    global relword_list
    didWorkWell = True
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
    input_btn = driver.find_element_by_xpath("//*[@id='searchBtn']")
    print(len(top500list)) #네이버 톱500리스트-딕셔너리형태
    top500_valuelist = list(top500list.values())
    #벨류리스트: 네이버 톱500리스트의 키워드이름만(500개 딕셔너리형태에서 벨류추출)
    print(top500_valuelist)
    for y in range(0, len(top500list)-1):#딱 저기 끝이 되면 딱 꺼지는건가?그런거같아보임. 딱 끝이되면 나가짐 실행안되고,, 미만인건가??궁금하네
        #if (didWorkWell == False):
        #    time.sleep(7)

        print(y)  # 만약 20개면 y가 19까지는 프린트 되어야함
        #didWorkWell = False

        #[0]으로 넘어감
        driver.switch_to.window(driver.window_handles[0])
        try:
            result = driver.switch_to.alert()
            result.accept()
            result.dismiss()

        except:
            "There is no alert"
        driver.implicitly_wait(1)
        #기존의 입력칸 지우고 톱500 단어리스트 하나하나씩 입력 - 싱글모드
        if Global.isFirst:
            input_text.clear()
            input_text.send_keys(top500_valuelist[y])  # 톱오백키워드입력칸
            input_btn.click()
            driver.implicitly_wait(3)
            time.sleep(8)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='shoppingKeywordCopy']")))
            # getRelWordLists
            relword_words = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']").text
            relword_list =  relword_words.split()
            # relword_list: 톱500상품이름 검색했을 때 연관검색어들 리스트목록
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[@id='q']").clear()
            driver.find_element_by_xpath("//*[@id='q']").send_keys(top500_valuelist[y+1])  # 톱오백키워드입력칸
            input_btn.click()
            driver.execute_script('window.open("http://helpstore.shop/mkeyword");')
            driver.switch_to.window(driver.window_handles[1])
            Global.isFirst = False
            time.sleep(0.5)
            driver.implicitly_wait(3)
            popup_btn = driver.find_element_by_xpath("//*[@id='btnHelpNeverShow']")
            popup_btn.click()

        else:
            time.sleep(2)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='shoppingKeywordCopy']")))
            relword_words = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']").text
            relword_list = relword_words.split()  # relword_list: 톱500상품이름 검색했을 때 연관검색어들 리스트목록

                #로딩이 다 되었는지 확인
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[@id='q']").clear()
            driver.find_element_by_xpath("//*[@id='q']").send_keys(top500_valuelist[y+1])  # 톱오백키워드입력칸
            input_btn.click()

#여기서부터는 이제 멀티로 키워드 따다닥 입력 코드


        driver.switch_to.window(driver.window_handles[1])
        # driver.switch_to_window(driver.window_handles[1])
        input_relwordlist = driver.find_element_by_xpath("//*[@id='q']")#멀티 키워드 뽑는페이지의 텍스트 입력칸

        for a in range(0, int(len(relword_list)) - 1):
            if (a == int(len(relword_list) - 1)):
                #didWorkWell = True
                driver.switch_to.window(driver.window_handles[0])
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
                        amount = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[6]").text
                        if name not in Global.keyWordList_final:
                            Global.keyWordList_final.append(name) #최종리스트에저장. 필터링 다 거친 단어/경쟁강도/클릭수: 키!
                            Global.keyStatsList_final.append(stats)
                            Global.keyClickList_final.append(click)
                            Global.keyAmountList_final.append(amount)

                except Exception as e:
                    driver.refresh()
                    driver.switch_to.window(driver.window_handles[0])
                    print(Global.keyWordList_final)
                    # 필터링까지 마친 최종리스트 3개!
                    break
        driver.switch_to.window(driver.window_handles[0])

        if y == (int(len(top500list))-2):
            print("end")
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(Global.keyWordList_final)
            sheet.append(Global.keyClickList_final)
            sheet.append(Global.keyStatsList_final)
            sheet.append(Global.keyAmountList_final)
            save_name = str(cat1)+'-'+str(cat2)+'('+str(mode)+').xlsx'
            wb.save(save_name)




smartstore()
# //*[@id="keywordBox"]
