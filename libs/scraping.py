from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

def fetch_performance(driver:webdriver.Chrome,wait:WebDriverWait) -> List[WebElement]:
    '''
        成績のページから成績のテーブルを取得する

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
        
        Returns:
            List[WebElement]: 成績のテーブル
        
        Raises:
            1つ目: 成績ページの読み込みに失敗した場合
            2つ目: 成績取得のクエリ実行に失敗した場合
    '''

    performance_button_script = "dbLinkClick('/kyoumu/seisekiSearchStudentInit.do;jsessionid=Hq2eJECpWtakzJdOrsU7imy1glBMDax0qy04cJF3?mainMenuCode=008&parentMenuCode=007');"
    driver.execute_script(performance_button_script)

    perfomance_inner_class = "txt12"
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,perfomance_inner_class)))
    except:
        raise Exception("Error: Time out read performance page")

    table_selector = "body > table:nth-child(9) > tbody > tr > td > table > tbody > tr"
    try:
        elems = driver.find_elements(by=By.CSS_SELECTOR,value=table_selector)
    except:
        raise Exception("Error: failed to get performance")
    
    return elems

def parse_performance(elems:List[WebElement]):
    '''
        成績テーブルから1つ1つの成績を取り出す

        Args:
            List[WebElement]: 成績のテーブル
        
        Returns:
            List[tuple]: 1つ1つに分けられた成績
        
        Raises:
            成績テーブルから成績の取り出しに失敗したときに発生する

    '''

    all_result = []

    table_inner_class = "txt12"

    for elem in elems:

        try:
            line = elem.find_elements(by=By.CLASS_NAME,value=table_inner_class)
        except:
            raise Exception("Error: failed to parse performance")

        line_result = []

        for i in line:
            text = i.text
            text = "".join(text.split())  #空白削除
            line_result.append(text)
        
        all_result.append(tuple(line_result))
    
    return all_result

def get_performance_content(driver:webdriver.Chrome,wait:WebDriverWait):
    '''
        学務から1成績のテーブルを取得し、それを1つ1つの成績に分割して返す一連の処理をする

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト      
        
        Returns:
            List[tuple]: 1つ1つに分けられた成績
        
        Note:
            テーブルの一行目は列名のため除外して返す
    
    '''
    elems = fetch_performance(driver,wait)

    return parse_performance(elems[1:])