import os
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import logging
import traceback
import threading


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

##
#ページからデータを取得
##
def get_data(driver,i,exp_name_list,exp_jobdescriptions,exp_worklocation,exp_salary):
    ##===========
    ##会社名、仕事内容、勤務地、給与を取得
    ##===========
    time.sleep(5)
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    jobdescriptions = driver.find_elements_by_css_selector('.cassetteRecruit__main > .tableCondition > tbody > tr:first-child > .tableCondition__body')
    worklocation = driver.find_elements_by_css_selector('.cassetteRecruit__main > .tableCondition > tbody > tr:nth-child(3) > .tableCondition__body')
    salary = driver.find_elements_by_css_selector('.cassetteRecruit__main > .tableCondition > tbody > tr:last-child > .tableCondition__body')

    # 1ページ分繰り返し
    print(len(name_list))
    for (name,job,location,sala) in zip(name_list,jobdescriptions,worklocation,salary):
        exp_name_list[i-1].append(name.text)
        exp_jobdescriptions[i-1].append(job.text)
        exp_worklocation[i-1].append(location.text)
        exp_salary[i-1].append(sala.text)
        #print(name.text+"\n"+job.text+"\n"+location.text+"\n"+sala.text+"\n\n")



#main

def main1():
    search_keyword = input("検索キーワードを入力して下さい >>> ")
    starttime = time.time()
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    #driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_jobdescriptions = []
    exp_worklocation = []
    exp_salary = []
    exp_name =[]
    exp_job = []
    exp_work = []
    exp_sala=[]
    ####======
    ##次ページの情報を取得する
    ####======
    #取得するページ数
    page_count = 3
    i = 1
    while i<=page_count:
        # ページ終了まで繰り返し取得
        exp_name_list.append([])
        exp_jobdescriptions.append([])
        exp_worklocation.append([])
        exp_salary.append([])
        #theread処理
        thread = threading.Thread(target=get_data, args=(driver,i,exp_name_list,exp_jobdescriptions,exp_worklocation,exp_salary))
        thread.start()
        
        ###====
        ##URLの規則から次ページを開く
        ##=====
        #現在のURL
        current_url = driver.current_url
        #次のページ
        if i == 1:
            pg = "pg"+str(i+1)+"/?"
            #次のページのURL
            next_url=current_url.replace('?', pg)
        else:
            next_url=current_url.replace("pg"+str(i), "pg"+str(i+1))
        #新規window
        driver.execute_script("window.open()")
        time.sleep(2)
        # 新規Windowを開いたあとのWindowハンドル一覧を取得
        print(driver.window_handles)
        driver.switch_to.window(driver.window_handles[i]) #switch new tab
        driver.get(next_url)
        time.sleep(2)
        i += 1
            
    thread.join()
    #CSV用に整形
    if page_count>1:
        for nline,jline,wline,sline in zip(exp_name_list,exp_jobdescriptions,exp_worklocation,exp_salary):
            exp_name= exp_name +nline
            exp_job= exp_job +jline
            exp_work=exp_work+wline
            exp_sala=exp_sala+sline

    #print(exp_name_list)
        
    ##====
    ##CSVに出力
    ##====
    csvdict = dict( 会社名=exp_name, 仕事内容=exp_job, 勤務地=exp_work, 給与=exp_sala)
    df = pd.DataFrame(csvdict)
    df.to_csv('result.csv')

    endtime = time.time()

    print("並列化を行った場合は",endtime-starttime,"秒です。")

def main2():
    search_keyword = input("検索キーワードを入力して下さい >>> ")
    starttime = time.time()
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    #driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

   
   # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_jobdescriptions = []
    exp_worklocation = []
    exp_salary = []

    ####======
    ##次ページの情報を取得する
    ####======
    #取得するページ数
    page_count = 3
    
    while page_count>0:
        ##===========
        ##会社名、仕事内容、勤務地、給与を取得
        ##===========
        time.sleep(5)
        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        jobdescriptions = driver.find_elements_by_css_selector('.cassetteRecruit__main > .tableCondition > tbody > tr:first-child > .tableCondition__body')
        worklocation = driver.find_elements_by_css_selector('.cassetteRecruit__main > .tableCondition > tbody > tr:nth-child(3) > .tableCondition__body')
        salary = driver.find_elements_by_css_selector('.cassetteRecruit__main > .tableCondition > tbody > tr:last-child > .tableCondition__body')

        # 1ページ分繰り返し
        print(len(name_list))
        for (name,job,location,sala) in zip(name_list,jobdescriptions,worklocation,salary):
            exp_name_list.append(name.text)
            exp_jobdescriptions.append(job.text)
            exp_worklocation.append(location.text)
            exp_salary.append(sala.text)
        
        time.sleep(5)
        ###====
        ##ページャー（次へ）をクリック
        ##=====
        pager_button = driver.find_element_by_css_selector('body > div.wrapper > div:nth-child(5) > form > div > nav:nth-child(103) > ul > li:last-child > a')
        #actions = ActionChains(driver)
        #actions.move_to_element(page_show)
        driver.execute_script('arguments[0].click();', pager_button) #要素を表示,クリック
        time.sleep(5)
        #pager_button.click()
        page_count -= 1
        
    ##====
    ##CSVに出力
    ##====
    csvdict = dict( 会社名=exp_name_list, 仕事内容=exp_jobdescriptions, 勤務地=exp_worklocation, 給与=exp_salary)
    df = pd.DataFrame(csvdict)
    df.to_csv('result2.csv')

    endtime = time.time()

    print("並列化を行なわない場合は",endtime-starttime,"秒です。")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    #エラーログの出力
    errorlog_path = 'errorlog.txt'
    try:
        main1()
        main2()
    except:
        error_m = traceback.format_exc()
        with open(errorlog_path,mode='w') as f:
            f.write(error_m)
