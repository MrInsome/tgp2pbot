FROM python:3.11

WORKDIR /usr/src/tgp2pbot/

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

