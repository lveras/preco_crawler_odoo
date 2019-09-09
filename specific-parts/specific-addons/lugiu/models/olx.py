# -*- coding: utf-8 -*-
from odoo import models, fields, api
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_element(driver, element, by, val=False,
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

    driver = webdriver.Chrome()
    driver.get('https://rj.olx.com.br/rio-de-janeiro-e-regiao/zona-sul/imo'
               'veis/aluguel?pe=1800&ros=1&sd=2218&sd=2223&sd=2231&sp=1&ss=2')

