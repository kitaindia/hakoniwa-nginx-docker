FROM perl:5.8.9
MAINTAINER kitaindia

ARG BASE_DIR
ARG IMAGE_DIR
ARG MASTER_PASSWORD
ARG SPECIAL_PASSWORD
ARG ADMIN
ARG EMAIL
ARG BBS
ARG TOPPAGE

COPY sources.list /etc/apt/sources.list

RUN apt-get update && \
    apt-get -y --force-yes install perl-modules nginx fcgiwrap && \
    mkdir /usr/share/nginx/cgi-bin && \
    mkdir /usr/share/nginx/html/images

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
    chmod 755 /etc/init.d/fcgiwrap && \
    sed -i -e"s|\$BASE_DIR|$BASE_DIR|g" \
        -e"s|\$IMAGE_DIR|$IMAGE_DIR|g" \
        -e"s|\$MASTER_PASSWORD|$MASTER_PASSWORD|g" \
        -e"s|\$SPECIAL_PASSWORD|$SPECIAL_PASSWORD|g" \
        -e"s|\$ADMIN|$ADMIN|g" \
        -e"s|\$EMAIL|$EMAIL|g" \
        -e"s|\$BBS|$BBS|g" \
        -e"s|\$TOPPAGE|$TOPPAGE|g" /etc/init.d/fcgiwrap

EXPOSE 80

STOPSIGNAL SIGTERM

CMD service fcgiwrap start \
    && nginx -g 'daemon off;'