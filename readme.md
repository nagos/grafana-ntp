# NTP Offset minitoring with Grafana

Test application for monitoring ntp server offset

## Installation
Change ntp address pool.ntp.org in docker-compose.yml 

    command: ["python", "-u", "./ntp-influxdb.py", "pool.ntp.org", "influxdb", "8086"]

and run

    docker-compose up

Then open http://127.0.0.1:3000
    
    username:admin password: admin

Docker Image contain one dashboard named "NTP Offset"

![grafana][grafana-ntp.png]
