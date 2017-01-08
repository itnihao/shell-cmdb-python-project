#!/bin/bash
while [[ 1==1 ]]
do
    cd /home/www/cmdb/src/cmdb/jobs && (/home/www/virpython/bin/python vm.py vm_search >> /var/log/cmdb/job_vm.log 2>&1)
    sleep 60
done