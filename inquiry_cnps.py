# url crawling
import requests
from bs4 import BeautifulSoup
# for json values
import json

def inquiry_cnps(number=583489878674, company='cj'):
    res = { 'success': False }

    url = f"http://cnps.site/api/makesrc?number={number}&company={company}"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        inq = json.loads(soup.text)
    else: return res
    
    if inq['success'] == False:
        res['msg'] = inq['msg']
        return res
    
    inq_msg = f"안녕하십니까 통계기반배송도착시간 예측 서비스 개발자 {'강시우'}입니다.\n\
질문자님의 택배가 {inq['target']['location']}에 있습니다. \n\
{inq['target']['location']}에 {inq['target']['status']}된 택배들 중 \n\n\
25%가 {inq['predict']['p25']}\n\
50%가 {inq['predict']['p50']}\n\
75%가 {inq['predict']['p75']}\n\
95%가 {inq['predict']['p95']}\n\
안으로 도착했습니다.\n\n\
{inq['predict']['pred']['range']}선으로 추정한 도착예정시간은 {inq['predict']['pred']['value']}입니다.\n\
더 자세한 정보는 아래 url에서 확인가능합니다.\n{url}"
    
    res = {'success': True, 'msg': inq_msg}#, 'inq': inq}
    return res

if __name__ == '__main__':
    print(inquiry_cnps()['msg'])