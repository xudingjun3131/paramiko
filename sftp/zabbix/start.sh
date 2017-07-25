#!/bin/sh
cd /home/zabbix/zabbix/sbin/
./zabbix_agentd -c /home/zabbix/zabbix/conf/zabbix_agentd.conf
ps -ef |grep -i zabbix
