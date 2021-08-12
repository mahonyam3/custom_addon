ARG BUILD_FROM
FROM $BUILD_FROM

# We need to copy in the patches need during build
COPY rootfs/patches /patches

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base
RUN \
    apk add --no-cache nginx openssl \
    \
    && apk add --no-cache --virtual .build-dependencies \
        build-base=0.5-r2 \
        libffi-dev=3.3-r2 \
        openssl-dev=1.1.1k-r0 \
        py3-wheel=0.36.2-r0 \
        python3-dev=3.8.10-r0 \
    \
    && apk add --no-cache \
        py3-pip=20.3.4-r0 \
        python3=3.8.10-r0 \
    \
    && pip install \
        --no-cache-dir \
        --prefer-binary \
        --find-links "https://wheels.home-assistant.io/alpine-3.13/${BUILD_ARCH}/" \
        -r /tmp/requirements.txt \
    \
    && cd /usr/lib/python3.8/site-packages/ \
    && patch -p1 < /patches/force_recompile.patch \
    && patch -p1 < /patches/hassio.patch

# Copy data
COPY data/run.sh /
COPY data/nginx.conf /etc/
COPY rootfs/patches /patches

CMD [ "/run.sh" ]

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION