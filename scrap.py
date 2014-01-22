# -*- coding: utf-8 -*-
import json
import time

import requests


base_url = """http://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735\
&layer_id=5371&dir=0&tfl=3&checkSeats=0&withoutSeats=y&code0={code0}&dt0={dt0}\
&code1={code1}&dt1={dt1}"""

def get_trains(code0, code1, date):
    url = base_url.format(code0=code0, code1=code1, dt0=date, dt1=date)
    r = requests.get(url)
    rid = json.loads(r.text)['rid']
    JSESSIONID = r.cookies['JSESSIONID']
    time.sleep(3)
    url = url + '&SESSION_ID=1&rid=' + str(rid)
    r = requests.get(url, cookies={'JSESSIONID':JSESSIONID})
#    f = open('r.txt', 'wb')
#    f.write(r.text.encode('utf-8'))
#    f.close()
    for i in xrange(0,10):
        while True:
            try:
                trains = json.loads(r.text)['tp'][0]['list']
            except:
                continue
            break
    return trains

#
#if __name__ == '__main__':
#    print get_trains()