
import json
import os
group = os.environ.get('ANSBILE_HOST_GROUP')

hosts = {
    'web': ['localhost', '127.0.0.1'],
    'group2': ['127.0.0.1'],
}

ret = hosts.get(group, [])
ret = {"default": ret}

print json.dumps(ret, indent=4)