import psycopg2
import psycopg2.extras
from libs import scraping
from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def is_exists_table(cursor:psycopg2.cursor,table_name:str) -> bool:
    '''
        exists : True
        not exists : False

    '''

    select_count_query = "select exists(select * from information_schema.tables where table_name=" +  table_name + ")"
    try:
        cursor.execute(select_count_query)
    except:
        raise Exception("Error: failed to execute select query")
    
    return cursor.fetchone()[0]

def insert_performance_db(conn:psycopg2.connection,cursor:psycopg2.cursor,add_performance:List[map],table_name:str):
    insert_query = "INSERT INTO " + table_name + " values(?,?,?,?,?,?,?,?,?,?,?)"
    
    try:
        cursor.executemany(insert_query,add_performance)
    except:
        raise Exception("Error: failed to insert into table")
    
    conn.commit()

def create_performance_db(driver: webdriver.Chrome, wait: WebDriverWait,conn:psycopg2.connection,cursor:psycopg2.cursor,table_name:str):
    create_query = "CREATE TABLE " + table_name
    create_query += ("(subject_name text primary key," #科目名
                    " instructor text,"              #担当教員名
                    " subject_category text,"        #科目区分
                    " selection_category text,"      #必修選択区分
                    " credit_num integer,"           #単位数
                    " evaluation text,"              #評価
                    " score real,"                   #得点
                    " subject_GP real,"              #科目GP
                    " acquisition_year integer,"     #取得年度
                    " registered_date text,"         #報告日
                    " test_category text)")          #試験種別
    
    try:
        cursor.execute(create_query)
    except:
        raise Exception("Error: failed to create table")
    
    all_performance = scraping.get_performance_content(driver,wait)
    insert_performance_db(conn,cursor,all_performance,table_name)

def search_new_performance(driver: webdriver.Chrome, wait: WebDriverWait,cursor:psycopg2.cursor,table_name:str) -> List[tuple]:
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
