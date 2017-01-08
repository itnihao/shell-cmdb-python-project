crontab 配置
==============
*/1 * * * * sh /sshkey/cmdb/cmdb_check_script.sh >> /tmp/cmdb_bastion_account.log 2>&1