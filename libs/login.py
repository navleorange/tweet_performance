from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_portal_page(driver:webdriver.Chrome,wait:WebDriverWait):
    PORTAL_URL = "https://gakujo.shizuoka.ac.jp/portal/"

    #学務情報システムの最初のページの読み込み
    try:
        driver.get(PORTAL_URL)
    except:
        raise Exception("Error: failed to get portal page")

def move_login_page(driver:webdriver.Chrome,wait:WebDriverWait):

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
        raise Exception("Error: failed to sent userID")
    
    try:
        driver.find_element(by=By.ID,value=input_password_id).send_keys(user_password)
    except:
        raise Exception("Error: failed to sent password")

    try:
        driver.find_element(by=By.CLASS_NAME,value=login_button_class).click()
    except:
        raise Exception("Error: failed to push login button")

def move_kyoum_page(driver:webdriver.Chrome,wait:WebDriverWait):
    system_link_id = "home_systemCooperationLink"

    #ページが読み込めているか確認
    try:
        wait.until(EC.presence_of_element_located((By.ID,system_link_id)))
    except:
        raise Exception("Error: Time out read gakujo page")
    
    KYOUM_URL = "https://gakujo.shizuoka.ac.jp/kyoumu/sso/loginStudent.do"

    kyoum_button_script = "systemCooperationOpenWin('/home/systemCooperationLink/initializeShibboleth?renkeiType=kyoumu', 'kyoumuWindow');"
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
    performance_button_script = "dbLinkClick('/kyoumu/seisekiSearchStudentInit.do;jsessionid=Hq2eJECpWtakzJdOrsU7imy1glBMDax0qy04cJF3?mainMenuCode=008&parentMenuCode=007');"
    
    try:
        driver.execute_script(performance_button_script)
    except:
        raise Exception("Error: failed to move performance page")

def login_gakujo(driver:webdriver.Chrome,wait:WebDriverWait,user_id:str,user_pass):
    get_portal_page(driver,wait)
    move_login_page(driver,wait)
    push_login_button(driver,wait,user_id,user_pass)