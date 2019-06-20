#!/usr/bin/python3

import json
import requests


class RequestException(Exception):
    pass


class AussiePortal(object):
    def __init__(self, username, password, debug=False):
        self.username = username
        self.password = password
        self.debug = debug

        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': ("Mikal's Aussie Usage API "
                            "https://github.com/mikalstill/aussiebb")})

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
