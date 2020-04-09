#!/usr/bin/env python3

from lxml import html
import requests
import DateTime
import time
from pathlib import Path

def findstats(location, size):
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
    if Path('new_deaths_{}.txt'.format(location)).is_file() and Path('new_infections_{}.txt'.format(location)).is_file():
        deathsfile = open("new_deaths_{}.txt".format(location), "a")
        infectionfile = open("new_infections_{}.txt".format(location), "a")
    else:
        deathsfile = open("new_deaths_{}.txt".format(location), "w+")
        infectionfile = open("new_infections_{}.txt".format(location), "w+")
    for table in tree.xpath(tablename):
        for tr in table.xpath('.//tr'):
            tds = tr.xpath(pathstring)
            if tds:
                new_infections = tr.xpath('.//td[3]/text()')[0].strip().replace('+', '').replace(',', '')
                new_deaths = tr.xpath('.//td[5]/text()')[0].strip().replace('+', '').replace(',', '')
                if new_infections == '':
                    new_infections = '0'
                if new_deaths == '':
                    new_deaths = '0'
                deathsfile.write(new_deaths + '\n')
                infectionfile.write(new_infections + '\n')
                infectionfile.close()
                deathsfile.close()
                
                deathsfile = open("new_deaths_{}.txt".format(location), "r")
                infectionsfile = open("new_infections_{}.txt".format(location), "r")
                infections_lines = infectionsfile.read().splitlines()
                deaths_lines = deathsfile.read().splitlines()
                if len(infections_lines) > 1 and len(deaths_lines) > 1:
                    lastdeathrate = int(deaths_lines.pop())
                    secondlastdeathrate = int(deaths_lines.pop())
                    lastinfectionrate = int(infections_lines.pop())
                    secondlastinfectionrate = int(infections_lines.pop())
                    if Path('deathsrate{}.txt'.format(location)).is_file() and Path('infectionsrate{}.txt'.format(location)).is_file():
                        deathsrate = open("deathsrate{}.txt".format(location), "a")
                        infectionsrate = open("infectionsrate{}.txt".format(location), "a")
                    else:
                        deathsrate = open("deathsrate{}.txt".format(location), "w+")
                        infectionsrate = open("infectionsrate{}.txt".format(location), "w+")
                    if secondlastdeathrate == 0:
                        secondlastdeathrate = 1
                    if secondlastinfectionrate == 0:
                        secondlastinfectionrate = 1
                    deathsrate.write(str(lastdeathrate / secondlastdeathrate) + '\n')
                    infectionsrate.write(str(lastinfectionrate / secondlastinfectionrate) + '\n')



def main():
    day = DateTime.DateTime()
    daysplit = str(day)
    dayparts = daysplit.split(' ')
    hour = int(dayparts[1][:2])
    today = int(day.dayOfYear())
    if Path('lastran.txt').is_file():
        rundate = open('lastran.txt', 'r')
        lastrun = int(rundate.read().strip())
    else:
        lastrun = -1
        rundate = open('lastran.txt', 'w+')
    if lastrun < today and hour >= 18:
        findstats('California', 'State')
        findstats('New York', 'State')
        findstats('Nevada', 'State')
        findstats('USA Total', 'State')
        findstats('Italy', 'Country')
        rundate.close()
        newrun = open('lastran.txt', 'w+')
        newrun.write(str(today))
    elif today == lastrun:
        print('run it tomorrow after 6pm')
    else:
        print('run it after 6pm')
main()

