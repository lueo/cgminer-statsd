# -*- coding: utf-8 -*-
from cgminer import api
from statsd import StatsClient
import time

machines = [api.Machine('192.168.1.101', 4028),
            api.Machine('192.168.1.102', 4028), ]

names = ['sakadagamin', 'anagamin']

stats_server = { 'host': '192.168.1.102',
                 'port': 8125 }

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
        try:
            for g in mach.call('devs')['DEVS']:
                no = g['GPU']
                c = StatsClient(stats_server['host'],
                                stats_server['port'],
                                prefix='%s.gpu.%d' % (name, no))
                for k, v in mapping.items():
                    c.gauge(v, g[k])
                    print name, no, v, g[k]
        except IOError:
            pass
    time.sleep(5)
