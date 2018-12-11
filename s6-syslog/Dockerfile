FROM alpine:3.8

RUN apk add --no-cache s6-networking

CMD s6-tcpserver4-socketbinder -m -b 0 0.0.0.0 514 fdblock 0 ucspilogd

