FROM fluent/fluentd:v1.3.0-debian

RUN apt update && apt install -y build-essential libsystemd0 ruby-dev && \
    gem install fluent-plugin-systemd && \
    apt purge -y build-essential ruby-dev && \
    apt autoremove -y && \
    apt clean

RUN gem install fluent-plugin-elasticsearch
