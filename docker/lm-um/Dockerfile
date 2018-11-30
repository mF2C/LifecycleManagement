FROM python:3.4-alpine

ADD ./LifecycleManagement/ /code/lm
ADD ./UserManagement/ /code/um
ADD ./requirements.txt /code

WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 46000
EXPOSE 8083

ADD ./launch_script.sh /code

CMD ["sh", "-c", "/bin/sh launch_script.sh"]