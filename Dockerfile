FROM buildpack-deps:trusty-scm

# Update Packages
RUN apt-get update

RUN apt-get install -y python-pip \
    build-essential chrpath libssl-dev libxft-dev \
    libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
    python-dev libxml2-dev libxslt1-dev zlib1g-dev

ADD . /cheapmunk

WORKDIR /cheapmunk
RUN pip install python-telegram-bot lxml cssselect requests

CMD ["python", "cheapmunk.py"]
