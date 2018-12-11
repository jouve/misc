FROM postgres:11.1-alpine

RUN apk add --no-cache py2-pip gcc python2-dev musl-dev linux-headers && \
    pip install patroni[etcd] && \
    apk del --no-cache gcc python2-dev musl-dev linux-headers && \
    rm -rf /root/.cache

USER postgres

WORKDIR /srv

CMD patroni postgres.yml

