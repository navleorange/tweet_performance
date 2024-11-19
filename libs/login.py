from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_portal_page(driver:webdriver.Chrome,wait:WebDriverWait):
    '''
        ポータルページを取得する

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
        
        Raises:
            ポータルページの取得に失敗した場合に発生
    '''

    PORTAL_URL = "https://gakujo.shizuoka.ac.jp/portal/"

    #学務情報システムの最初のページの読み込み
    try:
        driver.get(PORTAL_URL)
    except:
        raise Exception("Error: failed to get portal page")

def move_login_page(driver:webdriver.Chrome,wait:WebDriverWait):
    '''
        ポータルページからログインページに移動する

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
        
        Raises:
            1つ目: ポータルページにあるログイン画面へ遷移するボタンが表示されない場合に発生
            2つ目: ポータルページにあるログイン画面へ遷移するボタンを押すことに失敗した場合に発生
    '''

    portal_button_class = "btn_login"
    try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME,portal_button_class)))
    except:
        raise Exception("Error: Time out read portal page")
    
    try:
        driver.find_element(by=By.CLASS_NAME,value=portal_button_class).click()
    except:
        raise Exception("Error: failed to push login button")

def push_login_button(driver:webdriver.Chrome,wait:WebDriverWait,user_id:str,user_password):
    '''
        ユーザID,パスワードを入力してログインをする

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
            user_id (str): 学務情報システムにログインするためのユーザID
            user_password (str): 学務情報システムにログインするためのパスワード
        
        Raises:
            1つ目: ログインページにあるログインボタンが表示されない場合に発生
            2つ目: ユーザIDの入力にした場合に発生
            3つ目: パスワードの入力にした場合に発生
            4つ目: ログインボタンを押すことに失敗した場合に発生

    '''
    login_button_class = "form-element form-button"
    login_button_class = login_button_class.replace(" ",".")

    try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME,login_button_class)))
    except:
        raise Exception("Error: Time out read login page")

    input_userid_id = "username"
    input_password_id = "password"

    try:
        driver.find_element(by=By.ID,value=input_userid_id).send_keys(user_id)
    except:
        raise Exception("Error: failed to send userID")
    
    try:
        driver.find_element(by=By.ID,value=input_password_id).send_keys(user_password)
    except:
        raise Exception("Error: failed to send password")

    try:
        driver.find_element(by=By.CLASS_NAME,value=login_button_class).click()
    except:
        raise Exception("Error: failed to push login button")

def move_kyoum_page(driver:webdriver.Chrome,wait:WebDriverWait):
    '''
        学務ページから教務ページへ移動する

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
        
        Raises:
            1つ目: 学務ページにある教務ページへの遷移ボタンが表示されない場合に発生
            2つ目: 教務ページへの遷移ボタンを押したときのイベントの実行に失敗した場合に発生
            3つ目: 教務ページのタブの読み込みに失敗した場合に発生
            4つ目: 教務ページのタブへの切り替えに失敗した場合に発生
            5つ目: 教務ページの取得に失敗した場合に発生
    '''
    system_link_id = "home_systemCooperationLink"

    #ページが読み込めているか確認
    try:
        wait.until(EC.presence_of_element_located((By.ID,system_link_id)))
    except:
        raise Exception("Error: Time out read gakujo page")
    
    KYOUM_URL = "https://gakujo.shizuoka.ac.jp/kyoumu/sso/loginStudent.do"

    kyoum_button_script = "systemCooperationOpenWin('/home/systemCooperationLink/initializeShibboleth', 'kyoumuWindow');"
    try:
        driver.execute_script(kyoum_button_script)
    except:
        raise Exception("Error: failed to push kyoum login button")

    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)  #タブが増えるまで
    except:
        raise Exception("Error: Time out wait kyoum window")
    
    default_window = driver.window_handles[0]
    kyoum_window = driver.window_handles[1]

    try:
        driver.switch_to.window(kyoum_window)
    except:
        raise Exception("Error: failed to switch window to kyoum")

    try:
        driver.get(KYOUM_URL)
    except:
        raise Exception("Error: failed to get kyoum page")

def move_performance_page(driver:webdriver.Chrome,wait:WebDriverWait):
    '''
        教務ページの成績のページへ移動する

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
        
        Raises:
            成績ページへの遷移ボタンを押したときのイベントの実行に失敗した場合に発生
    '''

    performance_button_script = "dbLinkClick('/kyoumu/seisekiSearchStudentInit.do;');"
    
    try:
        driver.execute_script(performance_button_script)
    except:
        raise Exception("Error: failed to move performance page")

def login_gakujo(driver:webdriver.Chrome,wait:WebDriverWait,user_id:str,user_pass):
    '''
        ポータルページからログインまでの一連の処理をする

        Args:
            driver (webdriver.Chrome): Chromeブラウザを操作するオブジェクト
            wait (WebDriverWait): 待機処理をするオブジェクト
            user_id (str): 学務情報システムにログインするためのユーザID
            user_password (str): 学務情報システムにログインするためのパスワード
    '''

    get_portal_page(driver,wait)
    move_login_page(driver,wait)
    push_login_button(driver,wait,user_id,user_pass)
