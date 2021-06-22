import requests
import bs4
import os


URL = 'https://developer.android.com/reference/android/app/package-summary'
res = requests.get(URL)
soup = bs4.BeautifulSoup(res.text, "html.parser")
soup = soup.find_all("td", {"class": "jd-linkcol"})
table = bs4.BeautifulSoup(str(soup), "html.parser")
os.makedirs('outFiles', exist_ok=True)
for a in table.find_all('a', href=True):
    link = "https://developer.android.com"
    link += a['href']
    word = a["href"].split('/')
    className = word[len(word)-1]
    res = requests.get(link)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    tags = soup.select(".caution")
    tags_two = soup.select(".note")
    i = 0
    f = None
    if len(tags) or len(tags_two) > 0:
        f = open("outfiles/"+className, "w")
    while i in range(len(tags)):
        node = tags[i].parent
        while(node.name != "div"):
            node = node.parent
        api_title = node.select(".api-title")
        x = node.select('.caution')
        if len(api_title) == 0:
            api_title = node.select(".api-name")
        for ele in x:
            out = api_title[0].getText() + ":" + tags[i].getText()
            out = out.replace('\n', " ")
            out = out.replace('\t', " ")
            f.write(out+'\n')
            i += 1

    while i in range(len(tags_two)):
        node = tags_two[i].parent
        while(node.name != "div"):
            node = node.parent
        api_title = node.select(".api-title")
        x = node.select('.note')
        if len(api_title) == 0:
            api_title = node.select(".api-name")
        for ele in x:
            out = api_title[0].getText() + ":" + tags_two[i].getText()
            out = out.replace("\n", " ")
            out = out.replace('\t', " ")
            f.write(out+'\n')
            i += 1
    if f:
        f.close()
