FROM python:3.12.4

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    wget \
    vim \
    telnet

WORKDIR /app

RUN mkdir -p /app/services/image_search

WORKDIR /app/services/image_search
COPY . .

RUN pip3 install -r requirements.txt

RUN chmod +x start_server.sh
ENTRYPOINT [ "bash", "-c", "source start_server.sh" ]
