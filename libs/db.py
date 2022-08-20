import psycopg2
import psycopg2.extras
import psycopg2.extensions
from libs import scraping
from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def is_exists_table(cursor:psycopg2.extensions.cursor,table_name:str) -> bool:
    '''
        指定したテーブルがDB内に存在するか確認する

        Args:
            cursor (psycopg2.extensions.cursor): テーブルを操作するオブジェクト
            table_name (str): データを登録するテーブル名

        Returns:
            テーブルがある: True
            テーブルがない: False
        
        Raises:
            クエリの実行に失敗した場合に発生
    '''

    select_count_query = "select exists(select * from information_schema.tables where table_name=%s)"
    try:
        cursor.execute(select_count_query, (table_name,))
    except:
        raise Exception("Error: failed to execute select query")
    
    return cursor.fetchone()[0]

def insert_performance_db(conn:psycopg2.extensions.connection,cursor:psycopg2.extensions.cursor,add_performance:List[map],table_name:str):
    '''
        データをテーブルに登録する

        Args:
            conn (psycopg2.extensions.connection): DBを操作するオブジェクト
            cursor (psycopg2.extensions.cursor): テーブルを操作するオブジェクト
            add_performance (List[map]): 追加する成績
            table_name (str): データを登録するテーブル名
        
        Raises:
            クエリの実行に失敗した場合に発生
    '''

    insert_query = ("insert into " + table_name + " (subject_name, "            #科目名
                                                    " instructor, "             #担当教員名
                                                    " subject_category, "       #科目区分
                                                    " selection_category, "     #必修選択区分
                                                    " credit_num, "             #単位数
                                                    " evaluation, "             #評価
                                                    " score ,"                  #得点
                                                    " subject_GP,"              #科目GP
                                                    " acquisition_year, "       #取得年度
                                                    " registered_date, "        #報告日
                                                    " test_category)")          #試験種別
    insert_query += " values %s"
    
    try:
        psycopg2.extras.execute_values(cursor,insert_query,add_performance)
    except:
        raise Exception("Error: failed to insert into table")
    
    conn.commit()

def create_performance_db(driver: webdriver.Chrome, wait: WebDriverWait,conn:psycopg2.extensions.connection,cursor:psycopg2.extensions.cursor,table_name:str):
    '''
        テーブルを作成し、成績の登録を行う

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
            cursor (psycopg2.extensions.cursor): テーブルを操作するオブジェクト
            add_performance (List[map]): 追加する成績
            table_name (str): データを登録するテーブル名
        
        Raises:
            クエリの実行に失敗した場合に発生
    '''

    create_query = "CREATE TABLE " + table_name
    create_query += ("(subject_name text primary key," #科目名
                    " instructor text,"              #担当教員名
                    " subject_category text,"        #科目区分
                    " selection_category text,"      #必修選択区分
                    " credit_num integer,"           #単位数
                    " evaluation text,"              #評価
                    " score text,"                   #得点
                    " subject_GP text,"              #科目GP
                    " acquisition_year text,"        #取得年度
                    " registered_date text,"         #報告日
                    " test_category text)")          #試験種別
    
    try:
        cursor.execute(create_query)
    except:
        raise Exception("Error: failed to create table")
    
    all_performance = scraping.get_performance_content(driver,wait)
    insert_performance_db(conn,cursor,all_performance,table_name)

def search_new_performance(driver: webdriver.Chrome, wait: WebDriverWait,cursor:psycopg2.extensions.cursor,table_name:str) -> List[tuple]:
    '''
        成績を取得し、DBと照合して新しく追加された成績を取り出す

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
            cursor (psycopg2.extensions.cursor): テーブルを操作するオブジェクト
            table_name (str): データを登録するテーブル名
        
        Returns:
            List[tuple]: 更新された成績
        
        Raises:
            クエリの実行に失敗した場合に発生
    '''
    all_performance = scraping.get_performance_content(driver,wait)

    new_performance = []

    for performance in all_performance:
        subject_name = performance[0]

        check_query = "SELECT * FROM " + table_name + " WHERE subject_name='" + subject_name + "'"
        try:
            cursor.execute(check_query)
        except:
            raise Exception("Error: failed to check query")
        
        if not len(cursor.fetchall()):
            new_performance.append(performance)
    
    return new_performance
