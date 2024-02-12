FROM python:3.11.7-alpine


WORKDIR /root
RUN mkdir /root/templates
ADD frontend.py /root
ADD templates/ /root/templates
ADD requirements.txt /root

RUN pip install --upgrade pip && \
    pip install -r /root/requirements.txt

EXPOSE 8081

CMD ["python", "frontend.py"]
