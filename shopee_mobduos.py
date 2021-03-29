#!/usr/bin/python
# -*- encoding: utf-8 -*-

import ssl

import requests

import os
import traceback

import cv2
import time
import random
import numpy as np
from PIL import Image
import os , bs4 , time , threading , redis
from urllib.request import urlretrieve
from selenium.webdriver.common.keys import Keys
# selenium-part
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

save_path = os.path.join('./', '', 'xiaoetong.cookies')

headers = {
    # 'upgrade-insecure-requests': '1',
    # 'sec-fetch-site': 'none',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-user': '?1',
    # 'dnt': '1',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'if-modified-since': 'Thu, 26 Mar 2020 23:50:00 GMT',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'cookie': 'pgv_pvi=2471064576; pgv_pvid=5782002132; RK=ONolY5oif/; ptcz=a47870ca7ab81fada934148d6f51e3b0f277d6392a83da1500c67160e342c143; fp3_id1=1100440A15DCB3607EBA9783B987E536B5B521433EED99ED52A9088B37DA960BFCE46BFDBAAF02D2619C6CC32454932FF3EE; pac_uid=0_5e72d24333325; XWINDEXGREY=0; pgv_info=ssid=s4198525417',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

class Login(object):


    def __init__(self, **kwargs):
        self.__init_args__(**kwargs)

        try:
            self.run()
        except Exception as e:
            traceback.print_exc(e)
        self.after_quit()

    def __init_args__(self, **kwargs):
        self.acc = "13903012084"
        self.pwd = "jle0004908"
        self.url = "https://shopee.mobduos.com/#/login"

    @staticmethod
    def show(name):
        cv2.imshow('Show', name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def get_postion(chunk, canves):
        otemp = chunk
        oblk = canves
        target = cv2.imread(otemp, 0)
        template = cv2.imread(oblk, 0)
        # w, h = target.shape[::-1]
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        # print(result.argmax(), [x, y])
        return x, y
        # 展示圈出來的區域
        # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
        # cv2.imwrite("yuantu.jpg", template)
        # show(template)

    @staticmethod
    def get_track(distance):
        # 初速度
        v = 0
        # 單位時間為0.2s來統計軌跡，軌跡即0.2内的位移
        t = 0.2
        # 位移/軌跡列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 當前的位移
        current = 0
        # 到達mid值開始減速
        mid = distance * 7 / 8
        distance += 10  # 先滑過一點，最后再反著滑動回來
        # a = random.randint(1,3)
        while current < distance:
            if current < mid:
                # 加速度越小，單位時間的位移越小,模擬的軌跡就越多越詳細
                a = random.randint(2, 4)  # 加速運動
            else:
                a = -random.randint(3, 5)  # 減速運動
            # 初速度
            v0 = v
            # 0.2秒時間内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 當前的位置
            current += s
            # 添加到軌跡列表
            tracks.append(round(s))
            # 速度已經達到v,該速度作為下次的初速度
            v = v0 + a * t
        # 反著滑動到大概準確位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        return tracks

    def after_quit(self):
        self.driver.quit()

    def put_msg(self):
        try:
            tab = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div[2]/div/div[1]/p[2]')))
            region = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div[2]/div/form[2]/div[1]/div/div[1]/div/div/div/input')))
            text_box = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div[2]/div/form[2]/div[1]/div/div[1]/input')))
            text_pwd = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div[2]/div/form[2]/div[2]/div/div/input')))

            send_btn = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div[2]/div/form[2]/div[3]/div/button')))
        except Exception as e:
            print(e)
            raise RuntimeError
        tab.click()
        region.click()
        time.sleep(1)
        code = self.wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[1]/ul/li[1]')))
        code.click()
        text_box.send_keys(self.acc)
        text_pwd.send_keys(self.pwd)
        try:
            action = ActionChains(self.driver)
            action.click(send_btn).perform()
        except Exception as e:
            traceback.print_exc(e)
            return False

    def start_dirver(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path="C:/chromedriver.exe",chrome_options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        print('webdriver get: {0}'.format(self.url))
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10)

    def save_img(self, file_name, img_url):
        print('fetch img: {0}'.format(img_url))
        try:
            rs = requests.get(img_url, headers=headers, timeout=20)
        except Exception as e:
            print(e)
            time.sleep(0.5)
            rs = requests.get(img_url, headers=headers, timeout=20)
        content = rs.content
        save_path = os.path.join('./', '', file_name)
        with open(save_path, 'wb') as fp:
            fp.write(content)
        print('Save image')

    def run(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings()
        self.start_dirver()

        self.put_msg()
        time.sleep(3)

        if 'muti_index' in self.driver.current_url:
            return self.click_into_shop()
        else:
            self.driver.switch_to.frame(1)  # 切换到iframe
            time.sleep(3)
            # 等待圖片載入完成
            slideBg = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//div/img[@id="slideBg"]')))
            # 判断圖片是否載入完成
            bk_block = slideBg.get_attribute('src')  # 大圖 url
            if not bk_block:
                print('等待圖片載入中 ... ')
                time.sleep(2)
            # 取得背景圖
            bk_block = self.driver.find_element_by_xpath('//img[@id="slideBg"]')  # 大圖
            web_image_width = bk_block.size['width']
            bk_block_x = bk_block.location['x']

            # 取得缺口圖
            slide_block = self.driver.find_element_by_xpath('//img[@id="slideBlock"]')  # 小滑塊
            slide_block_x = slide_block.location['x']

            # 保存圖片至本地
            slide_block_img = slide_block.get_attribute('src')
            bk_block_img = bk_block.get_attribute('src')

            # 保存圖片
            img_bg_path = os.path.join('./', '', 'img_bg.png')
            img_slider_path = os.path.join('./', '', 'img_slider.png')
            self.save_img('img_slider.png', slide_block_img)
            self.save_img('img_bg.png', bk_block_img)

            # 取得web圖與示例圖的比例
            img_bkblock = Image.open(img_bg_path)
            real_width = img_bkblock.size[0]
            width_scale = float(real_width) / float(web_image_width)

            # 計算缺口位置
            position = self.get_postion(img_bg_path, img_slider_path)
            real_position = position[1] / width_scale
            # 減去滑塊起始位置的距離
            real_position = real_position - (slide_block_x - bk_block_x)
            # 取得滑動距軌跡列表
            track_list = self.get_track(real_position)
            print('滑動軌跡:', int(real_position), track_list)
            # print('第一步,取得滑動按钮')
            button = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="tc-drag-thumb"]')))
            ActionChains(self.driver).click_and_hold(on_element=button).perform()  # 點擊左鍵，按住不放
            time.sleep(0.2)
            # print('第二步,拖動元素')
            for track in track_list:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 滑鼠移動到距離當前位置（x,y）
                time.sleep(0.002)
            # ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()   # 微调
            time.sleep(0.5)
            ActionChains(self.driver).release(on_element=button).perform()
            time.sleep(3)
            # return self.click_into_shop()
            print("滑完了")
            # self.click_into_shop()
            return self.driver

    def click_into_shop(self):
        try:
            # shop = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="el-scrollbar__view"][10]')))
            print("click")
            # ActionChains(self.driver).click(shop).perform()
        except Exception as e:
            print("這裡出錯1")
            traceback.print_exc(e)
            return False
        # print('等待3秒 ...')
        # time.sleep(5)
        # if '/index' in self.driver.current_url:
        #     return self.catch_cookies()
        return False

    # def catch_cookies(self):
    #     cookies = self.driver.get_cookies()
    #     _cookie_dict = {}
    #     for vo in cookies:
    #         _cookie_dict[vo['name']] = vo['value']
    #     # 保存cookie
    #     self.util.file(save_path, _cookie_dict)
    #     print('更新cookies成功')
    #     return True

if __name__ == '__main__':
    driver = Login().run()

# redis_r = redis.StrictRedis(host='localhost', port='6379', db='3',
#                             decode_responses=True)
# def close_ad(driver):
#     try:
#         driver.find_element_by_class_name('el-icon-circle-close').get_attribute('class')
#         driver.find_elements_by_css_selector("[class='el-icon-circle-close']")[1].click()
#         return "取消廣告了"
#     except:
#         return "沒有無廣告"
# #####  將每個項目存入redis  目前共2024項
# def item_copy_to_redis(driver):
#     hot_sale_url = 'https://shopee.mobduos.com/#/hot-search-word/hot-sales-word'
#     driver.execute_script("window.open(\'{}\')".format(hot_sale_url))
#     ### 移動到熱銷詞頁面
#     driver.switch_to.window(driver.window_handles[1])
#     item = WebDriverWait(driver, 15).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, '//input[@class="el-input__inner"]')))
#     ActionChains(driver).click(item[0]).perform()
#     ## 第一層item 目前共0 ~ 21 共22項
#     First_item = WebDriverWait(driver, 15).until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
#     for i in First_item[0:22]:
#         ActionChains(driver).move_to_element(i).perform()
#         item = driver.find_elements_by_css_selector("[class='el-scrollbar__view el-cascader-menu__list']")
#         ckecks = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
#         ckecks = ckecks[22::]
#         for u in ckecks:
#             ActionChains(driver).move_to_element(u).perform()
#             item = driver.find_elements_by_css_selector("[class='el-scrollbar__view el-cascader-menu__list']")
#             name = item[2].text
#             third_item = name.split('\n')
#             for x in third_item:
#                 redis_r.lpush("hot_sales_word",(str(i.text)+","+str(u.text)+","+str(x)))
#                 print(str(i.text)+","+str(u.text)+","+str(x))
#
# def switch_to_hot_sale_url(driver):
#     hot_sale_url = 'https://shopee.mobduos.com/#/hot-search-word/hot-sales-word'
#     driver.execute_script("window.open(\'{}\')".format(hot_sale_url))
#     ### 移動到熱銷詞頁面
#     driver.switch_to.window(driver.window_handles[1])
#
# def To_First_Page(driver):
#     Number_of_pages = driver.find_element_by_xpath("//input[@type='number']")
#     Number_of_pages.clear()
#
# def click_item(driver):
#     try:
#         item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//input[@class="el-input__inner"]')))
#         ActionChains(driver).click(item[0]).perform()
#         hot_sales_words = redis_r.lpop("hot_sales_word")
#         hot_sales_word = hot_sales_words.split(",")
#         hot_sales_word[0]
#         hot_sales_word[1]
#         hot_sales_word[2]
#         item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
#         # item = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
#         for i in item:
#             if i.text == hot_sales_word[0]:
#                 ActionChains(driver).move_to_element(i).perform()
#                 time.sleep(0.5)
#                 item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
#                 # item = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
#                 length = int(len(item))
#                 for j in item:
#                     if j.text == hot_sales_word[1]:
#                         ActionChains(driver).move_to_element(j).perform()
#                         time.sleep(0.5)
#                         item = WebDriverWait(driver, 5).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='el-cascader-node__label']")))
#                         # item = driver.find_elements_by_css_selector("[class='el-cascader-node__label']")
#                         item = item[length::]
#                         for k in item:
#                             if k.text == hot_sales_word[2]:
#                                 ActionChains(driver).click(k).perform()
#                                 break
#                         break
#                 break
#         To_First_Page(driver)
#         time.sleep(2)
#         return '"類目":"{0}>{1}>{2}"'.format(hot_sales_word[0],hot_sales_word[1],hot_sales_word[2])
#     except Exception as e :
#         driver.refresh()
#         print(e)
#         redis_r.lpush("hot_sales_word",hot_sales_words)
#
# def hot_sales_word_data(driver,item_name):
#     driver.execute_script("document.body.style.zoom='0.1'")
#     hot_word_data_table = driver.find_elements_by_css_selector("[class='el-table__row']") ## 關鍵字的數據
#     if len(hot_word_data_table) == 0:
#         return "無資料"
#     time.sleep(2)
#     splitline = int(len(hot_word_data_table) / 2)
#     hot_word_data = hot_word_data_table[0:splitline] ## 關鍵字的數據
#     hot_word_heards = hot_word_data_table[splitline::] ## 熱銷詞的關鍵字
#     for data, h in zip(hot_word_data, hot_word_heards):
#         datas = data.text.split('\n')
#         if len(datas) == 11 :
#             datas.insert(7, "無資料")
#         datajson = '{{{13},' \
#         '"熱搜詞":"{0}",' \
#         '"近一日銷量(pcs)":"{1}",' \
#         '"近一周銷量(pcs)":"{2}",'\
#         '"近30日銷量(pcs)":"{3}",'\
#         '"近30日銷售額(NT$)":"{4}",'\
#         '"近30日銷量增長率":"{5}",'\
#         '"產品基數":"{6}",'\
#         '"產品動銷率":"{7}",'\
#         '"搜索量":"{8}",'\
#         '"推薦出價":"{9}",'\
#         '"累積點讚數":"{10}",'\
#         '"累積評論數":"{11}",'\
#         '"操作":"{12}",'\
#         '}}'.format(h.text,datas[0],datas[1],datas[2],datas[3],datas[4],datas[5],datas[6],
#                     datas[7],datas[8],datas[9],datas[10],datas[11],item_name)
#         redis_r.rpush("hot_sales_word_datas",datajson)
#         print(datajson)
#     return datajson
#
# def crawler(driver):
#     item_name = click_item(driver)
#     while True:
#         hot_sales_word_data(driver,item_name)
#         driver.execute_script("document.body.style.zoom='1'")
#         next_btn = driver.find_element_by_class_name("btn-next")
#         if next_btn.get_attribute('disabled') == 'true' :
#             return "掃完了"
#         next_btn.click()
#         time.sleep(3)

