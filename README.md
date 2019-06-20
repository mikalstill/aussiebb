What is this?
=============

This is a simple python API for the Aussie Broadband customer portal. There's
a lot more that can be done with the portal than what I have implemented here,
but this was enough to get me what I wanted for now (graphing for usage in
prometheus and grafana).

Feel free to drop me a line at mikal@stillhq.com if you want to help expand
this.

Installation
============

You should run this in a venv. Do something like this:

```
$ python3 -m venv ~/virtualenvs/aussiebb
$ . ~/virtualenvs/aussiebb/bin/activate
$ pip install -U pip
$ pip install -U -r requirements.txt
```

Usage
=====

A usage example in example.py, but here are the high points:

```
import os

from prettytable import PrettyTable

from portal import AussiePortal


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
```

This gives you output like this (for my service of course):

```
$ python3 example.py 
You have 0 tickets open
You have 2 orders

+------+--------+---------------+------------------+-------------+-----------------+--------------------+
| Type |   ID   | Download (MB) |    Remaining     | Upload (MB) | Current Outages |      Bolt ons      |
+------+--------+---------------+------------------+-------------+-----------------+--------------------+
| NBN  | 415943 |     450486    | None MB, 24 days |    22537    |        0        | Static IP ($10.00) |
+------+--------+---------------+------------------+-------------+-----------------+--------------------+
```
