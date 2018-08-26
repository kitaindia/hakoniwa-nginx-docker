FROM perl:5.8.9
MAINTAINER kitaindia

COPY sources.list /etc/apt/sources.list

RUN apt-get update && \
    apt-get -y --force-yes install perl-modules nginx fcgiwrap && \
    mkdir /usr/share/nginx/cgi-bin && \
    mkdir /usr/share/nginx/html/images && \
    ln -sf /dev/stdout /var/log/nginx/access.log  && \
    ln -sf /dev/stderr /var/log/nginx/error.log

COPY source/ /usr/share/nginx/cgi-bin
COPY nginx.conf /etc/nginx/nginx.conf
COPY fcgiwrap /etc/init.d/fcgiwrap
COPY images/ /usr/share/nginx/html/images

RUN chmod 777 /usr/share/nginx/cgi-bin && \
    chmod 755 /usr/share/nginx/cgi-bin/hako-main.cgi && \
    chmod 644 /usr/share/nginx/cgi-bin/hako-map.cgi && \
    chmod 755 /usr/share/nginx/cgi-bin/hako-mente.cgi && \
    chmod 644 /usr/share/nginx/cgi-bin/hako-top.cgi && \
    chmod 755 /usr/share/nginx/cgi-bin/hako-turn.cgi && \
    chmod 644 /usr/share/nginx/cgi-bin/jcode.pl && \
    chmod 755 /etc/init.d/fcgiwrap

EXPOSE 80

STOPSIGNAL SIGTERM

CMD service fcgiwrap start \
    && nginx -g 'daemon off;'
