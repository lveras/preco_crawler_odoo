import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os.path

global l
l = []

dir_path = os.path.dirname(os.path.realpath(__file__))


def getLeftNav(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    # Scrap
    i1 = soup.find_all('td', {"id": "leftnav"})
    i2 = i1[0].find_all('ul')
    i3 = [i.find_all('li') for i in i2]

    try:
        if 'Effacer' in str(i3[len(i3) - 1][1]):
            i3 = i3[0:len(i3) - 1]
    except:
        pass

    d = {}
    d2 = {}

    # Filling of the 2 dictionaries 
    for j in range(1, len(i3)):
        i4 = [i.find_all('a') for i in i3[j]]
        p = re.compile('(?<=\")(.*?)(?=\")')
        k = [p.findall(str(i)) for i in i4]
        k = k[1:len(k)]
        i5 = [i.text for i in i3[j]]
        key = i5[0]
        values = i5[1:]
        values = [i.replace('\xa0', ' ') for i in values]
        values = [i for i in values if i not in 'Effacer']

        for e in range(len(values)):
            try:
                url = 'https://www.google.com' + k[e][0].replace('&amp;', '&')
                d2[values[e]] = url

            except:
                pass

        d[key] = values

    return soup, d, d2

def visu(soup):
    j1 = soup.find_all('div', {'class': 'g'})
    j2 = [j.find_all('div', {'class': 'pslires'}) for j in j1]

    data = {'Name': [], 'Preco': [], 'Loja': [], 'Descrição': []}

    for i in range(len(j2)):
        try:
            name = j2[i][0].find_all('a')[1].text
            data['Name'].append(name)
        except:
            data['Name'].append('none')

        try:
            price = j2[i][0].find_all('div')[2].text.replace('\xa0', ' ')
            reta = j2[i][0].find_all('div')[3].text.replace('\xa0', ' ')
            data['Preco'].append(price)
            data['Loja'].append(reta)
        except:
            data['Preco'].append('none')
            data['Loja'].append('none')

        try:
            desc = j2[i][0].find_all('div')[5].text
            data['Descrição'].append(desc)
        except:
            data['Descrição'].append('none')

    df = pd.DataFrame(data=data)
    print(df)


def val_vl(vals, param):
    if 'R$' in vals and '–' in vals:
        lista = vals.replace('R$', '').replace(' ', '').replace('.', '').\
            replace(',', '.').split('–')

        if len(lista) > 1:
            if float(lista[0]) >= param['de'] and \
                    float(lista[1]) <= param['ate']:
                return True

    return False


def filtro_vl(d2, param):
    fil_vl = [d2[k] for k in d2.keys() if val_vl(vals=k, param=param)]

    return fil_vl


def val_param(val, param_key, param):
    if param_key in val:
        if param[param_key]['tipo'] == 'int':
            res = int(re.findall('\d+', val)[0])
            if param[param_key]['de'] <= res <= param[param_key]['ate']:
                return True
        if param[param_key]['tipo'] == 'str':

    return False


def filtro_param(d2, param):
    for p in param.keys():
        fil_p = [d2[k] for k in d2.keys()
                 if val_param(val=k, param_key=p, param=param)]


req = 'Geladeira'
url_master = 'https://www.google.com/search?q=' + req + \
             '&source=lnms&tbm=shop&start=0'

param = {'valor': {'de': 1000, 'ate': 2000},
         'param': {
             'litros': {'tipo': 'int', 'de': 300, 'ate': 500, 'val': ''},
             'frost free': {'tipo': 'str', 'de': '', 'ate': '',
                            'val': 'Frost Free'},
             'duplex': {'tipo': 'str', 'de': '', 'ate': '',
                        'val': 'Duplex'},
             'inox': {'tipo': 'str', 'de': '', 'ate': '',
                      'val': 'inox'}, }}

soup, d, d2 = getLeftNav(url_master)

url_filtro_vls = filtro_vl(d2, param=param['valor'])

url_filtros = []

for url in url_filtro_vls:
    soup, d, d2 = getLeftNav(url)
    for p in param['param']:
        for u in filtro_param(d2=d2, param=param['param']):
            url_filtros.append(u)
