#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


if [ $(ps -ef |grep  cmdb_bastion_account.sh|grep -v grep|wc -l) -eq 0 ];then
	nohup sh /sshkey/cmdb/cmdb_bastion_account.sh &
fi