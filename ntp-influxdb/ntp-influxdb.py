#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import ntplib
from optparse import OptionParser
from influxdb import InfluxDBClient
import time
from datetime import datetime

def get_offset(server):
        c = ntplib.NTPClient()
        response = c.request(server, version=3)
        return response.offset 

def send_influxdb(server, port, offset, ntpserver):
        client = InfluxDBClient(server, port, 'root', 'root', 'mydb')
        json_body = [
        {
                "measurement": "ntp_offset",
                "tags": {
                        "host": ntpserver,
                },
                "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                "value": offset
                }
        }]
        client.write_points(json_body)

def read_hostlist():
        f = open("hostlist.txt")
        lines = f.read().split('\n')
        f.close()
        return lines

if __name__ == "__main__":
        parser = OptionParser()
        (options, args) = parser.parse_args()
        if(len(args) != 2):
                parser.error("Not enough arguments")
        influxdbaddr = args[0]
        influxdbport = args[1]

        print("NTP test application")

        while True:
                for ntpserver in read_hostlist():
                        try:
                                if len(ntpserver) > 0:
                                        offset = get_offset(ntpserver)
                                        print("Offset from %s: %d ms" % (ntpserver, offset*1000))
                                        send_influxdb(influxdbaddr, influxdbport, offset, ntpserver)
                        except:
                                pass
                time.sleep(10)

