from bs4 import BeautifulSoup
import requests
import sys
import time

def save_2_txt(url):
    res = requests.get("https://casenote.kr"+url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    title = ""
    print(title+"downloaded.")
    try:
        title = soup.select('#header > div')[1].getText(strip=True).replace(" ","")
        content = soup.select('#mainbar')[0].getText()
    except:
        print("Could not save {0} as text.".format(url))
    if len(title) > 0:
        f = open(title+".txt", "w", encoding="utf-8")
        f.write(str(content))
        f.close()

def opt_2_query(option_court, option_period, option_case): 
    court = "&court="+str(option_court)
    period = "&period"+str(option_period)
    case = "&case"+str(option_case)
    opts = [court, period, case]
    return opts #returns formatted list of user options

def crawler(keyword, opts):
    for page in range(20):
        #NOTE: Using CaseNote's updated url format (2021.04.14)
        collection_url = "https://casenote.kr/search/?q="+keyword+"&sort=0&"+opts[0]+opts[1]+opts[2]+"&page="+str(page) 
        col_res = requests.get(collection_url)
        if col_res.status_code == 200:
            col_html = col_res.text
            soup = BeautifulSoup(col_html, "html.parser") #Creates soup obj for parsing 
            for lnk in soup.select('.searched_item a'):
                time.sleep(3)
                try:
                    print("Retrieving Casenote...")
                    save_2_txt(lnk['href'])
                except OSError as err:
                    print("OS error: {0}".format(err))
                    #NOTE: occurs when special chararcter is used in the title
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
        else:
            print("Status code:"+str(col_res.status_code))
        

def main():
    keyword = input("Keyword to search (키워드1+키워드2):")

    print("대법원=0, 고등법원·특허법원=1, 지방법원·행정법원·가정법원=2, 헌법재판소=3")
    option_court = input("Option[법원숫자&법원숫자]:")

    print("전체=0, 최근 3년=1, 최근 5년=2, 최근 10년=3, 직접입력=4")
    option_period = input("Option[기간숫자]:")

    print("민사=0, 형사=1, 행정=2")
    option_case = input("Option[사건종류&사건종류]:")

    user_opts = opt_2_query(option_court, option_period, option_case)
    crawler(keyword, user_opts)

if __name__ == '__main__':
    main()

