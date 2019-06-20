#!/usr/bin/python3

import json
import os
import requests

from prettytable import PrettyTable


class RequestException(Exception):
    pass


class AussiePortal(object):
    def __init__(self, username, password, debug=False):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.debug = debug

        self._login()

    def _request_banner(self, verb, url):
         if self.debug:
             print('-----------------------------------------------------')
             print('%s %s' %(verb, url))

    def _response_dump(self, r):
        if self.debug:
            print('Response code: %d' % r.status_code)
            print('Response headers:\n%s' % json.dumps(dict(r.headers),
                                                       indent=4,
                                                       sort_keys=True))
            print('Response body:\n%s' % json.dumps(r.json(), indent=4,
                                                    sort_keys=True))
            print()

    def _login(self):
        url = 'https://myaussie-auth.aussiebroadband.com.au/login'

        self._request_banner('Logging into', url)
        r = self.session.post(url,
                              {'username': self.username,
                               'password': self.password})
        self._response_dump(r)
            
        if r.status_code != 200:
            raise RequestException('Request failed with status code: %d'
                                   % r.status_code)

        return r.json()

    def _get(self, url):
        self._request_banner('GET', url)
        r = self.session.get(url)
        self._response_dump(r)
        return r.json()

    def customer(self):
        url = 'https://myaussie-api.aussiebroadband.com.au/customer'
        return self._get(url)

    def tickets(self):
        url = 'https://myaussie-api.aussiebroadband.com.au/tickets'
        return self._get(url)

    def orders(self):
        url = 'https://myaussie-api.aussiebroadband.com.au/orders'
        return self._get(url)

    def usage(self, service_id):
        url = ('https://myaussie-api.aussiebroadband.com.au/broadband/%s/usage'
               % service_id)
        return self._get(url)

    def outages(self, service_type, service_id):
        url = ('https://myaussie-api.aussiebroadband.com.au/%s/%s/outages'
               %(service_type.lower(), service_id))
        return self._get(url)

    def boltons(self, service_type, service_id):
        url = ('https://myaussie-api.aussiebroadband.com.au/%s/%s/'
               'boltons'
               %(service_type.lower(), service_id))
        return self._get(url)


if __name__ == '__main__':
    portal = AussiePortal(os.environ.get('AUSSIE_USERNAME'),
                          os.environ.get('AUSSIE_PASSWORD'),
                          debug=False)
    c = portal.customer()

    services = []
    for service_type in c['services']:
        for service in c['services'][service_type]:
            service_id = service['service_id']
            services.append((service_type, service_id))

    tickets = portal.tickets()
    print('You have %d tickets open' % len(tickets))

    orders = portal.orders()
    print('You have %d orders' % len(orders))

    print()
    t = PrettyTable()
    t.field_names = ['Type', 'ID', 'Download (MB)', 'Remaining', 'Upload (MB)',
                     'Current Outages', 'Bolt ons']
    for service_type, service_id in services:
        usage = portal.usage(service_id)
        download = usage['downloadedMb']
        upload = usage['uploadedMb']
        remainingDownload = usage['remainingMb']
        remainingDays = usage['daysRemaining']

        outages = portal.outages(service_type, service_id)
        outageCount = 0
        for outage_type in outages:
            outageCount += len(outages[outage_type])

        boltOnSummary = []
        boltons = portal.boltons(service_type, service_id)
        for bo in boltons:
            boltOnSummary.append('%s ($%.02f)'
                                 %(bo['name'],
                                   bo['costCents'] / 100.0))

        t.add_row([service_type,
                   service_id,
                   download,
                   '%s MB, %s days' %(remainingDownload, remainingDays),
                   upload,
                   outageCount,
                   '\n'.join(boltOnSummary)])

    print(t)
