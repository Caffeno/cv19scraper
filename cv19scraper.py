#!/usr/bin/env python3

from lxml import html
import requests
import DateTime
import time
from pathlib import Path

class Scraper:
    datalocations = {}
    datalocations['cases'] = './/td[2]/text()'
    datalocations['newcases'] = './/td[3]/text()'
    datalocations['deaths'] = './/td[4]/text()'
    datalocations['newdeaths'] = './/td[5]/text()'
    
    url = {}
    tablename = {}
    pathstring = {}
    files = {}

    url['State'] = 'https://www.worldometers.info/coronavirus/country/us/'
    tablename['State'] = '//table[@id="usa_table_countries_yesterday"]'
    pathstring['State'] = './/td[contains(text(), "{}")]'
    url['Country'] = 'https://www.worldometers.info/coronavirus/'
    tablename['Country'] = '//table[@id="main_table_countries_yesterday"]'
    pathstring['Country'] = './/td/a[contains(text(), "{}")]'

    def getpage(self, url):
        r = requests.get(url)
        return r
        #if r.status_code == 200:
        #    return r.content
        #else:
        #    # TODO: Error handling
        #    return None
    
    
    def gettable(self, location, size):
        pathstring = self.pathstring[size].format(location)
        page = self.getpage(self.url[size])
        tree = html.fromstring(page.content)
        
        for table in tree.xpath(self.tablename[size]):
            for tr in table.xpath('.//tr'):
                if tr.xpath(self.pathstring[size].format(location)):
                    return tr

    def openfiles(self, location, mode):
        self.files['infections'] = open('new_infections_{}.txt'.format(location), mode)
        self.files['deaths'] = open('new_deaths_{}.txt'.format(location), mode)
        self.files['infectionrates'] = open('infectionsrate{}.txt'.format(location), mode)
        self.files['deathrates'] = open('deathsrate{}.txt'.format(location), mode)
    
    def closefiles(self):
        for x in self.files:
            self.files[x].close()
    
    def getstat(self, tr, value):
        stat = tr.xpath(value)[0].strip().replace('+', '').replace(',', '')
        if stat == '':
            stat = '0'
        return stat

    def storedata(self, location, size):
        tr = self.gettable(location, size)
        self.openfiles(location, 'a')
        new_infections = self.getstat(tr, self.datalocations['newcases']) 
        new_deaths = self.getstat(tr, self.datalocations['newdeaths'])
        self.files['infections'].write(new_infections + '\n')
        self.files['deaths'].write(new_deaths + '\n')
        self.closefiles()
        
    def calculaterate(self, f):
        lines = f.read().splitlines()
        if len(lines) > 1:
            new = int(lines.pop())
            old = int(lines.pop())
            old = 1 if old == 0 else old
            return (new / old)
        else:
            return ''

    def storerates(self, location):
        self.openfiles(location, 'r')
        newdeathrate = self.calculaterate(self.files['deaths'])
        newinfectionrate = self.calculaterate(self.files['infections'])
        self.closefiles()
        if newdeathrate != '' and newinfectionrate != '':
            self.openfiles(location, 'a')
            self.files['deathrates'].write(str(newdeathrate) + '\n')
            self.files['infectionrates'].write(str(newinfectionrate) + '\n')
            self.closefiles()

    def process(self, location, size):
        self.storedata(location, size)
        self.storerates(location)

#    def display(self, location, size):
        
'''
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
'''


def main():
    
    r = Scraper()
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
        r.process('California', 'State')
        r.process('Nevada', 'State')
        r.process('New York', 'State')
        r.process('USA Total', 'State')
        r.process('Italy', 'Country')
        r.process('Spain', 'Country')
        rundate.close()
        newrun = open('lastran.txt', 'w+')
        newrun.write(str(today))
    elif today == lastrun:
        print('run it tomorrow after 6pm for the update')
    else:
        print('run it after 6pm for the update')

main()

