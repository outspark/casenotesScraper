from bs4 import BeautifulSoup
import requests
import sys

def save_2_txt(url):
    res = requests.get("https://casenote.kr"+url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('#header > div')[1].getText(strip=True)
    title_rm_space = title.replace(" ","")
    content = soup.select('#mainbar')[0].getText()
    # print(title_rm_space)
    # print(content)
    f = open("casenotes/"+title_rm_space+".txt", "w", encoding="utf-8")
    f.write(str(content))
    f.close()

def save_2_html(url):
    res = requests.get("https://casenote.kr"+url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('#header > div')[1].getText(strip=True).replace(" ","")
    content = soup.select('#mainbar')[0]
    with open("casenotes/html/"+title+".html","w", encoding="utf-8") as f:
        f.write(str(content))
         

def crawler(maxPage, keyword, outputFormat):
    page = 1 
    
    while page <= maxPage:
        collection_url = "https://casenote.kr/search/?q="+keyword+"&p="+str(page)+"&sort=1&cc=3&ct=2" #ct for instance (2 is High Court, 3 Lower District Court)
        col_res = requests.get(collection_url)
        print("Status code:"+str(col_res.status_code))
        col_html = col_res.text 
        soup = BeautifulSoup(col_html, "html.parser")
        for lnk in soup.select('.searched_item a'):
            try: 
                print("Retrieving Casenote...")
                if outputFormat == "1":
                    save_2_txt(lnk['href'])
                else: 
                    save_2_html(lnk['href'])
            except OSError as err:
                print("OS error: {0}".format(err))
                #NOTE: occurs when special chararcter is used in the title
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        page += 1

def main():
    # keyword = sys.argv[1]
    # maxPage = sys.argv[2]
    keyword = input("Keyword to search (키워드1+키워드2):")
    maxPage = input("Number of Index Pages (1 page = 10 cases, max 20):") 
    outputFormat = input("Output (html = 0, txt=1):")
    crawler(int(maxPage),keyword,outputFormat)

main()

