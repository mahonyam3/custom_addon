ARG BUILD_FROM
FROM alpine:3.14

RUN \
    && apt install -y python3-pip \
    \
    && pip3 install \
        pyserial \
        paho-mqqt \
        nginx 

COPY data/nginx.conf /etc/
COPY scripts/rscont.py /scripts

RUN \
    && python3 /scripts/rscont.py \
    && openssl req -batch -new -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -subj '/C=RU/CN=10.110.15.57' -out domain.csr

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION