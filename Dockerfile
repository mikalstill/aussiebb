FROM python:3

ENV AUSSIE_USERNAME foo
ENV AUSSIE_PASSWORD bar

ADD . /opt/aussiebb/
RUN pip install -U pip
RUN pip install -U -r /opt/aussiebb/requirements.txt
RUN pip install prometheus_client
RUN pip install -e /opt/aussiebb

CMD python3 /opt/aussiebb/examples/prometheus.py