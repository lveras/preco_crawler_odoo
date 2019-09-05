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

    res = {'soup': soup, 'd': d, 'd2': d2}

    return res


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

    df.reindex(columns=list(data.keys()))

    return df


def val_vl(val, param):
    if 'Acima' in val:
        return False

    lista = val.replace('Até R$ ', '').replace('.', '').replace(',', '') \
        if 'Até R$ ' in val else val.replace('R$', '').replace(' ', '').\
        replace('.', '').replace(',', '.').split('–')

    if isinstance(lista, list):
        if float(lista[0]) >= param['de'] and float(lista[1]) <= param['ate']:
            return True

    elif float(lista) <= param['ate']:
        return True

    return False


def filtro_vl(d, param):
    fil_vl = [k for k in d['Preço'] if val_vl(val=k, param=param)]

    return fil_vl


def val_param(ref, param):
    res = []
    for val in ref:
        if param['tipo'] == 'int':
            r = int(re.findall('\d+', val)[0])
            if param['de'] <= r <= param['ate']:
                res.append(val)
        if param['tipo'] == 'str':
            if val in param['val']:
                res.append(val)
        if param['tipo'] == 'list':
            for p in param['val']:
                if p in val:
                    res.append(val)

    return res


def filtro_param(ref, param):
    fil_list = []
    for k in ref.keys():
        for r in val_param(ref=ref[k], param=param[k]):
            fil_list.append(r)

    return fil_list


req = 'Geladeira'
url_master = 'https://www.google.com/search?q=' + req + \
             '&source=lnms&tbm=shop&start=0'

param = {'valor': {'de': 1000, 'ate': 2000},
         'param': {'Capacidade': {'tipo': 'int', 'de': 300, 'ate': 500},
                   'Marca': {'tipo': 'list', 'val':
                       ['Brastemp', 'Panasonic', 'Consul', 'Samsung']},
                   'Recursos': {'tipo': 'list', 'val':
                       ['Frost Free', 'Aço inox']}}}

categoria_list = [key for key in list(param['param'].keys())]

res = getLeftNav(url_master)

filtro_vls = filtro_vl(res['d'], param=param['valor'])
url_filtros = [res['d2'][val] for val in filtro_vls]


def verifica_link(res1, filtros, link):
    keys = res1['d2'].keys()

    for i in keys:
        if i.lower() in filtros.lower():
            link = res1['d2'][i]

    return link


for url in url_filtros:
    res = getLeftNav(url)
    ref = {d: res['d'][d] for d in res['d'] if
           'Limpar' not in res['d'][d][0] and d in categoria_list}

    filtros = filtro_param(ref=ref, param=param['param'])

    link = res['d2'][filtros[0]]
    for filtro in filtros[1:]:
        res1 = getLeftNav(link)
        lista = [res1['d'][key] for key in param['param'].keys() if
                 key in res1['d'].keys() and 'Limpar' not in res1['d'][
                     key] and filtro in res1['d'][key]]
        if lista:
            link = res1['d2'][filtro]

    res2 = getLeftNav(link)

    df = visu(soup=res2['soup'])

