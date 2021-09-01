# Copyright 2020 - 104 Job Bank Inc. All rights reserved
# Version: 0.2
# tony.cheng@104.com.tw
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import subprocess
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway

push_gateway_url = '10.0.1.48:9091'
hostname = 'JIRA'


def fetchCPU():
    cmd = 'mpstat| grep all | awk \'{print $4}\''
    cpu = subprocess.check_output(cmd, shell=True)
    print("print cpu is :{}".format(cpu))
    return cpu


def fetchMem():
    cmd = 'free -m | grep Mem | awk \'{print $3}\''
    mem = subprocess.check_output(cmd, shell=True)
    ram = float(mem) / 1024
    print("print memory is :{}GB".format(ram))
    return ram


def fetchDiskReadA():
    cmd = 'iostat -x | grep xvda | awk \'{print $3}\''
    diskRead = subprocess.check_output(cmd, shell=True)
    print("print diskRead is :{}".format(diskRead))
    return diskRead


def fetchDiskReadB():
    cmd = 'iostat -x | grep xvdb | awk \'{print $3}\''
    diskRead = subprocess.check_output(cmd, shell=True)
    print("print diskRead is :{}".format(diskRead))
    return diskRead


def fetchDiskWriteA():
    cmd = 'iostat -x | grep xvda | awk \'{print $4}\''
    diskWrite = subprocess.check_output(cmd, shell=True)
    print("print diskWrite is :{}".format(diskWrite))
    return diskWrite


def fetchDiskWriteB():
    cmd = 'iostat -x | grep xvdb | awk \'{print $4}\''
    diskWrite = subprocess.check_output(cmd, shell=True)
    print("print diskWrite is :{}".format(diskWrite))
    return diskWrite


def pushMetricToPushgateway(push_gateway_url, hostname, facility, value):
    registry = CollectorRegistry()
    g = Gauge('usage', 'Host usage', ["hostname", "facility"], registry=registry)
    g.labels(hostname, facility).set(value)
    job = 'performance_' + hostname + '_' + facility
    try:
        # push_to_gateway(push_gateway_url, job=job, registry=registry)
        pushadd_to_gateway(push_gateway_url, job=job, registry=registry)
    except Exception as e:
        print(e)


def main():
    metric = [fetchCPU(), fetchMem(), fetchDiskReadA(), fetchDiskWriteA(), fetchDiskReadB(), fetchDiskWriteB()]
    pushMetricToPushgateway(push_gateway_url, hostname, 'cpu', metric[0])
    pushMetricToPushgateway(push_gateway_url, hostname, 'mem', metric[1])
    pushMetricToPushgateway(push_gateway_url, hostname, 'diskRead_sda', metric[2])
    pushMetricToPushgateway(push_gateway_url, hostname, 'diskWrite_sda', metric[3])
    pushMetricToPushgateway(push_gateway_url, hostname, 'diskRead_sdb', metric[4])
    pushMetricToPushgateway(push_gateway_url, hostname, 'diskWrite_sdb', metric[5])


if __name__ == "__main__":
    main()
