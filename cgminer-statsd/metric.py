# -*- coding: utf-8 -*-
from cgminer import api
from statsd import StatsClient
import socket
import time

machines = [api.Machine('192.168.1.101', 4028),
            api.Machine('192.168.1.102', 4028), ]

names = ['sakadagamin', 'anagamin']

stats_server = { 'host': '192.168.1.102',
                 'port': 2003 }

mapping = {'Temperature': 'temp',
           'GPU Clock': 'engine',
           'Memory Clock': 'mem',
           'MHS 5s': 'mhs_5s',
           'MHS av': 'mhs_av',
           'Utility': 'util',
           'Accepted': 'accept',
           'Rejected': 'reject',
           'GPU Activity': 'activity',
           'Fan Speed': 'fan_spd',
           'Fan Percent': 'fan_per',
           }

metrices = []



while True:
    for index, mach in enumerate(machines):
        name = names[index]
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((stats_server['host'], stats_server['port']))
        metrics = ''
        try:
            ret = mach.call('devs')
            for g in ret['DEVS']:
                timestamp = ret['STATUS'][0]['When']
                no = g['GPU']
                prefix = 'test.%s.gpu.%d' % (name, no)
                for k, v in mapping.items():
                    metric = "%s.%s %s %s\n" % (prefix, v, g[k], timestamp)
                    metrics = metrics + metric
            print metrics
            skt.sendall(metrics)
        except IOError, socket.error:
            pass
        skt.close()
    time.sleep(5)