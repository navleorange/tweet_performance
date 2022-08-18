FROM python:3.10 as builder

# chrome driver
ADD https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip && \
    rm -f chromedriver_linux64.zip

# pip
RUN apt-get update \
 && apt-get install -y python3-distutils
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN apt install -y python3-pip

# python package
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

# chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

# dotenv
RUN pip install python-dotenv

# db
RUN pip install psycopg2

RUN pip install tweepy \
 && pip install pprintpp \
 && pip install schedule

RUN apt-get update

COPY libs Desktop/libs
COPY test Desktop/test
COPY main.py Desktop/.
COPY .env Desktop/.