FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ntp-influxdb.py .

CMD ["python", "-u", "./ntp-influxdb.py", "influxdb", "8086"]
