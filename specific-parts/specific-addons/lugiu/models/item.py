# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
import re
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from statistics import median
from datetime import datetime

import pythonwhois
import tldextract
import Levenshtein
from urllib.parse import quote
from proxy_requests import ProxyRequests
import json


RA_HOME = 'https://www.reclameaqui.com.br/'
RA_SEARCH = 'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1' \
            '/companies/search/{0}'
RA_SHORT_NAME = 'https://iosite.reclameaqui.com.br/raichu-io-site-v1/' \
                'company/shortname/{0}'
RA_MARKETPLACE_RANKINGS = "https://iosearch.reclameaqui.com.br/" \
                          "raichu-io-site-search-v1/companies/" \
                          "marketplace-rankings/topBest/{0}?" \
                          "index={1}&offset={2}"
RA_COMPANY_COMPLAINS = "https://iosearch.reclameaqui.com.br/" \
                       "raichu-io-site-search-v1/query/companyComplains" \
                       "/{1}/{2}?company={0}"
RA_COMPLAIN_PUBLIC = "https://iosite.reclameaqui.com.br/raichu-io-site-v1/" \
                     "complain/public/{0}"

IMPORTANCIA = [('indispensavel', 'Indispensável'),
               ('bomter', 'É bom ter'),
               ('perfumaria', 'Perfumaria'),
               ('umdia', 'Um dia, e talvez esse dia nunca chegue...'), ]
STATE = [('pesquisando', 'Pesquisando'),
         ('comprado', 'Comprado'), ]


class RAAbstract(object):

    """
    Abstração das funções básicas para o Crawler
    """

    __user_agent = None
    from proxy_requests import ProxyRequests
    import json

    def get(self, url):
        headers = {"User-Agent": self.user_agent}

        req = self.ProxyRequests(url)
        req.set_headers(headers)
        req.get_with_headers()

        return self.json.loads(req.get_raw().decode())

    @property
    def user_agent(self) -> str:
        from fake_useragent import UserAgent

        if self.__user_agent is None:
            self.__user_agent = UserAgent().random

        return self.__user_agent


class RASearch(RAAbstract):
    """
    Instância para buscar termos no Reclame Aqui
    """

    __response = None

    def __init__(self, query: str):
        """
        Na inicialização é realizada a requisição com as headers, e obtendo
        a resposta JSON da mesma para permitir as demais propriedades.
        :param query:
        """
        headers = {"User-Agent": self.user_agent}

        req = ProxyRequests(RA_SEARCH.format(quote(query.encode("utf-8"))))
        req.set_headers(headers)
        req.get_with_headers()

        self.__response = json.loads(req.get_raw().decode())

    @property
    def companies(self):
        """
        Lista de empresas encontradas
        :return:
        """
        data = self.__response
        for company in data.get("companies", []):
            yield self.__fix_company(company)

    def __fix_company(self, data: dict):
        """
        Corrige o dict da empresa
        :param data:
        :return:
        """
        def fix_company_index(index: str):
            """
            O index da empresa vem como texto no padrão:
            (chave=valor, chave=valor)
            é necessário que estes valores sejam separados
            e transformados em dict

            :param index:
            :return:
            """

            data = {}
            index = index[1:-1]
            indexes = index.split(",")

            for indx in indexes:
                indx = str(indx).strip()
                vals = indx.split("=")
                data[vals[0]] = vals[1]

            return data

        data["companyIndex6Months"] = fix_company_index(
            data.get("companyIndex6Months", ""))

        return data


class Item(models.Model):
    _name = "item"
    _rec_name = 'name'

    name = fields.Char(
        string='Nome',
        requered=True,
    )

    state = fields.Selection(
        string='Status',
        selection=STATE,
        default='pesquisando',
    )

    necessario_buscar = fields.Boolean(
        string='Pesquisar?',
        default=False,
    )

    comodo_id = fields.Many2one(
        comodel_name='comodo',
        string='Comodo',
    )

    quantidade = fields.Integer(
        string='Quantidade',
        default=1,
    )

    importancia = fields.Selection(
        selection=IMPORTANCIA,
        default='indispensavel',
        string='Importância',
    )

    valor_pg = fields.Float(
        string='Valor pago',
    )

    caracteristica_item_ids = fields.One2many(
        comodel_name='caracteristica.item',
        inverse_name='item_id',
        string='Caracteristicas',
    )

    valor_estimado = fields.Float(
        string='Valor estimado(und)',
        compute='_compute_valor_estimado',
    )

    @api.depends('caracteristica_item_ids')
    def _compute_valor_estimado(self):
        for rec in self:
            preco = rec.caracteristica_item_ids.filtered(
                lambda x: x.categoria_id.name == 'Preço')

            rec.valor_estimado = median([preco.de, preco.ate])

    busca_ids = fields.One2many(
        comodel_name='busca',
        inverse_name='item_id',
        string='Buscas',
    )

    total_estimado = fields.Float(
        string='Total estimado',
        compute='_compute_total_estimado',
    )

    @api.depends('quantidade', 'valor_estimado')
    def _compute_total_estimado(self):
        for rec in self:
            rec.total_estimado = rec.valor_estimado*rec.quantidade

    @api.multi
    def buscar(self):
        for rec in self:
            caracteristica_ids = rec.caracteristica_item_ids
            valor_id = caracteristica_ids.search(
                [('item_id', '=', rec.id),
                 ('categoria_id.name', '=', 'Preço')])

            categoria_ids = caracteristica_ids.search(
                [('categoria_id.name', '!=', 'Preço'),
                 ('item_id', '=', rec.id)])

            param = {'valor': {'de': valor_id.de, 'ate': valor_id.ate},
                     'param': {}}

            for categoria in categoria_ids:
                name = categoria.categoria_id.name
                if categoria.de:
                    param['param'][name] = {'de': categoria.de,
                                            'ate': categoria.ate}
                else:
                    param['param'][name] = {
                        'val': [parametro.name for parametro in
                                categoria.parametro_ids]}

            url_master = 'https://www.google.com.br/search?cr=countryBR&q=' + \
                         rec.name + '&source=lnms&tbm=shop&start=0'

            categoria_list = [key for key in list(param['param'].keys())]

            res = self.getLeftNav(url_master)

            filtro_vls = self.filtro_vl(res['d'], param=param['valor'])
            url_filtros = [res['d2'][val] for val in filtro_vls]

            for url in url_filtros:
                res = self.getLeftNav(url)
                ref = {d: res['d'][d] for d in res['d'] if
                       'Limpar' not in res['d'][d][0] and d in categoria_list}

                filtros = self.filtro_param(ref=ref, param=param['param'])

                link = res['d2'][filtros[0]]
                for filtro in filtros[1:]:
                    res1 = self.getLeftNav(link)
                    lista = \
                        [res1['d'][key] for key in param['param'].keys() if
                         key in res1['d'].keys() and 'Limpar' not in res1['d'][
                             key] and filtro in res1['d'][key]]
                    if lista:
                        link = res1['d2'][filtro]

                res2 = self.getLeftNav(link)

                res = self.visu(soup=res2['soup'], link=link)

                for i in range(len(res)):
                    try:
                        val = res[i]
                        val[0] = val[0].replace(' ...', '')
                        val[3] = self.busca_site(val[0]) or val[3]

                        conf = 'vai_fundo' if self.reclame_aqui(
                            url=val[3]) >= 2 else 'estranho'

                        data = {'item_id': self.id, 'name': val[0],
                                'descricao': val[1], 'preco': val[2],
                                'url': '<a href="{}" target="_blank">Link'
                                       '</a>'.format(val[3]),
                                'confianca': conf}

                        self.busca_ids.create(data)
                    except:
                        pass

    def check_confianca(self, url):
        confianca = 0
        domain = tldextract.extract(url)

        try:
            w = pythonwhois.get_whois('.'.join([domain.domain, domain.suffix]))
            existencia = ((datetime.now() - w['creation_date'][0]).days / 360)\
                if 'creation_date' in w else 0
            confianca = confianca+1 if existencia > 8 else confianca

        except:
            pass

        try:
            search = RASearch(query=domain.domain)
            for company in search.companies:
                if Levenshtein.distance(
                        str(domain.domain).lower(),
                        str(company['companyName']).lower()) <= 3:

                    break

            confianca = confianca+2 if company['companyIndex6Months']['status'] \
                                       == 'GOOD' else confianca

        except:
            pass

        return confianca

    def busca_site(self, name):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Chrome()
        driver.get('https://www.google.com.br/search?cr=countryBR&q=' + name +
                   '&source=lnms&tbm=shop&start=0')

        self.wait_element(driver=driver, by=By.XPATH,
                          element='//*/div[text()="CLASSIFICAR POR: PADRÃO"]')

        self.wait_element(driver=driver, by=By.XPATH,
                          element='//*/div[text()="PREÇO - '
                                  'DO MENOR PARA O MAIOR"]', )

        link = self.wait_element(
            driver=driver, element=name, by=By.PARTIAL_LINK_TEXT) \
            if self.wait_element(driver=driver, element=name,
                                 by=By.PARTIAL_LINK_TEXT) \
            else self.wait_element(driver=driver, by=By.XPATH,
                                   element='//*/div[text()="Melhor correspondê'
                                           'ncia"]/../div/div/div/div/a')
        try:
            link1 = self.wait_element(driver=driver, element='Visitar site',
                                      by=By.PARTIAL_LINK_TEXT).\
                get_attribute('href') or link

            driver.get(link1)
        except:
            driver.get(link)

        link = driver.current_url

        return link

    def wait_element(self, driver, element, by, val=False,
                     click=True, tempo=20):
        wait = WebDriverWait(driver, tempo)
        try:
            e = wait.until(EC.visibility_of_element_located((by, element)))
            if val:
                e.clear()
                e.send_keys(Keys.HOME + val)

            if click:
                e.click()

            return e
        except:
            return False

    def verifica_link(self, res1, filtros, link):
        keys = res1['d2'].keys()

        for i in keys:
            if i.lower() in filtros.lower():
                link = res1['d2'][i]

        return link

    def getLeftNav(self, url):
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
                    url = 'https://www.google.com.br' + k[e][0].replace(
                        '&amp;', '&')+"&cr=countryBR"
                    d2[values[e]] = url
                except:
                    pass

            d[key] = values

        res = {'soup': soup, 'd': d, 'd2': d2}

        return res

    def visu(self, soup, link):
        j1 = soup.find_all('div', {'class': 'g'})
        j2 = [j.find_all('div', {'class': 'pslires'}) for j in j1]

        data = {i: [] for i in range(len(j2))}

        for i in range(len(j2)):
            try:
                name = j2[i][0].find_all('a')[1].text
                data[i].append(name)
            except:
                data[i].append(False)

            try:
                desc = j2[i][0].find_all('div')[5].text
                data[i].append(desc)
            except:
                data[i].append(False)

            try:
                price = j2[i][0].find_all('div')[2].text.replace('\xa0', ' ')
                price = float(price.replace('R$ ', '').
                              replace('.', '').replace(',', '.'))
                data[i].append(price)
            except:
                data[i].append(False)

            data[i].append(link)

        return data

    def val_vl(self, val, param):
        if 'Acima' in val:
            return False

        lista = val.replace('Até R$ ', '').replace('.', '').replace(',', '') \
            if 'Até R$ ' in val else val.replace('R$', '').replace(' ', ''). \
            replace('.', '').replace(',', '.').split('–')

        if isinstance(lista, list):
            if float(lista[0]) >= param['de'] and \
                    float(lista[1]) <= param['ate']:
                return True

        elif float(lista) <= param['ate']:
            return True

        return False

    def filtro_vl(self, d, param):
        fil_vl = [k for k in d['Preço'] if self.val_vl(val=k, param=param)]

        return fil_vl

    def val_param(self, ref, param):
        res = []
        for val in ref:
            if 'de' in param:
                r = re.findall('\d+', val)
                if len(r) == 2:
                    if param['de'] <= float(r[0]) and \
                            float(r[1]) <= param['ate']:
                        res.append(val)

                elif len(r) == 1 and 'Acima' not in val:
                    if param['de'] <= float(r[0]) <= param['ate']:
                        res.append(val)

            else:
                for p in param['val']:
                    if p in val:
                        res.append(val)

        return res

    def filtro_param(self, ref, param):
        fil_list = []
        for k in ref.keys():
            for r in self.val_param(ref=ref[k], param=param[k]):
                fil_list.append(r)

        return fil_list
