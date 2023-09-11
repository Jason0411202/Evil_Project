import time
import os
from bs4 import BeautifulSoup  # 需安裝bs4
from selenium import webdriver  # 需安裝selenium
# import chromedriver_autoinstaller as chromedriver

'''
免責聲明:本程式由107級中正大學通訊系畢業生Graves Francis開發,僅供學術交流之用,
         若擅自違規使用或營利導致帳號被封鎖,本人一概不負責。
'''
# 先到webdriver官網下載Win32的執行檔(符合自己Chrome的大版本)(chromedriver.exe)，再放到與此程式碼同一個資料夾中

id = ''  # 必須修改成自己的帳號
password = ''  # 必須修改成自己的密碼
take_a_break = 0.5  # 當個有禮貌的網路爬蟲者，為了避免造成伺服器負擔，隨時休息一下
course_Type = ['博雅通識']  # 可選:基礎通識,博雅通識 格式:[第一門課的資訊,第二門課的資訊]
course_Dimention = ['自然科學與技術']# 可選:中國語文知識與應用,英文能力訓練,資訊能力課程,基礎概論課程, 格式:[第一門課的資訊,第二門課的資訊]
                                                         #      跨向度課程,藝術與美學,能源、環境與生態,人文思維與生命探索,公民與社會參與,經濟與國際脈動,自然科學與技術
course_Page = [3]  # 要搶的課程在第幾頁 格式:[第一門課的資訊,第二門課的資訊]
course_Position = [1]  # 要搶的課程在該頁的位置 格式:[第一門課的資訊,第二門課的資訊]
try_Times = 500000  # 嘗試搶課的次數
time_To_Loggout = 3  # 循環幾次後要重登(注意「一次要搶的課數」*time_To_Loggout不可超過200)
error_Counter = 0  # 出錯計數器
error_Counter_Max = 10000  # 出錯幾次後要強制結束

'''
疑難排解:

1.如果webdriver.Chrome那行出錯,開啟該執行檔(chromedriver.exe)後再接著run此程式碼試試
2.檢查自己的chrome.exe位置,路徑必須是唯一的: (win64版) C:\Program Files\Google\Chrome
                                        (win32版) C:\Program Files (x86)\Google\Chrome
3.在呼叫main() 上面一點的地方打上(225行處)

options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

4.error報錯指示:

    error001:可能是學號密碼打錯，網路環境不佳，網站介面被修改等等

    error002:可能是選課系統網站格式改變,網路環境不佳

    error003:可能是course_Type,course_Dimention那邊打錯字

    error004:可能是course_Type與course_Dimention未匹配

    error005:可能是course_Page、course_Position輸入錯誤,或是已經搶到課了

'''
def Login_User_Page():
    global error_Counter

    # 登入所需的輸入框網址
    driver.get('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/login.php?m=0')
    try:
        time.sleep(take_a_break)
        driver.find_element('name', 'id').send_keys(id)  # 送出學號
        time.sleep(take_a_break)
        driver.find_element('name', 'password').send_keys(password)  # 送出密碼
        time.sleep(take_a_break)
        driver.find_element(
            'xpath', '/html/body/font/center/form/table/tbody/tr[7]/td/input').submit()  # 送出密碼
        time.sleep(take_a_break)
    except:
        print("error001") #可能是學號密碼打錯，網路環境不佳，網站介面被修改等等
        error_Counter += 1
        if(error_Counter >= error_Counter_Max):
            os._exit(0)  # 強制結束程式
        time.sleep(take_a_break)


def Login_Pre_Main_Page(driver):
    driver.get('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/')  # 登入前主頁面網址


def Get_Sourse_Code_And_Print():
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 使用bs4解析網頁原始碼
    print("The original code is: ")
    print("")
    # print(soup) #印出當前網頁原始碼
    time.sleep(3)


def Send_Course_Seletion(i):
    global error_Counter
    try:
        driver.find_element('link text', '加選及加簽').click()  # 點擊加選與加簽鏈結
        time.sleep(take_a_break)
        driver.switch_to.window(driver.window_handles[1])  # 跳至新的視窗
        driver.find_element('xpath',
                            '/html/body/center/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[8]/font/input[3]').click()  # 點擊通識中心選項
    except:
        print('error002')  # 可能是選課系統網站格式改變,網路環境不佳
        error_Counter += 1
        if(error_Counter >= error_Counter_Max):
            os._exit(0)  # 強制結束程式
        time.sleep(take_a_break)

    try:
        if(course_Type[i] == '基礎通識'):
            driver.find_element('xpath',
                                '/html/body/center/form/table/tbody/tr[1]/td/div[3]/input[1]').click()  # 點擊基礎通識選項
            time.sleep(take_a_break)
            if(course_Dimention[i] == '中國語文知識與應用'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[1]/input[1]').click()  # 點擊中國語文知識與應用選項
            elif(course_Dimention[i] == '英文能力訓練'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[1]/input[2]').click()  # 點擊英文能力訓練選項
            elif(course_Dimention[i] == '資訊能力課程'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[1]/input[3]').click()  # 點擊資訊能力課程選項
            elif(course_Dimention[i] == '基礎概論課程'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[1]/input[4]').click()  # 點擊基礎概論課程選項
            else:
                print('error003')  # 可能是course_Type,course_Dimention那邊打錯字
                error_Counter += 1
                if(error_Counter >= error_Counter_Max):
                    os._exit(0)  # 強制結束程式
                time.sleep(take_a_break)

        elif(course_Type[i] == '博雅通識'):
            driver.find_element('xpath',
                                '/html/body/center/form/table/tbody/tr[1]/td/div[3]/input[2]').click()  # 點擊博雅通識選項
            time.sleep(take_a_break)
            if(course_Dimention[i] == '跨向度課程'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[1]').click()  # 點擊跨向度課程選項
            elif(course_Dimention[i] == '藝術與美學'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[2]').click()  # 點擊藝術與美學選項
            elif(course_Dimention[i] == '能源、環境與生態'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[3]').click()  # 點擊能源、環境與生態選項
            elif(course_Dimention[i] == '人文思維與生命探索'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[4]').click()  # 點擊人文思維與生命探索選項
            elif(course_Dimention[i] == '公民與社會參與'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[5]').click()  # 點擊公民與社會參與選項
            elif(course_Dimention[i] == '經濟與國際脈動'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[6]').click()  # 點擊經濟與國際脈動選項
            elif(course_Dimention[i] == '自然科學與技術'):
                driver.find_element('xpath',
                                    '/html/body/center/form/table/tbody/tr[1]/td/div[3]/span[2]/input[7]').click()  # 點擊自然科學與技術選項
            else:
                print('error003')  # 可能是course_Type,course_Dimention那邊打錯字
                error_Counter += 1
                if(error_Counter >= error_Counter_Max):
                    os._exit(0)  # 強制結束程式
                time.sleep(take_a_break)
        else:
            print('error003')  # 可能是打錯字
            error_Counter += 1
            if(error_Counter >= error_Counter_Max):
                os._exit(0)  # 強制結束程式
            time.sleep(take_a_break)

        time.sleep(take_a_break)
        driver.find_element('xpath',
                            '/html/body/center/form/input[6]').click()  # 送出表單
        time.sleep(take_a_break)
    except:
        print('error004')  # 可能是course_Type與course_Dimention未匹配
        error_Counter += 1
        if(error_Counter >= error_Counter_Max):
            os._exit(0)  # 強制結束程式
        time.sleep(take_a_break)


def Try_Get_Course(i):
    global error_Counter

    try:
        if(course_Page[i] == 2):
            driver.find_element('link text', '第 2 頁').click()  # 點擊第二頁的連結
        elif(course_Page[i] == 3):
            driver.find_element('link text', '第 3 頁').click()  # 點擊第三頁的連結
        elif(course_Page[i] == 4):
            driver.find_element('link text', '第 4 頁').click()  # 點擊第四頁的連結
        elif(course_Page[i] == 5):
            driver.find_element('link text', '第 5 頁').click()  # 點擊第五頁的連結
        if(course_Page[i] != 1):
            time.sleep(take_a_break)
        course_Xpath = '/html/body/center/form/table/tbody/tr[1]/th/table/tbody/tr['+str(
            course_Position[i]+1)+']/th[1]/input'
        driver.find_element('xpath', course_Xpath).click()
        time.sleep(take_a_break)
        driver.find_element('xpath',
                            '/html/body/center/form/table/tbody/tr[3]/th/input').submit()  # 送出表單
        time.sleep(take_a_break)
        driver.close()
        time.sleep(take_a_break)
    except:
        print('error005')  # 可能是course_Page、course_Position輸入錯誤,或是已經搶到課了
        error_Counter += 1
        if(error_Counter >= error_Counter_Max):
            os._exit(0)  # 強制結束程式
        time.sleep(take_a_break)


def main():
    counter1 = 0
    counter2 = 0
    while(counter1 < try_Times):
        Login_User_Page()
        counter2 = 0
        while(counter2 < time_To_Loggout):
            for i in range(len(course_Type)):
                Send_Course_Seletion(i)
                Try_Get_Course(i)
                driver.switch_to.window(driver.window_handles[0])  # 跳至新的視窗
            counter1 += 1
            counter2 += 1
            print('剩餘搶課的次數: ', try_Times-counter1)
            print('距離重登的次數: ', time_To_Loggout-counter2)
            print('')
        driver.back()

# chromedriver.install()
options = webdriver.ChromeOptions()  # 設定瀏覽器的選項
options.add_argument("--start-maximized")  # 將放大視窗加入選項
#options.add_argument('--headless') #不顯示瀏覽器UI

driver = webdriver.Chrome(options=options)  # 開啟Win32的執行檔

main()

driver.quit()

# 版權警告:此程式為Graves Francis所有，不得抄襲，盜版必究