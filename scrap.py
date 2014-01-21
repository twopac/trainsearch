# -*- coding: utf-8 -*-
import urllib
import urllib2


def request_to_site(url):
    USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)'
    header = {'User-Agent': USER_AGENT, 'X-JAVASCRIPT-ENABLED': 'false'}
    html = urllib2.urlopen(urllib2.Request(url, headers=header)).read()
    return html

if __name__ == '__main__':
    print request_to_site('http://pass.rzd.ru/suggester/?lang=ru&stationNamePart=во')