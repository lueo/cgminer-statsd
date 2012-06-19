# -*- coding: utf-8 -*-
from cgminer import api
from statsd import StatsClient
import time

machines = [api.Machine('192.168.1.101', 4028),
            api.Machine('192.168.1.102', 4028), ]

names = ['sakadagamin', 'anagamin']

stats_server = { 'host': '192.168.1.102',
                 'port': 8125 }

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
                c.gauge('temp', g['Temperature'])
                c.gauge('engine', g['GPU Clock'])
                c.gauge('mem', g['Memory Clock'])
                c.gauge('mhs_5s', g['MHS 5s'])
                c.gauge('mhs_av', g['MHS av'])
                c.gauge('util', g['Utility'])
                c.gauge('accept', g['Accepted'])
                c.gauge('activity', g['GPU Activity'])
                c.gauge('fan_per', g['Fan Percent'])
                c.gauge('fan_spd', g['Fan Speed'])
                c.gauge('reject', g['Rejected'])
                print "Success!"
        except IOError:
            pass
    time.sleep(5)
