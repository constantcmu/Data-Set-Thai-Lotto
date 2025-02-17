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
        'prize_pre_3digit': [],
        'prize_sub_3digits': []
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        columns = soup.find_all('div', class_='lottocheck__column') 
        if columns:
            for col in columns:
                for num in col.find_all('strong'):
                    if "เลขหน้า" in col.text:
                        row['prize_pre_3digit'].append(num.text)
                    elif "เลขท้าย" in col.text:
                        row['prize_sub_3digits'].append(num.text)
            
            # Adjust prize_pre_3digit and prize_sub_3digits if necessary
            if len(row['prize_pre_3digit']) < 2 and len(row['prize_sub_3digits']) > 2:
                row['prize_pre_3digit'] = row['prize_sub_3digits'][:2]
                row['prize_sub_3digits'] = row['prize_sub_3digits'][2:]

            # Ensure both lists have exactly 2 elements
            row['prize_pre_3digit'].extend([''] * (2 - len(row['prize_pre_3digit'])))
            row['prize_sub_3digits'].extend([''] * (2 - len(row['prize_sub_3digits'])))

            return row
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

columns = ['date', 'prize_pre_3digit', 'prize_sub_3digits']
df = pd.DataFrame(columns=columns)

archive_url = "https://news.sanook.com/lotto/archive/"
header = True

if os.path.exists('lotto_prize_3digit.csv'):
    os.remove('lotto_prize_3digit.csv')

if os.path.exists('lotto_prize_3digit.parquet'):
    os.remove('lotto_prize_3digit.parquet')

while True:
    archive = getArchivePage(archive_url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scappingLotto, archive.archiveList))

    for new_row in results:
        if new_row:
            newDf = pd.DataFrame([new_row])
            df = pd.concat([df, newDf], ignore_index=True)
            newDf.to_csv('lotto_prize_3digit.csv', mode='a', index=False, header=header)
            header = False

    if archive.nextPageUrl == "":
        df.to_parquet('lotto_prize_3digit.parquet', index=False)
        break
    else:
        archive_url = archive.nextPageUrl
