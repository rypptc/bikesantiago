import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from .models import Proyecto
import json
from django.db import transaction
from datetime import datetime, date
import os


def open_page(page_number, driver):
    dropdown = Select(driver.find_element('name', 'pagina_offset'))
    dropdown.select_by_index(page_number - 1)
    driver.implicitly_wait(2.5)
    table_data = get_table_data(driver.page_source)


def get_table_data(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table', {'class': 'tabla_datos'})
    rows = table.find_all('tr')

    proyectos = []

    for row in rows:
        cells = row.find_all('td')
        if cells:
            cell_data = [cell.get_text(strip=True) for cell in cells]
            if not cell_data[0]:
                continue
            proyecto = {
                'id': cell_data[0],
                'nombre': cell_data[1],
                'tipo': cell_data[2],
                'region': cell_data[3],
                'tipologia': cell_data[4],
                'titular': cell_data[5],
                'inversion': float(cell_data[6].replace('.', '').replace(',', '.')),
                'ingreso': datetime.strptime(cell_data[7], '%d/%m/%Y').date(),
                'estado': cell_data[8]
            }
            proyectos.append(proyecto)

    with open('seiadata.json', 'ab+') as f:
        f.seek(0, os.SEEK_END)
        if f.tell() == 0:
            f.write(b'[')
        else:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char == b']':
                f.seek(-1, os.SEEK_END)
                f.truncate()
                f.write(','.encode())
            else:
                f.write(','.encode())
        f.write(json.dumps(proyectos, default=str, ensure_ascii=False)[1:].encode())


def scrape_pages(start_page, end_page):
    url = 'https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php'
    driver = webdriver.Chrome()
    driver.get(url)
    for page in range(start_page, end_page+1):
        open_page(page, driver)
    driver.quit()

def populate_db_from_json(json_file):
    with open(json_file, 'r') as f:
        proyectos = json.load(f)

    with transaction.atomic():
        for proyecto in proyectos:

            fecha_ingreso = datetime.strptime(proyecto['ingreso'], '%Y-%m-%d')

            p = Proyecto()
            p.id = proyecto['id']
            p.nombre = proyecto['nombre']
            p.tipo = proyecto['tipo']
            p.region = proyecto['region']
            p.tipologia = proyecto['tipologia']
            p.titular = proyecto['titular']
            p.inversion = proyecto['inversion']
            p.ingreso = fecha_ingreso
            p.estado = proyecto['estado']
            p.save()
