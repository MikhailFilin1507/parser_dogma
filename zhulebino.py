import requests
import json
import pandas as pd
from datetime import date
import openpyxl


def parse():

    headers = {
        "accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52"
    }

    url='https://api-selectel.pik-service.ru/v2/filter?type=1,2&location=2,3&block=164&flatPage=3&flatLimit=8&onlyFlats=1'
    req = requests.get(url, headers=headers)
    src = req.text
    data = json.loads(src)

    vol = data['count']

    count_pages = vol // 8 + 1


    dict = {'rooms' : [],
            'price' : [],
            'discount': [],
            'area' : [],
            'sum' : [],
            'priceformeter' : []
    }

    for i in range(1,count_pages+1):
        url = 'https://api-selectel.pik-service.ru/v2/filter?type=1,2&location=2,3&block=164&flatPage=' + str(i) +'&flatLimit=8&onlyFlats=1'
        req = requests.get(url, headers=headers)
        src = req.text
        data = json.loads(src)
        for m in range(8):
            try:
                dict['rooms'].append(data['blocks'][0]['flats'][m]['rooms'])
                dict['price'].append(data['blocks'][0]['flats'][m]['price'])
                dict['discount'].append(data['blocks'][0]['flats'][m]['discount'])
                dict['area'].append(data['blocks'][0]['flats'][m]['area'])
                dict['sum'].append(data['blocks'][0]['flats'][m]['price']*(1-data['blocks'][0]['flats'][m]['discount']/100))
                dict['priceformeter'].append((data['blocks'][0]['flats'][m]['price']*(1-data['blocks'][0]['flats'][m]['discount']/100))/data['blocks'][0]['flats'][m]['area'])

            except:
                pass

    df = pd.DataFrame(dict)
    writer = pd.ExcelWriter(f'data/{str(date.today())}_pik_zhulebino.xlsx')
    df.to_excel(writer, index=False)
    writer._save()
    #writer.close()

    #df = pd.read_excel('data_pik_test.xlsx')
    len = df['rooms'].count()
    stud = df['priceformeter'].loc[df['rooms'] == -1].mean()
    odno = df['priceformeter'].loc[df['rooms'] == 1].mean()
    dva = df['priceformeter'].loc[df['rooms'] == 2].mean()
    tri = df['priceformeter'].loc[df['rooms'] == 3].mean()

    message = (
        f'Дата - {date.today()}.\n'
        f'Зайстройщик - ПИК.\n'
        f'Проект - Измайловский лес. \n'
        f'Средняя цена студий - {stud:.1f} руб/м2.\n'
    f'Средняя цена 1-комнатной - {odno:.1f} руб/м2.\n'
    f'Средняя цена 2-комнатной - {dva:.1f} руб/м2.\n'
    f'Средняя цена 3-комнатной - {tri:.1f} руб/м2.\n'
    f'Всего квартир в продаже - {len} шт.\n'
    '*Данные взяты с сайта pik.ru/zhulebino.')

    return message
