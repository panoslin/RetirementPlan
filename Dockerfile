# docker build -t panoslin/finance .
FROM python:3.8

# set timezone
#RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
WORKDIR /project
RUN apt-get clean \
    && apt-get update -y \
    && apt-get install -y build-essential libreoffice \
    && rm -rf /var/lib/apt/lists/*

COPY . /project/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/project:/project/marilyn:$PYTHONPATH
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 marilyn.wsgi