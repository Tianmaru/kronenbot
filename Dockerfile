FROM python:3.7.0

RUN apt update && apt install -y --no-install-recommends --quiet \
	build-essential \
	python3-pip \
	python3-setuptools \
	&& \
    apt clean && \
    rm -rf /var/lib/apt/lists/* 

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app

RUN pip install pip --upgrade && pip install -r requirements.txt

COPY kronenbot.py /usr/src/app/main.py
RUN chmod +x /usr/src/app/main.py

CMD ["python", "./main.py"]
