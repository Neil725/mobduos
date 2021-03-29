import sys
sys.path.append(r'C:\Users\user\PycharmProjects\pythonProject\mobduos')
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import os , bs4 , time , threading , redis , requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import mobduos.shopee_mobduos

load_dotenv()
redis_r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_POST'), db=os.getenv('REDIS_DB'),
                            decode_responses=True)
def close_ad(driver):
    try:
        WebDriverWait(driver, 10 , 0.5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[class='el-icon-circle-close']"))).get_attribute('class')
        driver.find_element_by_class_name('el-icon-circle-close').get_attribute('class')
        driver.find_elements_by_css_selector("[class='el-icon-circle-close']")[1].click()
        print("取消廣告了")
        return "取消廣告了"
    except:
        print("沒有廣告")
        return "沒有廣告"
#####  將每個項目存入redis  目前共2024項
def Item_copy_to_redis(driver):
    time.sleep(3)
    close_ad(driver)
    hot_sale_url = 'https://shopee.mobduos.com/#/hot-search-word/hot-sales-word'
    driver.execute_script("window.open(\'{}\')".format(hot_sale_url))
    ### 移動到熱銷詞頁面
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    close_ad(driver)
    item = WebDriverWait(driver, 15).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, '//input[@class="el-input__inner"]')))
    ActionChains(driver).click(item[0]).perform()
    ## 第一層item 目前共0 ~ 21 共22項
    First_item = WebDriverWait(driver, 15).until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
    for i in First_item[0:22]:
        ActionChains(driver).move_to_element(i).perform()
        # item = driver.find_elements_by_css_selector("[class='el-scrollbar__view el-cascader-menu__list']")
        ckecks = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
        ckecks = ckecks[22::]
        for u in ckecks:
            ActionChains(driver).move_to_element(u).perform()
            item = driver.find_elements_by_css_selector("[class='el-scrollbar__view el-cascader-menu__list']")
            name = item[2].text
            third_item = name.split('\n')
            for x in third_item:
                item_name = (str(i.text)+","+str(u.text)+","+str(x))
                redis_r.rpush("hot_sales_word",item_name)
                print(item_name)
    print("掃完了")
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return "OK"

def switch_to_hot_sale_url(driver):
    driver.switch_to.window(driver.window_handles[0])
    close_ad(driver)
    hot_sale_url = 'https://shopee.mobduos.com/#/hot-search-word/hot-sales-word'
    driver.execute_script("window.open(\'{}\')".format(hot_sale_url))
    ### 移動到熱銷詞頁面
    driver.switch_to.window(driver.window_handles[1])

def To_First_Page(driver):
    Number_of_pages = driver.find_element_by_xpath("//input[@type='number']")
    Number_of_pages.clear()

def click_item(driver,hot_sales_words):
    try:
        item = WebDriverWait(driver, 15).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//input[@class="el-input__inner"]')))
        time.sleep(1)
        ActionChains(driver).click(item[0]).perform()
        time.sleep(1)
        hot_sales_word = hot_sales_words.split(",")
        hot_sales_word[0]
        hot_sales_word[1]
        hot_sales_word[2]
        time.sleep(1)
        item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
        # item = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
        for i in item:
            if i.text == hot_sales_word[0]:
                ActionChains(driver).move_to_element(i).perform()
                time.sleep(0.5)
                item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
                # item = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
                length = int(len(item))
                for j in item:
                    if j.text == hot_sales_word[1]:
                        ActionChains(driver).move_to_element(j).perform()
                        time.sleep(0.5)
                        item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
                        # item = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
                        item = item[length::]
                        for k in item:
                            if k.text == hot_sales_word[2]:
                                ActionChains(driver).click(k).perform()
                                break
                        break
                break
        To_First_Page(driver)
        time.sleep(2)
        return '"類目":"{0}>{1}>{2}"'.format(hot_sales_word[0],hot_sales_word[1],hot_sales_word[2])
    except Exception as e :
        driver.refresh()
        print("找不到 項目")
        print(e)
        redis_r.lpush("hot_sales_word",hot_sales_words)

def hot_sales_word_data(driver,item_name):
    # if driver.find_element_by_class_name("el-loading-spinner"):

    driver.execute_script("document.body.style.zoom='0.1'")
    time.sleep(1)
    hot_word_data_table = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-table__row']")))
    # hot_word_data_table = driver.find_elements_by_css_selector("[class='el-table__row']") ## 關鍵字的數據
    # hot_word_data_table
    if len(hot_word_data_table) == 0:
        print("無資料")
        # return "無資料"
    # time.sleep(1)
    splitline = int(len(hot_word_data_table) / 2)
    hot_word_data = hot_word_data_table[0:splitline] ## 關鍵字的數據
    hot_word_heards = hot_word_data_table[splitline::] ## 熱銷詞的關鍵字
    for data, h in zip(hot_word_data, hot_word_heards):
        datas = data.text.split('\n')
        if len(datas) == 11 :
            datas.insert(7, "無資料")
        datajson = '{{{13},' \
        '"熱搜詞":"{0}",' \
        '"近一日銷量(pcs)":"{1}",' \
        '"近一周銷量(pcs)":"{2}",'\
        '"近30日銷量(pcs)":"{3}",'\
        '"近30日銷售額(NT$)":"{4}",'\
        '"近30日銷量增長率":"{5}",'\
        '"產品基數":"{6}",'\
        '"產品動銷率":"{7}",'\
        '"搜索量":"{8}",'\
        '"推薦出價":"{9}",'\
        '"累積點讚數":"{10}",'\
        '"累積評論數":"{11}",'\
        '"操作":"{12}",'\
        '}}'.format(h.text,datas[0],datas[1],datas[2],datas[3],datas[4],datas[5],datas[6],
                    datas[7],datas[8],datas[9],datas[10],datas[11],item_name)
        redis_r.rpush("hot_sales_word_datas",datajson)
    return datajson

def open_new_hot_sales(driver,redis_r,hot_sales_words):
    redis_r.rpush("hot_sales_word", hot_sales_words)
    time.sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    close_ad(driver)
    time.sleep(1)
    switch_to_hot_sale_url(driver)

def crawler(driver):
    time.sleep(10)
    close_ad(driver)
    time.sleep(1)
    switch_to_hot_sale_url(driver)
    time.sleep(5)
    close_ad(driver)
    new = ''
    while True :
        if len(redis_r.lrange('hot_sales_word',0,-1)) == 0:
            break
        hot_sales_words = redis_r.lpop("hot_sales_word")
        try:
            item_name = click_item(driver, hot_sales_words)
            while True :
                json = hot_sales_word_data(driver,item_name)
                now = json
                if new == now : ## 判斷是否進入下一頁了 沒有卡在loading中
                    open_new_hot_sales(driver,redis_r,hot_sales_words)
                    break
                new = json
                print(json)
                driver.execute_script("document.body.style.zoom='1'")
                time.sleep(1)
                next_btn = driver.find_element_by_class_name("btn-next")
                if next_btn.get_attribute('disabled') == 'true':
                    print("最後一頁了")
                    break
                next_btn.click()
                time.sleep(1)
        except Exception as e :
            open_new_hot_sales(driver,redis_r,hot_sales_words)
            print(e)
        time.sleep(3)
    print("crawler complete")
if __name__=='__main__':
    ### step:1 將分類項目存入redis
    driver = mobduos.shopee_mobduos.Login().run()
    # time.sleep(10)
    # Item_copy_to_redis(driver)
    # ### step:2 透過分類項目 逐一收尋該項目的熱銷詞數據
    # threads = []
    # RunChrome = range(0,5,1)
    # for i in RunChrome:
    #     threads.append(threading.Thread(target = crawler ))
    #     time.sleep(1)
    # for i in range(0,len(threads)):
    #     threads[i].start()
    # driver = mobduos.shopee_mobduos.Login().run()
    time.sleep(10)
    crawler(driver)
