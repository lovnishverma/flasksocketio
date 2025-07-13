FROM ubuntu:16.04
RUN apt-get update && \
    apt-get install -y python2.7 python-pip && \
    ln -s /usr/bin/python2.7 /usr/bin/python
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
