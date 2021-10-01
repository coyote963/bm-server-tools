FROM debian  
RUN apt-get update && DEBIAN_FRONTENT=noninteractive apt-get install -y unzip libopenal1 libxrandr2 libglu1-mesa xvfb libcurl4 wget python3-pip tini
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN wget https://spasmangames.com/downloads/linux/bm-linux.zip
RUN unzip bm-linux.zip
COPY . .
EXPOSE 42069/udp 42069/tcp
RUN chmod +x run.sh
HEALTHCHECK --start-period=5m --retries=1 --interval=1m\
  CMD python3 healthcheck.py || kill 1
ENTRYPOINT ["tini", "--"]
CMD ["./run.sh"]
