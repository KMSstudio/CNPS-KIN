# number extracting
import re
# url crawling
import requests
from bs4 import BeautifulSoup

#대한통운, 우체국택배, 
constant = {
    'cj': r"%EB%8C%80%ED%95%9C%ED%86%B5%EC%9A%B4",
}

def inquiry_kin(company='cj', questionN=-1):
    res = []

    kin_url = f"https://kin.naver.com/search/list.naver?query={constant[company]}&section=kin&sort=date"
    response = requests.get(kin_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ques_rawlist = soup.select(r"#s_content > div.section > ul > li > dl > dt")
    else: return []
    
    if questionN == -1 or questionN > len(ques_rawlist):
        questionN = len(ques_rawlist)
    for i in range(questionN):
        ques = ques_rawlist[i]

        #get url of question
        head = str(ques).find('href="')
        tail = str(ques).find('"', head+6)
        ques_url = str(ques)[(head+6):tail]
        ques_url = ques_url.replace('&amp;', '&')
        ques_url = ques_url.replace('§', '&s')

        ques_d1id =     ques_url[(ques_url.find('d1id=')+len('d1id=')):ques_url.find('&', ques_url.find('d1id='))]
        ques_dirId =    ques_url[(ques_url.find('dirId=')+len('dirId=')):ques_url.find('&', ques_url.find('dirId='))]
        ques_docId =    ques_url[(ques_url.find('docId=')+len('docId=')):ques_url.find('&', ques_url.find('docId='))]

        #get content
        response = requests.get(ques_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            ques_title = soup.select_one(r"#content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__title > div > div")
            ques_content = soup.select_one(r"#content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__content")
            ques_text = ques_title.get_text().strip() + '  ' + ques_content.get_text().strip() if ques_content is not None else ques_title.get_text().strip()
        else:
            continue

        #get invoice
        ques_numbers = re.findall(r'\d+', ques_text)
        ques_numbers = list(set(ques_numbers))          # remove duplication

        for ques_number in ques_numbers:
            if len(str(ques_number)) < 9:
                continue
            res.append({
                'url': ques_url, 'd1id': ques_d1id, 'dirId': ques_dirId, 'docId': ques_docId,
                'text': ques_text, 'number': ques_number, 'company': company})
    return res

if __name__ == '__main__':
    val = inquiry_kin()
    for res in val:
        print(res)
        print()