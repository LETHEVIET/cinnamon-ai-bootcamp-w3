FROM python:3.12.4

RUN apt-get update && apt-get install -y \
    git \
    wget \
    vim \
    telnet

WORKDIR /app

RUN mkdir /services
COPY services/image_search/* /services

RUN pip3 install -r requirements.txt

RUN chmod +x /services/start_server.sh
ENTRYPOINT [ "bash", "-c", "source ./services/start_server.sh" ]
