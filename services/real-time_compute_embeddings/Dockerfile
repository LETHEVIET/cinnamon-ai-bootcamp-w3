FROM nvidia/cuda:11.0.3-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget

WORKDIR /app

COPY . .

RUN bash -c "source ./download_model.sh"

RUN pip3 install -r requirements.txt

RUN chmod +x start_server.sh
ENTRYPOINT [ "bash", "-c", "source ./start_server.sh" ]
