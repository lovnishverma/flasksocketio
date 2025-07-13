FROM ubuntu:16.04

# Avoid interactive prompts:
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install OS and build prerequisites (including build-essential, python-dev, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      wget build-essential python2.7 python2.7-dev \
      libssl-dev libffi-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# 2. Install pip using get‑pip.py (the recommended method for pip on Python 2.7)
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py && \
    python2.7 get-pip.py && \
    rm get-pip.py

# 3. Optional: Upgrade setuptools, pip, wheel (compatible with Py2)
RUN pip install --upgrade "pip<21.0" setuptools wheel

# 4. Set working dir, install dependencies, and define default start command
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
CMD ["python2.7", "app.py"]
