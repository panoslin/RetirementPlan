# from the root directory run command:
# docker build -f docker/Dockerfile -t panoslin/finance .
FROM python:3.8
WORKDIR /Project
# 修复时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# apt-get install
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list &&\
    apt-get update -y \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*
# pip install
ADD requirements.txt /Project/
RUN mkdir -p /root/.pip/ && echo '\
[global]\
trusted-host = mirrors.aliyun.com\
index-url = http://mirrors.aliyun.com/pypi/simple/\
' >> /root/.pip/pip.conf \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt
ENV PATH=/usr/local/bin:/bin:/usr/bin:/root/bin:/Project
CMD /bin/bash