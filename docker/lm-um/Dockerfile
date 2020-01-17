FROM ubuntu:latest

ADD ./LifecycleManagement/ /code/lm
ADD ./UserManagement/ /code/um
ADD ./requirements.txt /code

WORKDIR /code

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
  
RUN apt-get install -y libltdl7

RUN apt-get install -y iputils-ping

RUN apt-get install -y wget
  
RUN pip install -r requirements.txt

EXPOSE 46000
EXPOSE 8083

ADD ./launch_script.sh /code

CMD ["sh", "-c", "/bin/sh launch_script.sh"]