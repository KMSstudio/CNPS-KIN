# number extracting
import re
# url crawling
import requests
from bs4 import BeautifulSoup

#대한통운, 로젠, 우체국택배, 
constant = {
    'cj': r"%EB%8C%80%ED%95%9C%ED%86%B5%EC%9A%B4",
    'lg': r"%EB%A1%9C%EC%A0%A0",
    'po': r"%EC%9A%B0%EC%B2%B4%EA%B5%AD%ED%83%9D%EB%B0%B0"
}

def bn_src(list, data):
    lft = 0; rht = len(list)-1; mid = (lft+rht)//2
    while lft<=rht:
        if data>list[mid]: lft=mid+1
        elif data<list[mid]: rht=mid-1
        else: return mid
        mid=(lft+rht)//2
    return -1

def inquiry_kin(company='cj', page=0):
    res = []
    #get response of kin main src
    kin_url = f"https://kin.naver.com/search/list.naver?query={constant[company]}&section=kin&sort=date" + ('' if not int(page) else f'&page={page}')
    response = requests.get(kin_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ques_rawlist = soup.select(r"#s_content > div.section > ul > li > dl > dt")
    else: return []
    for ques in ques_rawlist:
        #get url of question
        head = str(ques).find('href="')
        tail = str(ques).find('"', head+6)
        ques_url = str(ques)[(head+6):tail]
        ques_url = ques_url.replace('&amp;', '&')
        ques_url = ques_url.replace('§', '&s')
        #extract docIds (deleted)
        #ques_d1id =     ques_url[(ques_url.find('d1id=')+len('d1id=')):ques_url.find('&', ques_url.find('d1id='))]
        #ques_dirId =    ques_url[(ques_url.find('dirId=')+len('dirId=')):ques_url.find('&', ques_url.find('dirId='))]
        #ques_docId =    ques_url[(ques_url.find('docId=')+len('docId=')):ques_url.find('&', ques_url.find('docId='))]
        #get content
        response = requests.get(ques_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            ques_title = soup.select_one(r"#content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__title > div > div")
            ques_content = soup.select_one(r"#content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__content")
            try: ques_text = ques_title.get_text().strip() + '  ' + ques_content.get_text().strip() if ques_content is not None else ques_title.get_text().strip()
            except: continue
        else: continue
        #get invoice
        ques_numbers = re.findall(r'\d+', ques_text)
        #remove duplication
        ques_numbers = list(set(ques_numbers))
        #read record file
        try:
            f = open('./log/invoice.txt', 'r')
            rec = f.read().split(';')
            f.close()
        except: rec = []
        for ques_number in ques_numbers:
            if len(str(ques_number)) < 9: continue
            if bn_src(rec, f"{company}_{ques_number}")!=-1: continue
            res.append({
                'url': ques_url, 'text': ques_text, 'number': ques_number, 'company': company})
    return res

if __name__ == '__main__':
    val = inquiry_kin()
    for res in val:
        print(res)
        print()