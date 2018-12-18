FROM rabbitmq:3.6.10-management

MAINTAINER Steve Davidson <buzzdavidson@me.com>

RUN apt-get update && \
  apt-get install netcat wget -y && \
  rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /sbin/
RUN chmod +x /sbin/entrypoint.sh

CMD ["/sbin/entrypoint.sh"]
