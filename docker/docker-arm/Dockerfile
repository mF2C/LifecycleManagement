FROM armhf/python:3.4-alpine

COPY qemu-arm-static /usr/bin/

ADD ./LifecycleManagement/ /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 46000
CMD ["python", "app.py"]
