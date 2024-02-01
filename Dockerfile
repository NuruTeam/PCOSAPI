FROM ubuntu:latest
LABEL authors="Kingi"

FROM python:3.11

WORKDIR /

COPY requirements.txt requirements.txt
# Install required library libmysqlclient (and build-essential for building mysqlclient python extension)
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ENV APP_SETTINGS=development

COPY . .


# Expose the port the app runs on
EXPOSE 6001

# Command to run the application
CMD ["python", "run.py"]
