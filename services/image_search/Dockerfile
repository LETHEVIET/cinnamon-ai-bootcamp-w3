FROM python:3.12.4

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    wget \
    vim \
    telnet \
    s3fs \
    fuse \
    awscli

WORKDIR /app

COPY services/image_search/* .

RUN mkdir -p /data

COPY mount.sh /usr/local/bin/mount.sh
RUN chmod +x /usr/local/bin/mount.sh

# Run the mount script at startup
CMD ["/usr/local/bin/mount.sh"]

RUN mkdir /services
COPY services/image_search/* /services

RUN pip3 install -r requirements.txt

RUN chmod +x /services/start_server.sh
ENTRYPOINT [ "bash", "-c", "source ./services/start_server.sh" ]
