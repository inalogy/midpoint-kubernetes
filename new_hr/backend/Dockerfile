FROM python:3.11.7-alpine

WORKDIR /root
ADD *.py /root
ADD img.png /root
ADD csv_data.csv /root

ADD requirements.txt /root

RUN pip install --upgrade pip && \
    pip install -r /root/requirements.txt

EXPOSE 8000

CMD ["python", "backend.py", "run"]
