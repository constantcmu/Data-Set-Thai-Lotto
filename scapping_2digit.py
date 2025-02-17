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
        'prize_2digits': []
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        columns = soup.find_all('div', class_='lottocheck__column')
        if columns:
            for col in columns:
                for num in col.find_all('strong'):
                    if "เลขท้าย 2 ตัว" in col.text:
                        row['prize_2digits'].append(num.text)
            return row
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

columns = ['date', 'prize_2digits']
df = pd.DataFrame(columns=columns)

archive_url = "https://news.sanook.com/lotto/archive/"
header = True

if os.path.exists('lotto_prize_2digit.csv'):
    os.remove('lotto_prize_2digit.csv')

if os.path.exists('lotto_prize_2digit.parquet'):
    os.remove('lotto_prize_2digit.parquet')

while True:
    archive = getArchivePage(archive_url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scappingLotto, archive.archiveList))

    for new_row in results:
        if new_row:
            newDf = pd.DataFrame([new_row])
            df = pd.concat([df, newDf], ignore_index=True)
            newDf.to_csv('lotto_prize_2digit.csv', mode='a', index=False, header=header)
            header = False

    if archive.nextPageUrl == "":
        df.to_parquet('lotto_prize_2digit.parquet', index=False)
        break
    else:
        archive_url = archive.nextPageUrl
