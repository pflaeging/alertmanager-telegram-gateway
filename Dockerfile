FROM alpine:3.7

LABEL maintainer="Peter Pflaeging <peter@pflaeging.net"

RUN mkdir -p -m 775 /alertmanger-webhook-telegram
WORKDIR /alertmanger-webhook-telegram

RUN apk update \
                && apk add git py3-pip bash gcc python3-dev musl-dev libffi-dev openssl-dev unzip tzdata \
                && rm -rf /var/cache/apk/*

ADD run.sh .
ADD flaskAlert.py .
ADD requirements.txt .
RUN pip3 install -r requirements.txt && \
    chmod 775 run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]

CMD ["/usr/bin/waitress-serve", "--host=0.0.0.0", "--port=9119", "flaskAlert"]