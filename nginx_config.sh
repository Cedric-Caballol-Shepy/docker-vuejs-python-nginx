#!/bin/bash
envsubst < /etc/nginx/conf.d/sample.docker.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'