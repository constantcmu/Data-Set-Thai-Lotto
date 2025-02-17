import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
import pandas as pd
import os
import concurrent.futures

@dataclass
class ArchivePage:
    archiveList: List[str]
    nextPageUrl: str

def getArchivePage(url):
    print(f"Page = {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        nextPageUrl = ""
        lotto = []
        for link in soup.find_all('a', class_='pagination__item--next'):
            nextPageUrl = link.get('href')
            break

        divContent = soup.find(
            'div', class_=['box-cell', 'box-cell--lotto', 'content'])

        for link in divContent.find_all('a'):
            lottoUrl = link.get('href')
            if "/lotto/check/" in lottoUrl:
                lotto.append(lottoUrl)

        return ArchivePage(archiveList=lotto, nextPageUrl=nextPageUrl)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def getDate(url):
    d = url.split("/")
    while ("" in d):
        d.remove("")
    dateStr = d[len(d)-1]
    date = dateStr[0:2]
    month = dateStr[2:4]
    year = str(int(dateStr[4:8])-543)
    return f"{year}-{month}-{date}"

def scappingLotto(url):
    if url == 'https://news.sanook.com/lotto/check/ผลสลากกินแบ่งรัฐบาลงวดประจำวันที่1สิงหาคม2552/':
        url = 'https://news.sanook.com/lotto/check/01082552/'

    response = requests.get(url)
    date = getDate(url)
    print(f'{date} = {url}')

    row = {
        'date': date,
        'nearby_1st': []
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='lottocheck__sec--nearby')
        if div:
            for ele in div.find_all('strong', class_="lotto__number"):
                row['nearby_1st'].append(ele.text)
            return row
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

columns = ['date', 'nearby_1st']
df = pd.DataFrame(columns=columns)

archive_url = "https://news.sanook.com/lotto/archive/"
header = True

if os.path.exists('lotto_nearby_1st.csv'):
    os.remove('lotto_nearby_1st.csv')

if os.path.exists('lotto_nearby_1st.parquet'):
    os.remove('lotto_nearby_1st.parquet')

while True:
    archive = getArchivePage(archive_url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scappingLotto, archive.archiveList))

    for new_row in results:
        if new_row:
            newDf = pd.DataFrame([new_row])
            df = pd.concat([df, newDf], ignore_index=True)
            newDf.to_csv('lotto_nearby_1st.csv', mode='a', index=False, header=header)
            header = False

    if archive.nextPageUrl == "":
        df.to_parquet('lotto_nearby_1st.parquet', index=False)
        break
    else:
        archive_url = archive.nextPageUrl
