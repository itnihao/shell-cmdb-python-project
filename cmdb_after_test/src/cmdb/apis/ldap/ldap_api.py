import ldap
import ldap.modlist as modlist
# from  ldap.controls import SimplePagedResultsControl
from application import app

# BASE_DIR = (os.path.dirname(__file__))
# CONF = ConfigParser()
# CONF.read(os.path.join(BASE_DIR, 'ldapserver.conf'))
#
# LDAP_ENABLE = CONF.getint('ldap', 'ldap_enable')
#
# LDAP_ENABLE=1
#
#
# if LDAP_ENABLE:
#     # LDAP_HOST_URL = CONF.get('ldap', 'host_url')
#     # LDAP_BASE_DN = CONF.get('ldap', 'base_dn')
#     # LDAP_ROOT_DN = CONF.get('ldap', 'root_dn')
#     # LDAP_ROOT_PW = CONF.get('ldap', 'root_pw')
LDAP_HOST_URL = app.config['HOST_URL']
LDAP_BASE_DN = app.config['BASE_DN']
LDAP_ROOT_DN = app.config['ROOT_DN']
LDAP_ROOT_PW = app.config['ROOT_PWD']



class LDAPMgmt():
    def __init__(self,
                 host_url,
                 base_dn,
                 root_cn,
                 root_pw):
        self.ldap_host = host_url
        self.ldap_base_dn = base_dn
        self.conn = ldap.initialize(host_url)
        self.conn.set_option(ldap.OPT_REFERRALS, 0)
        self.conn.protocol_version = ldap.VERSION3
        self.conn.simple_bind_s(root_cn, root_pw)

    def list(self, filter, scope=ldap.SCOPE_SUBTREE, attr=None):
        result = {}
        try:
            ldap_result = self.conn.search_s(self.ldap_base_dn, scope, filter, attr)
            # for entry in ldap_result:
            #     name, data = entry
            #     for k, v in data.items():
            #         print '%s: %s' % (k, v)
            #         result[k] = v
            return ldap_result
        except ldap.LDAPError, e:
            print e


    def add(self, dn, attrs):
        try:
            ldif = modlist.addModlist(attrs)
            self.conn.add_s(dn, ldif)
            return 1
        except ldap.LDAPError, e:
            return 0

    def update(self, dn, attrs):
        try:
            # ldif = modlist.modifyModlist(old,new)
            self.conn.modify_s(dn, attrs)
            return 1
        except ldap.LDAPError, e:
            return 0
            print e

    def rename(self,dn,attrs,base):
        try:
            self.conn.rename_s(dn,attrs,base)
            return 1
        except ldap.LDAPError, e:
            return 0
        
    def addUser(self,username,userid):
        username = username.encode("utf-8")
        dn='uid=%s,ou=Users,%s'%(username,self.ldap_base_dn)
        attrs = {}
        attrs['cn'] = username
        attrs['uid'] = username
        attrs['objectClass'] = ['account','top','posixAccount','shadowAccount']
        attrs['userPassword'] = '{SSHA}R8apRtO7u0f8vnpJSkAG7ZPGMqmxL9Kw'
        attrs['loginShell'] = '/bin/bash'
        attrs['uidNumber'] = '%s'%userid
        attrs['gidNumber'] = '1000'
        attrs['homeDirectory'] = '/home/%s'%(username)
        self.add(dn,attrs)
        print('User %s add seccessful!'%(username))

    def addSudo(self, user ,commands):
        sudoDn = 'ou=Sudoers,%s'%self.ldap_base_dn;
        try:
            ldap_result = self.conn.search_s(sudoDn,ldap.SCOPE_SUBTREE,'cn=%s'%user,None)
        except ldap.LDAPError, e:
            return 0
        dn='cn=%s,%s'%(user,sudoDn)
        if not ldap_result:
            attrs = {}
            attrs['cn'] = user
            attrs['objectClass'] = ['top','sudoRole']
            attrs['sudoCommand'] = ['!ALL']
            attrs['sudoCommand'].extend(commands)
            attrs['sudoHost'] = ['ALL']
            attrs['sudoOption'] = ['!authenticate']
            attrs['sudoRunAsUser'] = ['ALL']
            attrs['sudoUser'] = user
            return self.add(dn,attrs)
        else:
            sudoCommand = ldap_result[0][1]['sudoCommand']
            for sudoCmd in sudoCommand:
                commands = [command for command in commands if sudoCmd != command]
            sudoCommand.extend(commands)
            attrs=[(ldap.MOD_REPLACE,'sudoCommand',sudoCommand)]
            return self.update(dn,attrs)

    def delSudo(self, user ,commands ,type = 'ALL'):
        sudoDn = 'ou=Sudoers,%s'%self.ldap_base_dn;
        try:
            ldap_result = self.conn.search_s(sudoDn,ldap.SCOPE_SUBTREE,'cn=%s'%user,None)
        except ldap.LDAPError, e:
            return 0
        if ldap_result:
            dn='cn=%s,%s'%(user,sudoDn)
            sudoCommand = ldap_result[0][1]['sudoCommand']
            if type == 'ALL':
                sudoCommand = ['ALL']
            else:
                for command in commands:
                    sudoCommand = [sudoCmd for sudoCmd in sudoCommand if sudoCmd != command]
            attrs=[(ldap.MOD_REPLACE,'sudoCommand',sudoCommand)]
            return self.update(dn,attrs)

    def addDepart(self,departname):
        sudo_dn = 'ou=%s,%s' % (departname,LDAP_BASE_DN)
        sudo_attr = {'objectClass': ['top', 'organizationalUnit'],
                 'ou': ['%s' % departname],

                 }
        return self.add(sudo_dn,sudo_attr)

    def updateDepart(self,old_departname,new_department):
        return_code=1
        sudo_dn = 'ou=%s,%s' % (old_departname,LDAP_BASE_DN)
        # mod_attrs = [
        #     (ldapgroup.MOD_REPLACE,'ou',new_department),
        # ]
        # self.update(sudo_dn,mod_attrs)
        # ldap_result=self.list(('ou=%s' %(old_departname)))
        try:
            self.addDepart(new_department)
        except Exception,e:
            None
        ldap_result = self.conn.search_s(sudo_dn, ldap.SCOPE_SUBTREE, 'cn=*', None)

        for item in ldap_result:
            dn=item[0]
            attrs=item[1]
            if self.updateDepartmentforGroup(old_departname,new_department,attrs['cn'][0])==0:
                return_code=0
                break
        self.deleteDepart(old_departname)
        return return_code
        # ldap_result = self.conn.search_s(sudo_dn, ldapgroup.SCOPE_SUBTREE, 'ou=*', None)
        # print ldap_result
        # self.rename(sudo_dn,'ou=%s' % (new_department),LDAP_BASE_DN)

    def updateDepartmentforGroup(self,old_department,new_department,group):
        sudo_dn='cn=%s,ou=%s,%s' % (group,old_department,LDAP_BASE_DN)
        return self.rename(sudo_dn,'cn=%s' % (group),'ou=%s,%s' % (new_department,LDAP_BASE_DN))

    def deleteDepart(self,department):
        sudo_dn = 'ou=%s,%s' % (department,LDAP_BASE_DN)
        ldap_result = self.conn.search_s(sudo_dn, ldap.SCOPE_SUBTREE, 'cn=*', None)
        for item in ldap_result:
            dn=item[0]
            attrs=item[1]
            if self.delete('%s,ou=%s,%s' % (dn.split(',')[0],str(department),LDAP_BASE_DN))==0:
                return 0
        return self.delete(sudo_dn)

    def addGroup(self,department,group):
        sudo_dn='cn=%s,ou=%s,%s' % (group,department,LDAP_BASE_DN)
        number=self.genNewGid('gidNumber')
        sudo_attr={'objectClass': ['top', 'posixGroup'],
                 'cn': ['%s' % group],
                 'cn': ['%s' % str(number)],
                  'gidNumber':[str(number)]
                 }
        return {'code':self.add(sudo_dn,sudo_attr),'number':str(number)}

    def updateGroup(self,department,old_group,new_group):
        sudo_dn='cn=%s,ou=%s,%s' % (old_group,department,LDAP_BASE_DN)
        # mod_attrs = [
        #     (ldapgroup.MOD_REPLACE,'ou',new_department),
        # ]
        # self.update(sudo_dn,mod_attrs)
        return self.rename(sudo_dn,'cn=%s' % (new_group),'ou=%s,%s' % (department,LDAP_BASE_DN))

    def deleteGroup(self,groupname,department,gid):
        try:
            sudo_group_sudo='cn=%s,ou=%s,%s' % ('%#'+gid,'Sudoers',LDAP_BASE_DN)
            self.delete(sudo_group_sudo)
        except Exception,e:
            print e

        sudo_dn = 'cn=%s,ou=%s,%s' % (groupname,department,LDAP_BASE_DN)
        return self.delete(sudo_dn)

    def addUser2Group(self,user,group,department):
        sudo_dn='cn=%s,ou=%s,%s' % (group,department,LDAP_BASE_DN)
        add_attrs = [
            (ldap.MOD_ADD,'memberUid',user),
        ]
        self.update(sudo_dn,add_attrs)

    def deleteUserFromGroup(self,user,group,department):
        sudo_dn='cn=%s,ou=%s,%s' % (group,department,LDAP_BASE_DN)
        add_attrs = [
            (ldap.MOD_DELETE,'memberUid',user),
        ]
        return self.update(sudo_dn,add_attrs)

    def modify(self, dn, attrs):
        try:
            attr_s = []
            for k, v in attrs.items():
                attr_s.append((2, k, v))
            self.conn.modify_s(dn, attr_s)
        except ldap.LDAPError, e:
            print e

    def delete(self, dn):
        try:
            self.conn.delete_s(dn)
            return 1
        except ldap.LDAPError, e:
            return 0

    def genNewGid(self,filter1):
        ldap_result = self.conn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE, '%s=*' %(filter1), [filter1])
        list_number=[]
        if(ldap_result):
            for entry in ldap_result:
                name,data = entry
                list_number.append(data['gidNumber'][0])
            return int(max(int (i) for i in list_number)+1)
        else:
            return 1