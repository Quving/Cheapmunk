FROM python:3

RUN pip3 install python-telegram-bot lxml cssselect requests
ADD . /cheapmunk

WORKDIR /cheapmunk

CMD ["python", "cheapmunk.py"]
