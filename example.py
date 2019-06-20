#!/usr/bin/python3


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
