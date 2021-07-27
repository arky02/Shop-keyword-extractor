# 멀티로 빠르게 뽑기 - 500개 한번에
# 네이버 카테고리 조정해서 쓰기
# need to modify : cat1, cat2

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
chracters = "/\?"


# 0으로 하면 건너뜀.


def naverShoppingDatalab():
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

    # 첫번째 카테고리 선택 - *str(): 선택하고자 하는 카테고리의 list index
    cate1 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span")
    cate1.click()
    cat1_address = "//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[" + str(Global.cat1) + "]/a"
    category1 = driver.find_element_by_xpath(cat1_address)  # 첫번째 분야에 원하는 목록위치!!!!!!!
    Global.cat1_name = category1.text
    category1.click()

    try:
        # 두번째 카테고리 선택
        cate2 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span")
        cate2.click()
        cat2_address = "//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[" + str(
            Global.cat2) + "]/a"
        category2 = driver.find_element_by_xpath(cat2_address)  # 두번째 분야에 원하는 목록위치!!!!!!!!!!
        Global.cat2_name = category2.text
        category2.click()
    except Exception as E:
        Global.cat1 += 1
        Global.cat2 = 1
        Global.cat3 = 1
        Global.cat4 = 1
        naverShoppingDatalab()

    # 세번째 카테고리 선택
    if Global.cat3 != 0:
        try:
            cate3 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span")
            cate3.click()
            cat3_adress = "//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[" + str(Global.cat3) + "]/a"
            category3 = driver.find_element_by_xpath(cat3_adress)  # 세번째 분야에 원하는 목록위치!!!!!!!
            Global.cat3_name = category3.text
            category3.click()
        except Exception as E:
            Global.cat2 += 1
            Global.cat3 = 1
            Global.cat4 = 1
            naverShoppingDatalab()

    # 네번째 카테고리 선택
    if Global.cat4 != 0:
        try:
            cate4 = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[4]/span")
            cate4.click()
            cat4_adress = "//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[4]/ul/li[" + str(
                Global.cat4) + "]/a"
            category4 = driver.find_element_by_xpath(cat4_adress)  # 세번째 분야에 원하는 목록위치!!!!!!!
            Global.cat4_name = category4.text
            category4.click()
            getNaverTop500List(driver, True)
            Global.cat4 += 1
            Global.isFirst = True
            naverShoppingDatalab()

        except Exception as e:
            print("no cat4")
            getNaverTop500List(driver, False)


def getNaverTop500List(driver, isCat4Exist):
    btn = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/a")
    btn.click()

    while True:
        time.sleep(0.5)

        pagenum = driver.find_element_by_xpath(
            "//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em").text
        rank_list = driver.find_elements_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li")

        for x in rank_list:
            item_num, item_name = x.find_element_by_tag_name('a').text.split('\n')  # ['숫자','이름']

            for y in range(len(chracters)):
                item_name = item_name.replace(chracters[y], "")

            top500_list[item_num] = item_name

        # TODO 2(2). 1-25페이지 end 범위정하기(12/13: 1-12/13-25)
        if int(pagenum) == 25:
            print("top500list: ")
            print(top500_list)
            driver.close()
            # os.system("python singlemode.py")
            helpstore(top500_list, isCat4Exist)
            break

        driver.find_element_by_class_name('btn_page_next').click()


def helpstore(top500list, isCat4Exist):
    # 스마트스토어에서 톱500키워드 뽑은거 헬프스토어로 넘김
    # 헬프스토어
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
    print(len(top500list))  # 네이버 톱500리스트-딕셔너리형태
    top500_valuelist = list(top500list.values())
    # 벨류리스트: 네이버 톱500리스트의 키워드이름만(500개 딕셔너리형태에서 벨류추출)
    print(top500_valuelist)
    for y in range(1, len(top500list)):  # 딱 저기 끝이 되면 딱 꺼지는건가?그런거같아보임. 딱 끝이되면 나가짐 실행안되고,, 미만인건가??궁금하네
        # if (didWorkWell == False):
        #    time.sleep(7)

        print(y)  # 만약 20개면 y가 19까지는 프린트 되어야함
        # didWorkWell = False

        # [0]으로 넘어감
        driver.switch_to.window(driver.window_handles[0])
        try:
            result = driver.switch_to.alert()
            result.accept()
            result.dismiss()

        except:
            "There is no alert"
        driver.implicitly_wait(1)
        # 기존의 입력칸 지우고 톱500 단어리스트 하나하나씩 입력 - 싱글모드
        if Global.isFirst:
            input_text.clear()
            input_text.send_keys(top500_valuelist[0])  # 톱오백키워드입력칸
            input_btn.click()
            driver.implicitly_wait(3)
            time.sleep(8)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='shoppingKeywordCopy']")))
            # getRelWordLists
            relword_words = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']").text
            relword_list = relword_words.split()
            # relword_list: 톱500상품이름 검색했을 때 연관검색어들 리스트목록
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[@id='q']").clear()
            driver.find_element_by_xpath("//*[@id='q']").send_keys(top500_valuelist[1])  # 톱오백키워드입력칸
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
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='shoppingKeywordCopy']")))
            relword_words = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']").text
            relword_list = relword_words.split()  # relword_list: 톱500상품이름 검색했을 때 연관검색어들 리스트목록

            # 로딩이 다 되었는지 확인
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[@id='q']").clear()
            driver.find_element_by_xpath("//*[@id='q']").send_keys(top500_valuelist[y])  # 톱오백키워드입력칸
            input_btn.click()

        # 여기서부터는 이제 멀티로 키워드 한번에 입력 코드
        driver.switch_to.window(driver.window_handles[1])
        # driver.switch_to_window(driver.window_handles[1])
        input_relwordlist = driver.find_element_by_xpath("//*[@id='q']")  # 멀티 키워드 뽑는페이지의 텍스트 입력칸

        for a in range(0, int(len(relword_list))):
            if (a == int(len(relword_list))):
                # didWorkWell = True
                driver.switch_to.window(driver.window_handles[0])
                break
            input_relwordlist.send_keys(relword_list[a])
            driver.find_element_by_xpath("//*[@id='searchBtn']").click()
            input_relwordlist.clear()

        if y % 5 == 0 or y == (int(len(top500list))-1):
            for a in range(1, 10000):
                try:
                    num = "{}".format(a)
                    stats = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[7]").text
                    click = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[5]").text
                    if float(stats) < 15.00 and click.find(',') != -1:
                        name = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[2]").text
                        amount = driver.find_element_by_xpath("//*[@id='dataList']/tr[" + num + "]/td[6]").text
                        if name not in Global.keyWordList_final:
                            Global.keyWordList_final.append(name)  # 최종리스트에저장. 필터링 다 거친 단어/경쟁강도/클릭수: 키!
                            Global.keyStatsList_final.append(stats)
                            Global.keyClickList_final.append(click)
                            Global.keyAmountList_final.append(amount)

                except Exception as e:
                    driver.refresh()
                    driver.switch_to.window(driver.window_handles[0])
                    print("Global.keyWordList_final")
                    print(Global.keyWordList_final)
                    # 필터링까지 마친 최종리스트 3개!
                    break
        driver.switch_to.window(driver.window_handles[0])

        if y == (int(len(top500list))-1):
            print("end")

            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(Global.keyWordList_final)
            sheet.append(Global.keyClickList_final)
            sheet.append(Global.keyStatsList_final)
            sheet.append(Global.keyAmountList_final)

            if not isCat4Exist:
                categoryName = { Global.cat1_name,  Global.cat2_name, Global.cat3_name, "(4번째 카테고리 X)"}
                sheet.append(list(categoryName))
                save_name = str(Global.cat1) + '-' + str(Global.cat2) + '-' + str(Global.cat3) + '.xlsx'
                Global.cat3 += 1
                Global.cat4 = 1
            else:
                categoryName = {Global.cat1_name, Global.cat2_name, Global.cat3_name, Global.cat4_name}
                sheet.append(list(categoryName))
                save_name = str(Global.cat1) + '-' + str(Global.cat2) + '-' + str(Global.cat3) + '-' + str(
                    Global.cat4) + '.xlsx'

            wb.save(save_name)
            driver.quit()

for _ in range(1, 15):
    naverShoppingDatalab()
    Global.isFirst = True
    time.sleep(10)

# //*[@id="keywordBox"]
