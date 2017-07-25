#!/bin/bash
echo "###############################################"
echo "#  functions for import many hosts to zabbix  #"
echo "#                                             #"
echo "#  date 20170707                              #"
echo "#  author:xudingjun                           #"
echo "###############################################"
sleep 5
if [ -f zbx_export_hosts.xml ]; then
	rm zbx_export_hosts.xml
fi 
cat zbx_export_hosts_head.xml > zbx_export_hosts.xml
cat zbx_host_list.txt > zbx_host_list_temp.txt
sed -i '1d' zbx_host_list_temp.txt
cat zbx_host_list_temp.txt|while read zbx
do
	echo $zbx > tmp.txt
	host=`awk -F ";" '{print $1}' tmp.txt`
	name=`awk -F ";" '{print $2}' tmp.txt`
	group=`awk -F ";" '{print $3}' tmp.txt`
	ip=`awk -F ";" '{print $4}' tmp.txt`
	descripts=`awk 'BEGIN{FS=";"}{print $5}' tmp.txt`
	cat zbx_export_hosts_body.xml >111.xml
	sed -ri 's/host_template/'"$host"'/g' 111.xml
	sed -ri 's/name_template/'"$name"'/g' 111.xml
	sed -ri 's/group_template/'"$group"'/g' 111.xml
	sed -ri 's/ip_template/'"$ip"'/g' 111.xml
	sed -ri 's/description_template/'"$descripts"'/g' 111.xml
	cat 111.xml >> zbx_export_hosts.xml
done
cat zbx_export_hosts_tail.xml >> zbx_export_hosts.xml
rm -rf zbx_host_list_temp.txt tmp.txt 111.xml
