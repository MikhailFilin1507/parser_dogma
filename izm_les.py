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

    url='https://api-selectel.pik-service.ru/v2/filter?type=1,2&location=2,3&block=90&flatPage=3&flatLimit=8&onlyFlats=1'
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
        url = 'https://api-selectel.pik-service.ru/v2/filter?type=1,2&location=2,3&block=90&flatPage=' + str(i) +'&flatLimit=8&onlyFlats=1'
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
    writer = pd.ExcelWriter(f'data/{str(date.today())}_pik_izm_les.xlsx')
    df.to_excel(writer, index=False)
    writer._save()


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
    '*Данные взяты с сайта pik.ru/i-les.')

    return message


#
#
# ans = {}
#
# for i in range(len(list_id)):
#     url = 'https://erzrf.ru/erz-rest/api/v1/gk/list-map/?gkId='+ str(list_id[i]) + '&region=moskva&regionKey=143443001&costType=1&sortType=qrooms'
#     req = requests.get(url, headers=headers)
#     src = req.text
#     data = json.loads(src)
#     ans['apartmentsCountAll'] = data['list'][0]['apartmentsCountAll']
#     ans['apartmentsCountMonitoring'] = data['list'][0]['apartmentsCountMonitoring']
#     ans['apartmentsCountSales'] = data['list'][0]['apartmentsCountSales']
#     ans['complexType'] = data['list'][0]['complexType']
#     ans['erzMark'] = data['list'][0]['erzMark']
#     ans['filteredApartmentsCount'] = data['list'][0]['filteredApartmentsCount']
#     ans['filteredObjectsCount'] = data['list'][0]['filteredObjectsCount']
#     ans['floorsFrom'] = data['list'][0]['floorsFrom']
#     ans['floorsTo'] = data['list'][0]['floorsTo']
#     ans['gkAddress'] = data['list'][0]['gkAddress']
#     ans['gkClass'] = data['list'][0]['gkClass']
#     ans['gkId'] = data['list'][0]['gkId']
#     ans['gkName'] = data['list'][0]['gkName']
#     ans['latitude'] = data['list'][0]['latitude']
#     ans['longitude'] = data['list'][0]['longitude']
#     ans['maxSquare'] = data['list'][0]['maxSquare']
#     ans['metro'] = data['list'][0]['metro']
#     ans['minApartmentCost'] = data['list'][0]['minApartmentCost']
#     ans['minApartmentCostM2'] = data['list'][0]['minApartmentCostM2']
#     ans['objectsCountAll'] = data['list'][0]['objectsCountAll']
#     ans['wallMaterial'] = data['list'][0]['wallMaterial']
#
#     url = 'https://erzrf.ru/erz-rest/api/v1/gk/advantages/'+ str(list_id[i])
#     req = requests.get(url, headers=headers)
#     src = req.text
#     data = json.loads(src)
#
#     for n in range(len(data)):
#         for m in range(len(data[n]['values'])):
#             ans[str(data[n]['values'][m]['name'])] = data[n]['values'][m]['mark']
#
#
#



# build = {
#     0: "Строится",
#     1: "Сдан"
# }
#
# url1 = 'https://erzrf.ru/erz-rest/api/v1/gk/advantages/11971083001'
# req = requests.get(url1, headers=headers)
# src = req.text
# data = json.loads(src)
# for i in range(len(data)):
#     for k in range(len(data[i]['values'])):
#         table_dog[0].append(str(data[i]['values'][k]['name']))
#
# url2 =  'https://erzrf.ru/erz-rest/api/v1/gk/advantages/'
# for n in range(len(table_dog)-1):
#     url3 = url2+str(table_dog[n+1][1])
#     req = requests.get(url3, headers=headers)
#     src = req.text
#     data = json.loads(src)
#     for i in range(len(data)):
#         for k in range(len(data[i]['values'])):
#             table_dog[n+1].append(data[i]['values'][k]['mark'])
#
# table_dog[0].append('Итоговая оценка')
#
# url4 = 'https://erzrf.ru/erz-rest/api/v1/gk/index/'
# for n in range(len(table_dog)-1):
#     url5 = url4+str(table_dog[n+1][1])
#     requ = requests.get(url5, headers=headers)
#     srcu = requ.text
#     data = json.loads(srcu)
#     try:
#         table_dog[n+1].append(data['erzMark'])
#     except:
#         table_dog[n + 1].append('Нет данных')
#

#
#


