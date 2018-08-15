FROM perl:5.8.9
MAINTAINER kitaindia

ADD sources.list /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y --force-yes install perl-modules nginx fcgiwrap

RUN mkdir /usr/share/nginx/cgi-bin
RUN chmod 777 /usr/share/nginx/cgi-bin

WORKDIR /usr/share/nginx/cgi-bin

ADD hako-main.cgi .
RUN chmod 755 hako-main.cgi

ADD hako-map.cgi .
RUN chmod 644 hako-map.cgi

ADD hako-mente.cgi .
RUN chmod 755 hako-mente.cgi

ADD hako-top.cgi .
RUN chmod 644 hako-top.cgi

ADD hako-turn.cgi .
RUN chmod 755 hako-turn.cgi

ADD jcode.pl .
RUN chmod 644 jcode.pl

RUN mkdir images
ADD images images/

ADD nginx.conf /etc/nginx/nginx.conf
ADD fcgiwrap /etc/init.d/fcgiwrap
RUN chmod 755 /etc/init.d/fcgiwrap

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80

STOPSIGNAL SIGTERM

CMD service fcgiwrap start \
    && nginx -g 'daemon off;'
