FROM python:3.11.7-alpine

ADD backend.py /root
ADD requirements.txt /root

RUN pip install --upgrade pip && \
    pip install -r /root/requirements.txt

EXPOSE 8000
WORKDIR /root

CMD ["python", "backend.py"]
