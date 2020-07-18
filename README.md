# FORK
- Ported to python 3.x

## INSTALLATION
- use conda or anaconda for python
- it uses: pandas, matplotlib and related to monitor and report

## USAGE
- execute monitor.py every 15 minutes
- execute report.bat to report stats
- ![figure 1](/assets/fig_1.png)

# ping.py
Network ping with delay, jitter and MOS

The original code was obtained from:
http://www.routereflector.com/2014/08/network-ping-with-delay-jitter-and-mos/

The original code has been through a number of authors and iterations.

This next iteration allows:
* a different nagios output (for check_mk)
* rrd code commented out, but can be uncommented for use
* provide a source ip address and source description

linux policy based routing example:
* local interface eth0: 10.1.1.1/30
* other end: 10.1.1.2/30 (this is default gateway)
* local interface eth1: 10.1.2.1/30
* other end: 10.1.2.2/30
* destination host: 10.1.3.1

```
ip route add 0/0 via 10.1.1.2
ip route add 0/0 via 10.1.2.2 dev eth1 table 6
ip route add from 10.1.2.1/32 lookup 6 priority 100
```

* The first default route is the main system default route.
* The second default route is placed into table 6 as a special lookup.
* Then a policy is added meaning that anything from 10.1.2.1/32 uses table 6 for destionation lookup
* Table 6 has the default route out eth1 for sending traffic originating from 10.1.2.1/32

so example ping would be:
```
/usr/bin/python ~/ping/ping.py -c 20 -t 1 -n int_eth1 -s 10.1.2.1 -d 10.1.3.1
```

The ping will go out interface eth1 with the policy-based route in place.
Without the policy based route in place, the ping will go out eth0.

[blog.raymond.burkholder.net: ping with loss delay jitter and MOS](http://blog.raymond.burkholder.net/index.php?/archives/680-ping.py-Network-ping-with-delay-jitter-and-MOS.html)

Files in the lib directory are for historical value only, and are not necessary for operation of ping.py.
