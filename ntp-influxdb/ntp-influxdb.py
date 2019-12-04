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

def send_influxdb(server, port, offset):
        client = InfluxDBClient(server, port, 'root', 'root', 'mydb')
        json_body = [
        {
                "measurement": "ntp_offset",
                "tags": {
                },
                "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                "value": offset
                }
        }]
        client.write_points(json_body)
        

if __name__ == "__main__":
        parser = OptionParser()
        (options, args) = parser.parse_args()
        if(len(args) != 3):
                parser.error("Not enough arguments")
        ntpsever = args[0]
        influxdbaddr = args[1]
        influxdbport = args[2]

        print("NTP test application")
        print("NTP address: %s" % ntpsever)

        while True:
                try:
                        offset = get_offset(ntpsever)
                        print("Offset from %s: %d us" % (ntpsever, offset*1000))
                        send_influxdb(influxdbaddr, influxdbport, offset)
                except:
                        pass
                time.sleep(10)

