from selenium import webdriver
import time
import globall

url = "https://whereispost.com/seller/#/"
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
html = driver.page_source
input_text = driver.find_element_by_xpath("//*[@id='keyword']")
input_btn = driver.find_element_by_xpath("/html/body/content/div/div[2]/div[1]/div/div/div/div/form/button")
#keyword_copy_start_btn = driver.find_element_by_xpath("//*[@id='relkey_on']/h2/span/i")
#keyword_real_copy_btn = driver.find_element_by_xpath("//*[@id='myModal']/div/div[1]/span")
keyword_list = driver.find_elements_by_xpath("//*[@id='relkey']")

input_text.send_keys('치마')
driver.implicitly_wait(1)
input_btn.click()
#for로 LI의 개수만큼 클릭을 해야함


for x in range(1,100):
    num = "{}".format(x)
    keyword = driver.find_element_by_xpath("//*[@id='relkey']/li["+num+"]/a")
    keyword.click()
    time.sleep(0.5)

#//*[@id="relkey"]/li[1]/a
#//*[@id="relkey"]/li[2]/a




