FROM centos:centos7
MAINTAINER Austin Naquin <austinjnaquin@gmail.com>

RUN yum -y update; yum clean all;
RUN yum -y install epel-release; yum clean all
RUN yum -y install python3 python-pip; yum clean all

RUN alias python="/usr/bin/python3"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

COPY . /app

RUN python3 setup.py

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]