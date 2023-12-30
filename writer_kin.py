import clipboard
import keyboard

from io import BytesIO
import win32clipboard
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

implicitly_wait_rate = 3

#wait user press [key]] and release it
def wait_keyboard(key):
    while True: 
        if keyboard.is_pressed(key): break
    while True:
        if not keyboard.is_pressed(key): break

#https://all-share-source-code.tistory.com/42
def image_to_clipboard(filepath):
    #load image
    image = Image.open(filepath)
    output=BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    #send to clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

#ans list must be made up with dictionary that contain 'number', 'company', 'url', 'msg' as key
def write_kin(ans_list):
    global implicitly_wait_rate
    print('open writer...')
    driver = webdriver.Chrome()
    driver.get(url = 'https://www.naver.com/')
    driver.implicitly_wait(implicitly_wait_rate)
    main_window = driver.current_window_handle
    print('login browser and press Enter')
    wait_keyboard('enter')
    #answering
    for ans in ans_list:
        print('='*50)
        #new tab load
        driver.execute_script(f"window.open('{ans['url']}');")
        driver.implicitly_wait(implicitly_wait_rate) #wait
        driver.switch_to.window(driver.window_handles[-1])
        print(f"open tab {ans['url']}") #$
        #check is question valid & find answer button
        try:
            driver.find_element(by=By.CSS_SELECTOR, value=r'.adoptCheck')
            ans_valid = False
        except: ans_valid = True
        try: write_btn = driver.find_element(by=By.CSS_SELECTOR, value=r'#answerWriteButton')
        except: ans_valid = False
        if not ans_valid: 
            print('question is not valid') #$
            driver.close()
            driver.switch_to.window(main_window)
            continue
        print('question is valid') #$
        #find answer button
        write_btn.click()
        #copy message to clipboard and wait user action
        clipboard.copy(ans['msg'])
        print('write "Ctrl+V" (msg) and press Enter') #$
        wait_keyboard('enter')
        #copy prediction image to clipboard and "
        image_to_clipboard(f"./image/{ans['company']}_{ans['number']}_pred.png")
        print('write "Ctrl+V" (pred) and press Enter') #$
        wait_keyboard('enter')
        #copy prediction image to clipboard and "
        image_to_clipboard(f"./image/{ans['company']}_{ans['number']}_hist.png")
        print('write "Ctrl+V" (hist) and press Enter') #$
        wait_keyboard('enter')
        #submit
        submit_btn = driver.find_element(by=By.CSS_SELECTOR, value=r'#answerRegisterButton')
        submit_btn.click()
        print('submit the message') #$
        #wait until answer submited
        print('press enter when you confirm answer is submited')
        wait_keyboard('enter')
        # close tab and bak to main window
        driver.close()
        driver.switch_to.window(main_window)
        print('wait for next question...') #$
        #time.sleep(1)
    #closing
    print('close writer...')
    driver.quit()

if __name__ == '__main__':
    write_kin([{'url': 'https://kin.naver.com/qna/detail.naver?d1id=8&dirId=81302&docId=461217436&qb=64yA7ZWc7Ya17Jq0&enc=utf8&sion=kin&rank=1&search_sort=3&spq=0', 'msg': '안녕하십니까 통계기반배송도착시간 예측 서비스 개발자 강시우입니다.\n질문자님의 택배가 수성MP에 있습니다. \n수성MP에 간선상차된 택배들 중 \n\n25%가 16시간 46분\n50%가 18시간 2분\n75%가 19시간 40분\n95%가 1일 15시간 54분\n안으로 도착했습니다.\n\n75%선으로 추정한 도착예정시간은 12월 29일 17시 54분입니다.\n더 자세한 정보는 아래 url에서 확인가능합니다.\nhttp://cnps.site/api/makesrc?number=682590831003&company=cj'}, {'url': 'https://kin.naver.com/qna/detail.naver?d1id=8&dirId=81302&docId=461217382&qb=64yA7ZWc7Ya17Jq0&enc=utf8&sion=kin&rank=2&search_sort=3&spq=0', 'msg': '안녕하십니까 통계기반배송도착시간 예측 서비스 개발자 강시우입니다.\n질문자님의 택배가 곤지암Hub에 있습니다. \n곤지암Hub에 간선상차된 택배들 중 \n\n25%가 8시간 0분\n50%가 9시간 25분\n75%가 11시간 3분\n95%가 13시간 37분\n안으로 도착했습니다.\n\n75%선으로 추정한 도착예정시간은 12월 29일 16시 8분입니다.\n더 자세한 정보는 아래 url에서 확인가능합니다.\nhttp://cnps.site/api/makesrc?number=583491348490&company=cj'}])