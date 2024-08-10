import json

from bs4 import BeautifulSoup
# import requests

# url = 'https://www.iana.org/domains/root/db'
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
# }
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('parser\index.html', 'w', encoding="utf-8") as file:
#     file.write(src)

with open('parser\index.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src)
all_tld = soup.find_all(class_='domain tld')

all_tld_list = []
for tld in all_tld:
    children = tld.find_all()

    for child in children:
        all_tld_list.append(child.text)


with open('parser\ all_tdl.json', 'w', encoding="utf-8") as file:
    json.dump(all_tld_list, file, indent=4, ensure_ascii=False)


