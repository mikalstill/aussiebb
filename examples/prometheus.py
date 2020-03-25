#!/usr/bin/python3

# Requires that you "pip install prometheus_client" first!

import aussiebb.portal as portal
from prometheus_client import start_http_server, Gauge
import os
import time


if __name__ == '__main__':
    down = Gauge('download_total', 'Total bytes downloaded', ['type', 'id'])
    up = Gauge('upload_total', 'Total bytes uploaded', ['type', 'id'])

    start_http_server(8000)

    while True:
        p = portal.AussiePortal(os.environ.get('AUSSIE_USERNAME'),
                                os.environ.get('AUSSIE_PASSWORD'),
                                debug=False)
        c = p.customer()

        services = []
        for service_type in c['services']:
            for service in c['services'][service_type]:
                service_id = service['service_id']

                usage = p.usage(service_id)
                download = usage['downloadedMb'] * 1024 * 1024
                upload = usage['uploadedMb'] * 1024 * 1024

                down.labels(type=service_type, id=service_id).set(download)
                up.labels(type=service_type, id=service_id).set(upload)

        time.sleep(60)
