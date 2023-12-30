from selenium import webdriver
from selenium.webdriver.common.by import By

implicitly_wait_rate = 3

# inq_list must be made up with dictionary that contain 'number', 'company', 'url' as key
def inquiry_cnps(inq_list):
    global implicitly_wait_rate
    res = [] #resource
    rec = [] #record
    #make driver
    driver = webdriver.Chrome()
    driver.get(url = 'https://www.google.com/')
    driver.implicitly_wait(implicitly_wait_rate)
    main_window = driver.current_window_handle
    #inquirying
    for inq in inq_list:
        #new tab load
        inq_url = f"http://cnps.site/search?number={inq['number']}&company={inq['company']}"
        driver.execute_script(f"window.open('{inq_url}');")
        driver.implicitly_wait(implicitly_wait_rate)
        driver.switch_to.window(driver.window_handles[-1])
        #check is question valid & find image
        try:
            prediction = driver.find_element(by=By.CSS_SELECTOR, value=r'#statistical-prediction')
            histogram = driver.find_element(by=By.CSS_SELECTOR, value=r'#histogram')
        except:
            driver.close()
            driver.switch_to.window(main_window)
            continue
        #screenshot image
        prediction.screenshot(f"./image/{inq['company']}_{inq['number']}_pred.png")
        histogram.screenshot(f"./image/{inq['company']}_{inq['number']}_hist.png")
        #make message
        inq_msg = prediction.text.replace('배송도착시간 통계', '안녕하십니까 www.cnps.site 의 개발자 강시우입니다.')+f'\n{inq_url}에 방문해 더 상세한 내용을 확인할 수 있습니다.' 
        res.append({'number': inq['number'], 'company': inq['company'], 'url': inq['url'], 'msg': inq_msg})
        rec.append(f"{inq['company']}_{inq['number']}")
        #close tab
        driver.close()
        driver.switch_to.window(main_window)
    driver.quit()
    #record invoice number & company
    with open('./log/invoice.txt', 'r') as f: rec.extend(f.read().split(';'))
    rec.sort()
    with open('./log/invoice.txt', 'w') as f: f.write(';'.join(rec))
    return res

if __name__ == '__main__':
    inquiry_cnps([{'number': 574677392484, 'company': 'cj', 'url': r'https://kin.naver.com/qna/detail.naver?d1id=8&dirId=81302&docId=461272618&qb=64yA7ZWc7Ya17Jq0&enc=utf8&section=kin&rank=1&search_sort=3&spq=0', 'docId': 461272618}])