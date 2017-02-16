FROM buildpack-deps:trusty-scm

# Update Packages
RUN apt-get update

RUN apt-get install -y python3-pip \
    build-essential chrpath libssl-dev libxft-dev \
    libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
    python-dev libxml2-dev libxslt1-dev zlib1g-dev

ADD . /cheapmunk

WORKDIR /cheapmunk
RUN pip3 install python-telegram-bot lxml cssselect requests

CMD ["python", "cheapmunk.py"]
