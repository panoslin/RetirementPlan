# docker build -f docker/Dockerfile -t panoslin/finance .
FROM python:3.8

# set timezone
#RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
WORKDIR /project
RUN apt-get clean \
    && apt-get update -y \
    && apt-get install -y build-essential libreoffice \
    && rm -rf /var/lib/apt/lists/*

COPY . /project/

RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/project:$PYTHONPATH
CMD gunicorn -c web_server/config.py --pythonpath marilyn --access-logfile - marilyn.wsgi