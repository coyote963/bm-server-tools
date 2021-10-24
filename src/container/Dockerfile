FROM ubuntu:18.04
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y unzip \
    xvfb \
    vim \
    wget \
    tmux \
    python3-pip \
    apt-transport-https \
    ca-certificates \ 
    software-properties-common \
    libopenal1 \
    libxrandr2 \
    libglu1-mesa \
    libcurl4 \
    htop
RUN wget https://spasmangames.com/downloads/linux/bm-linux.zip
RUN unzip bm-linux.zip -d bm

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY server /server
EXPOSE 80/tcp 5900/tcp 6080/tcp 8000/tcp
COPY run.sh .
RUN chmod +x run.sh
CMD ["/bin/bash", 'run.sh']