from ansible.playbook import PlayBook
from ansible.inventory import Inventory,Host as AHost,Group as AGroup
from ansible import callbacks
from ansible import utils
from ansible import inventory

#ssss

class PlaybookRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):
    def __init__(self, task, stats,script_name,job_id, verbose=None):
        super(PlaybookRunnerCallbacks, self).__init__(stats, verbose)
        self.celery_task = task
        self.script_name=script_name
        self.job_id=job_id

    def on_ok(self, host, host_result):
        super(PlaybookRunnerCallbacks, self).on_ok(host, host_result)
        self.celery_task.logs.append("ok:[%s]" % host)
        # self.celery_task.logs.append("host_result:[%s]" % host_result)
        # upgrade_taks_log_byid(self.job_id,"ok:[%s]" % host)
        self.celery_task.update_state(state='PROGRESS', meta={'msg': self.celery_task.logs})

    def on_unreachable(self, host, results):
        super(PlaybookRunnerCallbacks, self).on_unreachable(host, results)
        # print "unreachable:[%s] %s" % (host, results)
        self.celery_task.logs.append("unreachable:[%s] %s" % (host, results))
        self.celery_task.update_state(state='FAILURE', meta={'msg': self.celery_task.logs})

    def on_failed(self, host, results, ignore_errors=False):
        super(PlaybookRunnerCallbacks, self).on_failed(host, results, ignore_errors)
        self.celery_task.logs.append("failed:[%s] %s" % (host, results))
        self.celery_task.update_state(state='FAILURE', meta={'msg': self.celery_task.logs})


class PlaybookCallbacks(callbacks.PlaybookCallbacks):
    def __init__(self, task, script_name,job_id,verbose=False):
        super(PlaybookCallbacks, self).__init__(verbose);
        self.celery_task = task
        self.script_name=script_name
        self.job_id=job_id

    def on_setup(self):
        super(PlaybookCallbacks, self).on_setup()
        self.celery_task.logs.append("GATHERING FACTS")
        # upgrade_taks_log_byid(self.job_id,"GATHERING FACTS")
        self.celery_task.update_state(state='PROGRESS', meta={'msg': self.celery_task.logs})

    def on_task_start(self, name, is_conditional):
        super(PlaybookCallbacks, self).on_task_start(name, is_conditional)
        self.celery_task.logs.append("TASK: [%s]" % name)
        # upgrade_taks_log_byid(self.job_id,"TASK: [%s]" % name)
        self.celery_task.logs.append("start script: [%s]" % self.script_name)
        # upgrade_taks_log_byid(self.job_id,"start script: [%s]" % self.script_name)
        self.celery_task.update_state(state='PROGRESS', meta={'msg': self.celery_task.logs})


# hostfile = './hosts.py'
# inventory = Inventory(hostfile)
# hosts = {'group':{'hosts': ['10.249.6.36', '10.249.6.37']}}
#
stats = callbacks.AggregateStats()
job_id=0
# vars = {"web":['10.249.6.36', '10.249.6.37']}

# host1 = AHost(name='10.249.6.36')
# host2 = AHost(name='10.249.6.37')
# group1 = AGroup(name="web")
# group1.add_host(host1)
# group1.add_host(host2)
# inventory = Inventory(host_list=['10.249.6.36', '10.249.6.37'], vault_password="Hello123")
# inventory.add_group(group1)

# im = inventory.Inventory('/root/opt/share/iplist')

def get_pb(task,_machines,_playbook,_name,_id):
    group1=''
    group1 = AGroup(name="web")
    host_list=[]
    for m in _machines:
        host_list.append(str(m['ip']))
        host1 = AHost(name=str(m['ip']))
        group1.add_host(host1)
    inventory = Inventory(host_list=host_list, vault_password="Hello123")
    inventory.add_group(group1)

    job_id=_id

    if task:
        runner_cb = PlaybookRunnerCallbacks(task, stats,_name,job_id, verbose=utils.VERBOSITY)
        playbook_cb = PlaybookCallbacks(task,_name,job_id, verbose=utils.VERBOSITY)
    else:
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats,_name,job_id, verbose=utils.VERBOSITY)
        playbook_cb = callbacks.PlaybookCallbacks(_name,job_id,verbose=utils.VERBOSITY)

    pb = PlayBook(playbook=_playbook,
                  callbacks=playbook_cb,
                  runner_callbacks=runner_cb,
                  stats=stats,
                  # host_list=hosts,
                  inventory=inventory,
                  # extra_vars=vars,
                  # key_file='/root/opt/Identity'
                  )
    return pb

if __name__ == '__main__':
    get_pb(None).run()
