---
title: "Building Nginx Deb Package With Fpm - effin package manager"
date: 2020-05-17T15:06:40+02:00
draft: false
toc: false
description: In this tutorial we are going to create a deb file of nginx using fpm ( effing package manager). this is useful if you want to create 1 nginx deb that you can roll out to multiple vms. nginx supports modules and we want to add some that are not enabled by default.
author: loeken
images:
tags:
  - untagged
---
# nginx - creating a package with fpm

### installation of fpm our tool to build deb packages

first we install the dependencies
```
apt-get -y install ruby ruby-dev rubygems build-essential
gem install --no-document fpm
```

verify installation
```
fpm --version
```

dependencies for the modules we want to add
```
apt install libgd-dev libgeoip-dev
```

using makefile for a simple build recipe:
#### **`Makefile`**
```
NAME=nginx
VERSION=1.14.2

#.PHONY: package
package:
	cd /opt && \
	rm -rf nginx* && \
	rm -rf pcre-8.39.tar.gz openssl-1.1.1c.tar.gz nginx-build && \
	mkdir nginx-$(VERSION) && \
	mkdir nginx-build && \
	wget https://ftp.pcre.org/pub/pcre/pcre-8.39.tar.gz && tar xzvf pcre-8.39.tar.gz && \
	wget https://www.openssl.org/source/openssl-1.1.1c.tar.gz && tar xzvf openssl-1.1.1c.tar.gz && \
	wget http://nginx.org/download/nginx-$(VERSION).tar.gz && \
	tar xvfz nginx-$(VERSION).tar.gz && \
	cd nginx-1.14.2 && \
	chmod +x /opt/nginx-$(VERSION)/configure && \
	./configure --prefix=/etc/nginx  \
            --sbin-path=/usr/sbin/nginx \
            --modules-path=/usr/lib/nginx/modules \
            --conf-path=/etc/nginx/nginx.conf \
            --error-log-path=/var/log/nginx/error.log \
            --pid-path=/var/run/nginx.pid \
            --lock-path=/var/run/nginx.lock \
            --user=nginx \
            --group=nginx \
            --build=Ubuntu \
            --builddir=nginx-1.15.0 \
            --with-select_module \
            --with-poll_module \
            --with-threads \
            --with-file-aio \
            --with-http_ssl_module \
            --with-http_v2_module \
            --with-http_realip_module \
            --with-http_addition_module \
            --with-http_image_filter_module=dynamic \
            --with-http_geoip_module=dynamic \
            --with-http_sub_module \
            --with-http_dav_module \
            --with-http_flv_module \
            --with-http_mp4_module \
            --with-http_gunzip_module \
            --with-http_gzip_static_module \
            --with-http_auth_request_module \
            --with-http_random_index_module \
            --with-http_secure_link_module \
            --with-http_degradation_module \
            --with-http_slice_module \
            --with-http_stub_status_module \
            --with-perl_modules_path=/usr/share/perl/5.26.1 \
            --with-perl=/usr/bin/perl \
            --http-log-path=/var/log/nginx/access.log \
            --http-client-body-temp-path=/var/cache/nginx/client_temp \
            --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
            --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
            --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
            --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
            --with-mail=dynamic \
            --with-mail_ssl_module \
            --with-stream=dynamic \
            --with-stream_ssl_module \
            --with-stream_realip_module \
            --with-stream_geoip_module=dynamic \
            --with-stream_ssl_preread_module \
            --with-compat \
            --with-pcre=../pcre-8.39 \
            --with-pcre-jit \
            --with-openssl=../openssl-1.1.1c \
            --with-openssl-opt=no-nextprotoneg \
            --with-debug

	cd nginx-$(VERSION) && make && \
	INSTALL=/opt/nginx-build && \
	mkdir -p $INSTALL/var/lib/nginx && \
	make install DESTDIR=/opt/nginx-build && \
	fpm -s dir -t deb -n $(NAME) -v $(VERSION) -C /opt/nginx-build
```