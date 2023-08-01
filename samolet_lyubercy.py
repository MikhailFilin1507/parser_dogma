import requests
import json
import pandas as pd
from datetime import date

def parse():

    headers = {
        "accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52"
    }


    url = 'https://samolet.ru/api_redesign/flats/?free=1&ordering=-order_manual,filter_price_package,pk&project=2&offset=0&limit=12'
    req = requests.get(url, headers=headers)
    src = req.text
    data = json.loads(src)

    vol = data['count']

    count_pages = vol // 12 + 1

    dict = {'rooms': [],
            'price': [],
            'discount': [],
            'area': [],
            'sum': [],
            'priceformeter': []
            }


    for i in range(0, (count_pages+1)*12, 12):
        url = 'https://samolet.ru/api_redesign/flats/?project=2&from=project&ordering=-order_manual,filter_price_package,pk&free=1&offset=' + str(i) + '&limit=12'
        #url = 'https://erzrf.ru/erz-rest/api/v1/gk/table?region=moskva&regionKey=143443001&costType=1&page=' + str(i) + '&sortType=cmxrating&min=11&max=20'
        req = requests.get(url, headers=headers)
        src = req.text
        data = json.loads(src)

        for m in range(12):
            try:
                dict['rooms'].append(data['results'][m]['rooms'])
                dict['price'].append(data['results'][m]['price'])
                dict['discount'].append(data['results'][m]['discount'])
                dict['area'].append(data['results'][m]['area'])
                dict['sum'].append(data['results'][m]['price'] * (1 - data['results'][m]['discount'] / 100))
                dict['priceformeter'].append((data['results'][m]['price'] * (1 - data['results'][m]['discount'] / 100)) / data['results'][m]['area'])
            except:
                pass

    df = pd.DataFrame(dict)
    writer = pd.ExcelWriter(f'data/{str(date.today())}_smlt_lyubercy.xlsx')
    df.to_excel(writer, index=False)
    writer._save()

    len = df['rooms'].count()
    stud = df['priceformeter'].loc[df['rooms'] == 0].mean()
    odno = df['priceformeter'].loc[df['rooms'] == 1].mean()
    dva = df['priceformeter'].loc[df['rooms'] == 2].mean()
    tri = df['priceformeter'].loc[df['rooms'] == 3].mean()

    message = (
        f'Дата - {date.today()}.\n'
        f'Застройщик - Самолет.\n'
        f'Проект - Люберцы. \n'
        f'Средняя цена студий - {stud:.1f} руб/м2.\n'
    f'Средняя цена 1-комнатной - {odno:.1f} руб/м2.\n'
    f'Средняя цена 2-комнатной - {dva:.1f} руб/м2.\n'
    f'Средняя цена 3-комнатной - {tri:.1f} руб/м2.\n'
    f'Всего квартир в продаже - {len} шт.\n'
    '*Данные взяты с сайта samolet.ru/project/lyubercy/.')

    return message

