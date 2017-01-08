# coding=utf-8
__author__ = 'qiqi'
import paramiko
from application import app

class ParamikoLib():
    def __init__(self,host):
        self.host = host
        self.port = 22
        self.user = 'root'
        self.key = paramiko.RSAKey.from_private_key_file(app.config.get('ANSIBLE_KEY'),app.config.get('ANSIBLE_KEY_PASS'))
        self.stdin = ''
        self.stdout = ''
        self.stderr = ''
        self.par = paramiko.SSHClient()
        self.par.load_system_host_keys()
        self.par.connect(self.host,self.port,self.user,self.key)

    def execute(self,command):
        self.stdin,self.stdout,self.stderr = self.par.exec_command(command)

    def get_stdin(self):
        return self.stdin.read().strip()

    def get_stdout(self):
        return self.stdout.read().strip()

    def get_stderr(self):
        return self.stderr.read().strip()

