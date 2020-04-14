#!/usr/bin/env python3

from lxml import html
import requests
from pathlib import Path

def currentstats(location, size):
    if size == 'State':
        url = 'https://www.worldometers.info/coronavirus/country/us/'
        tablename = '//table[@id="usa_table_countries_yesterday"]'
        pathstring = './/td[contains(text(), "{}")]'.format(location)
    elif size == 'Country':
        url = 'https://www.worldometers.info/coronavirus/'
        tablename = '//table[@id="main_table_countries_yesterday"]'
        pathstring = './/td/a[contains(text(), "{}")]'.format(location)
    page = requests.get(url)

    tree = html.fromstring(page.content)
    
    for table in tree.xpath(tablename):
        for tr in table.xpath('.//tr'):
            tds = tr.xpath(pathstring)
            if tds:
                current_infections = tr.xpath('.//td[2]/text()')[0].strip().replace('+', '').replace(',', '')
                current_deaths = tr.xpath('.//td[4]/text()')[0].strip().replace('+', '').replace(',', '')
                new_infections = tr.xpath('.//td[3]/text()')[0].strip().replace('+', '').replace(',', '')
                new_deaths = tr.xpath('.//td[5]/text()')[0].strip().replace('+', '').replace(',', '')
                print('')
                print(location)
                print('----------------------------------------')
                print('infection information')
                print("Yesterday's infection count: {}".format(current_infections))
                print("New infections Yesterday: {}".format(new_infections))
                if Path('infectionsrate{}.txt'.format(location)).is_file():
                    infectionsrate = open('infectionsrate{}.txt'.format(location), 'r')
                    infection_rates = infectionsrate.read().splitlines()
                    lastir = infection_rates.pop()
                    print('Infection Growth factor from yesterday: {}'.format(lastir))
                    if len(infection_rates) >= 1:
                        priorir = infection_rates.pop()
                        if float(lastir) > float(priorir):
                            print('Infection Growth factor incress: +{}'.format(float(lastir) - float(priorir)))
                        elif float(lastir) < float(priorir):
                            print('Infection Growth factor decress: -{}'.format(float(priorir) - float(lastir)))
                        else:
                            print('constant Infection growth factor')
                print('')
                print('death information')
                print("Yesteray's death count: {}".format(current_deaths))
                print("New deaths yesterday: {}".format(new_deaths))
                if Path('deathsrate{}.txt'.format(location)).is_file():
                    deathsrate = open('deathsrate{}.txt'.format(location), 'r')
                    death_rates = deathsrate.read().splitlines()
                    lastdr = death_rates.pop()
                    print('Death Growth factor from yesterday: {}'.format(lastdr))
                    if len(death_rates) >= 1:
                        priordr = death_rates.pop()
                        if float(lastdr) > float(priordr):
                            print('Death Growth factor incress: +{}'.format(float(lastdr) - float(priordr)))
                        elif float(lastdr) < float(priordr):
                            print('Death Growth factor decress: -{}'.format(float(priordr) - float(lastdr)))
                        else:
                            print('Constant Death Growth factor')
                print('----------------------------------------')
currentstats("California", 'State')
currentstats("New York", 'State')
currentstats("Nevada", 'State')
currentstats("USA Total", 'State')
currentstats("Italy", 'Country')
currentstats('Spain', 'Country')
