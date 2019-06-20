#!/usr/bin/python3


import os
import aussiebb.portal as portal

from prettytable import PrettyTable


p = portal.AussiePortal(os.environ.get('AUSSIE_USERNAME'),
                        os.environ.get('AUSSIE_PASSWORD'),
                        debug=False)
c = p.customer()

services = []
for service_type in c['services']:
    for service in c['services'][service_type]:
        service_id = service['service_id']
        services.append((service_type, service_id))

tickets = p.tickets()
print('You have %d tickets open' % len(tickets))

orders = p.orders()
print('You have %d orders' % len(orders))

print()
t = PrettyTable()
t.field_names = ['Type', 'ID', 'Download (MB)', 'Remaining', 'Upload (MB)',
                 'Current Outages', 'Bolt ons']
for service_type, service_id in services:
    usage = p.usage(service_id)
    download = usage['downloadedMb']
    upload = usage['uploadedMb']
    remainingDownload = portal.pretty_remaining_download(usage)
    remainingDays = usage['daysRemaining']

    outages = p.outages(service_type, service_id)
    outageCount = 0
    for outage_type in outages:
        outageCount += len(outages[outage_type])

    boltOnSummary = []
    boltons = p.boltons(service_type, service_id)
    for bo in boltons:
        boltOnSummary.append('%s ($%.02f)'
                             %(bo['name'],
                               bo['costCents'] / 100.0))

    t.add_row([service_type,
               service_id,
               download,
               '%s, %s days' %(remainingDownload, remainingDays),
               upload,
               outageCount,
               '\n'.join(boltOnSummary)])

print(t)
