from selenium import webdriver
import time
import Global

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
popup_btn = driver.find_element_by_xpath("//*[@id='btnHelpNeverShow']")
popup_btn.click()
#keyword_copy_start_btn = driver.find_element_by_xpath("//*[@id='relkey_on']/h2/span/i")
#keyword_real_copy_btn = driver.find_element_by_xpath("//*[@id='myModal']/div/div[1]/span")
input_text = driver.find_element_by_xpath("//*[@id='q']")
input_btn = driver.find_element_by_xpath("//*[@id='searchBtn']")
print(Global.top500_list)
print(len(Global.top500_list))

for y in range(1, len(Global.top500_list)):


    input_text.send_keys(Global.top500_list[y])
    driver.implicitly_wait(1)
    input_btn.click()
    driver.implicitly_wait(5)

    Global.word_list[0] = driver.find_element_by_xpath("//*[@id='keywordBox']").text
    Global.statistics_list[0] = driver.find_element_by_xpath("//*[@id='rate']").text
    #for로 LI의 개수만큼 클릭을 해야함

    for x in range(1,100):
        try:
            num = "{}".format(x)
            keyword = driver.find_element_by_xpath("//*[@id='shoppingKeywordLayer']/span["+num+"]")
            Global.word_list[x + 1] = keyword.text
            #print(globall.word_list[x+1])
            keyword.click()
            time.sleep(3)
            driver.switch_to_window(driver.window_handles[1])
            Global.statistics_list[x + 1] = driver.find_element_by_xpath("//*[@id='rate']").text
            #print(globall.statistics_list[x+1])
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            #globall.word_list[x] = driver.find_element_by_xpath("//*[@id='keywordBox']").text

        except Exception as e:
            print(Global.word_list)
            print(Global.statistics_list)
            break

#//*[@id="relkey"]/li[1]/a
#//*[@id="relkey"]/li[2]/a




