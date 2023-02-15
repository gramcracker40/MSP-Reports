FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR "/MSP Report"

COPY . .

CMD ["python3", "runner.py"]