# -*- coding: utf-8 -*-
import re
from sqlalchemy import and_

from flask import Blueprint, render_template, request,json

from flask_login import login_required

from application import fujs
from views.functions import visible, responsejson
from views.log import addlog
from models.user import *
from models.user_host import *
from models.host import *
from models.ip_address import *
from models.host_ip import *
from apis.ldap.ldap_api import *


@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

ldapgroup = Blueprint('ldapgroup', __name__)

try:
    ldap_conn = LDAPMgmt(LDAP_HOST_URL, LDAP_BASE_DN, LDAP_ROOT_DN, LDAP_ROOT_PW)
except:
    ldap_conn=''

@ldapgroup.route("/deplist", methods=['POST', 'GET'])
@login_required
def deplist():
    show = visible()
    # maps=Usergroupmap.query.all()
    # se=Usergroupmapchema(many=True).dump(maps)
    # se1=se.data
    department_q=Department.query.all()
    se=DepartmentSchema(many=True).dump(department_q)
    department=se.data
    return render_template('ldapgroup/deplist.html', show=show, department=department)


@ldapgroup.route("/depadd", methods=['POST', 'GET'])
@login_required
def depadd():
    if request.method == 'POST':
        name=request.form['name']
        description=request.form['description']
        leaderid=request.form['leaderid']
        bleaderid=request.form['bleaderid']
        try:
            select_same=Department.query.filter_by(name=name).all()
            if select_same:
                return responsejson(1,'Department aleardy existed!')
            # if ldap_conn.addDepart(str(name))==0:
            #     return responsejson(1,'Department add failed!')
            dctarget=Department(name=name,description=description,leader_uid=leaderid,bleader_uid=bleaderid)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'Department add failed!')

@ldapgroup.route("/depdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def depdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除部门失败")
        info=Department.query.filter(Department.id==id).first()
        # su_dn='ou=%s' % (info.name)
        # searche_r=ldap_conn.list(su_dn)
        # if searche_r:
        #     if ldap_conn.deleteDepart(str(info.name))==0:
        #         su_dn='ou=%s' % (info.name)
        #         searche_r=ldap_conn.list(su_dn)
        #         if searche_r:
        #             return responsejson(1,"删除部门失败")

        db.session.delete(info)
        db.session.commit()
        logmsg="删除部门,部门id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除部门成功")
    except Exception,e:
        return responsejson(1,"删除部门失败")

@ldapgroup.route("/depmodify/<int:id>",methods=['GET', 'POST'])
@login_required
def depmodify(id):
    try:
        logmsg=""
        code=0
        intreg=re.compile('^\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,'修改部门失败')

        info=Department.query.filter(Department.id==id).first()
        name=request.form['name']
        description=request.form['description']
        leaderid=request.form['leaderid']
        bleaderid=request.form['bleaderid']

        if info.name!=name:
            # if ldap_conn.updateDepart(str(info.name),str(name))==0:
            #     return responsejson(1,'修改部门失败')
            logmsg=logmsg+"name:%s 更改为 %s"%(info.name,name)+","
            info.name=name
        if info.description!=description:
            logmsg=logmsg+"description:%s 更改为 %s"%(info.description,description)+","
            info.description=description
        info.leader_uid=leaderid
        info.bleader_uid=bleaderid

        info.updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        logmsg="修改部门信息,id:%d,%s"%(id,logmsg)
        addlog(logmsg,1)
        return responsejson(0,'')
    except Exception,e:
        return responsejson(0,'修改部门失败')

@ldapgroup.route("/<int:id>",methods=['GET', 'POST'])
@login_required
def detail(id):
    jsonval={}
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    info=Department.query.filter(Department.id==id).first()
    id_name = {}
    user_ = User.query.all()
    for user in user_:
        id_name[user.id] = user.cn_name

    if info:
        jsonval['id']=info.id
        jsonval['name']=info.name
        jsonval['description_r']=info.description
        jsonval['leader_uid']= info.leader_uid
        jsonval['leader_name']= id_name[info.leader_uid]
        jsonval['bleader_uid']=info.bleader_uid
        jsonval['bleader_name']=id_name[info.bleader_uid]

    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@ldapgroup.route("/grouplist", methods=['POST', 'GET'])
@login_required
def grouplist():
    show = visible()
    # maps=Usergroupmap.query.all()
    # se=Usergroupmapchema(many=True).dump(maps)
    # se1=se.data
    group_q=Group.query.all()
    se=GroupSchema(many=True).dump(group_q)
    group=se.data

    department_info=DepartmentSchema(many=True).dump(Department.query.all()).data
    return render_template('ldapgroup/grouplist.html', show=show, group=group,department_info=department_info)

@ldapgroup.route("/groupadd", methods=['POST', 'GET'])
@login_required
def groupadd():
    if request.method == 'POST':
        name=str(request.form['name'])

        description=str(request.form['description'])

        dp_id=int(request.form['id'])
        try:
            select_de=Department.query.filter(Department.id==dp_id).first()
            sudo_dn='cn=%s' % (name)
            # result_s=ldap_conn.list(sudo_dn)
            # if not result_s:
            #     add_return=ldap_conn.addGroup(select_de.name,name)
            #     if add_return['code']==0:
            #         return responsejson(1,'Group add failed!')
            #     ldap_id=add_return['number']
            # else:
            #     cn,attr=result_s[0]
            #     ldap_id=attr['gidNumber']

            dctarget=Group(name=name,description=description,ldap_id='0',department_id=dp_id)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'Department add failed!')

@ldapgroup.route("/groupdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def groupdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除组失败")
        info=Group.query.filter(Group.id==id).first()
        # su_dn='cn=%s' % (info.name)
        # searche_r=ldap_conn.list(su_dn)
        # if searche_r:
        #     if ldap_conn.deleteGroup(str(info.name),str(info.department.name),str(info.ldap_id))==0:
        #         su_dn='cn=%s' % (info.name)
        #         searche_r=ldap_conn.list(su_dn)
        #         if searche_r:
        #             return responsejson(1,"删除组失败")

        db.session.delete(info)
        db.session.commit()
        logmsg="删除组,组id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除组成功")
    except Exception,e:
        return responsejson(1,"删除组失败")

@ldapgroup.route("/group/<int:id>",methods=['GET', 'POST'])
@login_required
def group(id):
    jsonval={}
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    info=Group.query.filter(Group.id==id)
    # if info:
    #     jsonval['id']=info.id
    #     jsonval['name']=info.name
    #     jsonval['description_r']=info.description
    #     jsonval['department']=info.department
    jsonval=GroupSchema(many=True).dump(info).data[0]
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@ldapgroup.route("/groupdetail/<int:id>",methods=['GET', 'POST'])
@login_required
def groupdetail(id):
    show=visible()
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        return app.response_class(json.dumps({}), mimetype='application/json')
    info=Usergroupmap.query.filter(Usergroupmap.group_id==id)

    jsonval=UsergroupmapSchema(many=True).dump(info).data
    current_group=Group.query.filter(Group.id==id).first()
    return render_template('ldapgroup/groupdetail.html', maps=jsonval,show=show,current_group=current_group)


@ldapgroup.route("/groupmodify/<int:id>",methods=['GET', 'POST'])
@login_required
def groupmodify(id):
    try:
        logmsg=""
        code=0
        intreg=re.compile('^\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,'修改组失败')

        info=Group.query.filter(Group.id==id).first()
        name=request.form['name']
        description=request.form['description']
        dp_id=request.form['id']

        mo_dp=Department.query.filter(Department.id==int(dp_id)).first()
        if info.department.name!=mo_dp.name:
            # if ldap_conn.updateDepartmentforGroup(str(info.department.name),str(mo_dp.name),info.name)==0:
            #      return responsejson(1,'修改组失败')
            info.department_id=int(dp_id)
        if info.name!=name:
            # if ldap_conn.updateGroup(str(mo_dp.name),str(info.name),str(name))==0:
            #     return responsejson(1,'修改组失败')
            logmsg=logmsg+"name:%s 更改为 %s"%(info.name,name)+","
            info.name=name
        if info.description!=description:
            logmsg=logmsg+"description:%s 更改为 %s"%(info.description,description)+","
            info.description=description

        info.updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        logmsg="修改组信息,id:%d,%s"%(id,logmsg)
        addlog(logmsg,1)
        return responsejson(0,'')
    except Exception,e:
        return responsejson(1,'修改组失败')

# @ldapgroup.route("/groupdeleteuser", methods=['POST', 'GET'])
# @login_required
# def groupdeleteuser():
#     if request.method == 'POST':
#         user_id=request.form['user_id']
#         group_id=request.form['group_id']

@ldapgroup.route("/sudolist", methods=['POST', 'GET'])
@login_required
def sudolist():
    show = visible()
    # maps=Usergroupmap.query.all()
    # se=Usergroupmapchema(many=True).dump(maps)
    # se1=se.data
    sudo_q=Sudo.query.all()
    se=SudoSchema(many=True).dump(sudo_q)
    sudo_r=se.data
    return render_template('ldapgroup/sudolist.html', show=show, sudo=sudo_r)

@ldapgroup.route("/sudoadd", methods=['POST', 'GET'])
@login_required
def sudoadd():
    if request.method == 'POST':
        name=request.form['name']
        description=request.form['description']
        try:
            select_same=Sudo.query.filter_by(cmd=name).all()
            if select_same:
                return responsejson(1,'Department aleardy existed!')
            dctarget=Sudo(cmd=name,description=description)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'Department add failed!')

@ldapgroup.route("/sudodetail/<int:id>",methods=['GET', 'POST'])
@login_required
def sudodetail(id):
    jsonval={}
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    info=Sudo.query.filter(Sudo.id==id)
    # if info:
    #     jsonval['id']=info.id
    #     jsonval['name']=info.name
    #     jsonval['description_r']=info.description
    #     jsonval['department']=info.department
    jsonval=SudoSchema(many=True).dump(info).data[0]
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@ldapgroup.route("/sudomodify/<int:id>",methods=['GET', 'POST'])
@login_required
def sudomodify(id):
    try:
        logmsg=""
        code=0
        intreg=re.compile('^\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,'修命令失败')

        info=Sudo.query.filter(Sudo.id==id).first()
        name=request.form['name']
        description=request.form['description']

        if info.cmd!=name:

            logmsg=logmsg+"name:%s 更改为 %s"%(info.cmd,name)+","
            info.cmd=name
        if info.description!=description:
            logmsg=logmsg+"description:%s 更改为 %s"%(info.description,description)+","
            info.description=description

        info.updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        logmsg="修改命令信息,id:%d,%s"%(id,logmsg)
        addlog(logmsg,1)
        return responsejson(0,'')
    except Exception,e:
        return responsejson(1,'修改命令失败')

@ldapgroup.route("/sudodelete/<int:id>",methods=['GET', 'POST'])
@login_required
def sudodelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除命令失败")
        info=Sudo.query.filter(Sudo.id==id).first()

        db.session.delete(info)
        db.session.commit()
        logmsg="删除命令,命令id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除命令成功")
    except Exception,e:
        return responsejson(1,"删除命令失败")

@ldapgroup.route("/sudouser", methods=['POST', 'GET'])
@login_required
def sudouser():
    show = visible()
    users=User.query.all()
    # se=UserSchema(many=True).dump(users)
    return_u={'cn':[],'ping':[]}
    for u in users:
        return_u['ping'].append(u.name)
        return_u['cn'].append(u.cn_name)

    # maps=Usergroupmap.query.all()
    # se=Usergroupmapchema(many=True).dump(maps)
    # se1=se.data
    # department_q=Department.query.all()
    # se=DepartmentSchema(many=True).dump(department_q)
    # department=se.data
    return render_template('ldapgroup/user_sudo.html', show=show, users=return_u,sudo='')

@ldapgroup.route("/sudouser/usersudodetails/<name>",methods=['GET', 'POST'])
@login_required
def usersudodetails(name):
    show = visible()
    user=User.query.filter(User.name==str(name)).first()
    if not user:
        user=User.query.filter(User.cn_name==str(name)).first()
        # if not user:
        #     return responsejson(0,"no user")
    user_current=UserSchema().dump(user).data

    info=Sudousermap.query.filter(Sudousermap.user_id==user.id)
    se=SudousermapSchema(many=True).dump(info)

    groups_s=Usergroupmap.query.filter(Usergroupmap.user_id==user.id).all()
    group=UsergroupmapSchema(many=True).dump(groups_s).data


    uhs=UserHost.query.filter(UserHost.uid==user.id).all()
    return_host=[]
    for uh in uhs:
       ma=Host.query.filter(Host.id==uh.host_id).first()
       ip=IpAddress.query.filter(IpAddress.id==ma.primary_ip_id).first()
       return_host.append({'hostid':uh.host_id,'hostname':ma.hostname,"ip":ip.ipv4,'id':uh.id})


    users=User.query.all()
    return_u={'cn':[],'ping':[]}
    for u in users:
        return_u['ping'].append(u.cn_name)
        return_u['cn'].append(u.name)

    cmd_info=SudoSchema(many=True).dump(Sudo.query.all()).data
    group_info=GroupSchema(many=True).dump(Group.query.all()).data

    # pool_all=Pool.query.all()
    # pool_info=[]
    # for each_pool in pool_all:
    #     pool_info.append({'name':each_pool.name,'id':each_pool.id})

    pools_user=Userpoolmap.query.filter(Userpoolmap.user_id==user.id).all()
    pools=[]
    for each_poo_user in pools_user:
        pools.append({'id':each_poo_user.id,'user_id':each_poo_user.user_id,'pool_id':each_poo_user.pool_id
                      ,'pool':{'name':each_poo_user.pool.name,'id':each_poo_user.pool.id}})

    return render_template('ldapgroup/userforsudo.html', sudo=se.data, show=show, cmd_info=cmd_info,groups=group,pools=pools,
                           users=return_u,user_current=user_current,hosts=return_host,group_info=group_info)
    # return app.response_class(json.dumps(se.data), mimetype='application/json')

@ldapgroup.route("/sudouseradd",methods=['GET', 'POST'])
@login_required
def sudouseradd():
    if request.method == 'POST':
        user_id=request.form['user_id']
        sudo_id=request.form['sudo_id']
        try:
            select_same=Sudousermap.query.filter_by(user_id=user_id,sudo_id=sudo_id).all()
            if select_same:
                return responsejson(1,'Mapping aleardy existed!')
            user=User.query.filter(User.id==int(user_id)).first()
            sudo=Sudo.query.filter(Sudo.id==int(sudo_id)).first()
            if ldap_conn.addSudo(str(user.name),[str(sudo.cmd)])==0:
                return responsejson(1,'Add failed!')

            dctarget=Sudousermap(user_id=user_id,sudo_id=sudo_id)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'sudo add failed!')

@ldapgroup.route("/sudouserdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def sudouserdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删用户命令失败")
        info=Sudousermap.query.filter(Sudousermap.id==id).first()
        user=User.query.filter(User.id==info.user_id).first()
        sudo=Sudo.query.filter(Sudo.id==info.sudo_id).first()

        if ldap_conn.delSudo(str(user.name),[str(sudo.cmd)],type='one')==0:

            return responsejson(1,"删用户命令失败")

        db.session.delete(info)
        db.session.commit()
        logmsg="删除用户命令,命令id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除用户命令成功")
    except Exception,e:
        return responsejson(1,"删除用户命令失败")

@ldapgroup.route("/sudouserdevices",methods=['GET', 'POST'])
@login_required
def sudouserdevices():
    try:
        alldevices={'hostname':[],'ip':[]}
        hosts=Host.query.all()
        for h in hosts:
            if(h.deleted==0):
                alldevices['hostname'].append(h.hostname)
                ip=IpAddress.query.filter(IpAddress.id==h.primary_ip_id).first()
                if(ip):
                    alldevices['ip'].append(ip.ipv4)
        return app.response_class(json.dumps(alldevices), mimetype='application/json')

    except Exception,e:
       return app.response_class(json.dumps({}), mimetype='application/json')

@ldapgroup.route("/userdeviceadd",methods=['GET', 'POST'])
@login_required
def userdeviceadd():
    if request.method == 'POST':
        user_id=request.form['user_id']
        device=request.form['device']
        try:
            count_s=str(device).split('.')
            if(len(count_s)>3):
                ip_s=IpAddress.query.filter(IpAddress.ipv4==str(device)).first()
                if not ip_s:
                    return responsejson(1,'No such device!')
                host_s=Host.query.filter(Host.primary_ip_id==ip_s.id).first()
                if not host_s:
                    return responsejson(1,'No such device!')
            else:
                host_s=Host.query.filter(Host.hostname==device).first()
                if not host_s:
                    return responsejson(1,'No such device!')

            dctarget=UserHost(uid=int(user_id),host_id=host_s.id,role=1,status=1)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'Department add failed!')

@ldapgroup.route("/userdevicedelete/<int:id>",methods=['GET', 'POST'])
@login_required
def userdevicedelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删用户设备失败")
        info=UserHost.query.filter(UserHost.id==id).first()

        if not info:

            return responsejson(1,"删用户设备失败")

        db.session.delete(info)
        db.session.commit()
        logmsg="删除用户设备,设备id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除用户设备成功")
    except Exception,e:
        return responsejson(1,"删除用户设备失败")

@ldapgroup.route("/usergroupadd", methods=['POST', 'GET'])
@login_required
def usergroupadd():
    if request.method == 'POST':
        user_id=int(request.form['user_id'])
        group_id=int(request.form['group_id'])

        try:
            select_group=Group.query.filter(Group.id==group_id).first()
            select_dep=Department.query.filter(Department.id==select_group.department_id).first()
            select_user=User.query.filter(User.id==user_id).first()

            # sudo_dn='ou=%s' % (str(select_dep.name))
            # result_s=ldap_conn.list(sudo_dn)
            # if not result_s:
            #     ldap_conn.addDepart(str(select_dep.name))
            #
            # sudo_dn='cn=%s' % (str(select_group.name))
            # result_s=ldap_conn.list(sudo_dn)
            # if not result_s:
            #     add_return=ldap_conn.addGroup(str(select_dep.name),str(select_group.name))
            #     if add_return['code']==0:
            #         # print 1
            #         return responsejson(1,'UserGroup add failed!')
            #     ldap_id=add_return['number']

            # if ldap_conn.addUser2Group(str(select_user.name),str(select_group.name),str(select_dep.name))==0:
            #     # print 2
            #     return responsejson(1,'UserGroup add failed!')

            select_usergroup=Usergroupmap.query.filter(Usergroupmap.user_id==user_id,Usergroupmap.group_id==group_id).first()
            if select_usergroup:
                return responsejson(1,'UserGroup add Existed!')

            dctarget=Usergroupmap(user_id=user_id,group_id=group_id)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            print e.message
            return responsejson(1,'UserGroup add failed!')

@ldapgroup.route("/usergroupdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def usergroupdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删用户组失败")

        info=Usergroupmap.query.filter(Usergroupmap.id==id).first()

        if not info:
            return responsejson(1,"删用户组失败")

        select_group=Group.query.filter(Group.id==info.group_id).first()
        select_dep=Department.query.filter(Department.id==select_group.department_id).first()
        select_user=User.query.filter(User.id==info.user_id).first()

        # if ldap_conn.deleteUserFromGroup(str(select_user.name),str(select_group.name),str(select_dep.name))==0:
        #     return responsejson(1,"删用户组失败")

        db.session.delete(info)
        db.session.commit()
        logmsg="删除用户组,组id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除用户组成功")
    except Exception,e:
        return responsejson(1,"删除用户组失败")

@ldapgroup.route("/sudogroup/<int:id>",methods=['GET', 'POST'])
@login_required
def sudogroup(id):
    show = visible()

    group=Group.query.filter(Group.id==id).first()

        # if not user:
        #     return responsejson(0,"no user")
    group_current=GroupSchema().dump(group).data

    info=Sudogroupmap.query.filter(Sudogroupmap.group_id==group.id)
    se=SudousermapSchema(many=True).dump(info)


    cmd_info=SudoSchema(many=True).dump(Sudo.query.all()).data

    return render_template('ldapgroup/sudogroup.html', sudo=se.data, show=show, cmd_info=cmd_info,
                           group_current=group_current)
    # return app.response_class(json.dumps(se.data), mimetype='application/json')

@ldapgroup.route("/sudogroupadd",methods=['GET', 'POST'])
@login_required
def sudogroupadd():
    if request.method == 'POST':
        group_id=request.form['group_id']
        sudo_id=request.form['sudo_id']
        try:
            select_same=Sudogroupmap.query.filter_by(group_id=group_id,sudo_id=sudo_id).all()
            if select_same:
                return responsejson(1,'Mapping aleardy existed!')
            group=Group.query.filter(Group.id==int(group_id)).first()
            sudo=Sudo.query.filter(Sudo.id==int(sudo_id)).first()
            if ldap_conn.addSudo('%#'+str(group.ldap_id),[str(sudo.cmd)])==0:
                return responsejson(1,'Add failed!')

            dctarget=Sudogroupmap(group_id=group_id,sudo_id=sudo_id)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,' Add failed!')

@ldapgroup.route("/sudogroupdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def sudogroupdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删命令失败")
        info=Sudogroupmap.query.filter(Sudogroupmap.id==id).first()
        group=Group.query.filter(Group.id==info.group_id).first()
        sudo=Sudo.query.filter(Sudo.id==info.sudo_id).first()

        if ldap_conn.delSudo('%#'+str(group.ldap_id),[str(sudo.cmd)],type='one')==0:

            return responsejson(1,"删命令失败")

        db.session.delete(info)
        db.session.commit()
        logmsg="删除组命令,命令id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除命令成功")
    except Exception,e:
        return responsejson(1,"删除命令失败")

@ldapgroup.route("/userpooladd",methods=['GET', 'POST'])
@login_required
def userpooladd():
    if request.method == 'POST':
        try:
            msg=''
            user_id=request.form['user_id']
            pool_ids=request.form['pool_ids'].split(',')
            for pool_name in pool_ids:
            # pool_name=request.form['pool']
                try:
                    select_pool=Pool.query.filter(Pool.id==pool_name).first()
                    if not select_pool:
                        msg+=pool_name+' not existed!'
                        continue
                    select_same=Userpoolmap.query.filter_by(user_id=user_id,pool_id=select_pool.id).all()
                    if select_same:
                       msg+=pool_name+'Mapping aleardy existed!'
                       continue
                    user=User.query.filter(User.id==int(user_id)).first()
                    # sudo=Sudo.query.filter(Sudo.id==int(sudo_id)).first()
                    # if ldap_conn.addSudo(str(user.name),[str(sudo.cmd)])==0:
                    #     return responsejson(1,'Add failed!')

                    dctarget=Userpoolmap(user_id=user_id,pool_id=select_pool.id)
                    db.session.add(dctarget)
                    db.session.commit()
                except Exception,e:
                    msg+=pool_name+' add failed!'
            return responsejson(0,msg)
        except Exception,e:
            return responsejson(1,"add Pool失败")

@ldapgroup.route("/userpooldelete/<int:id>",methods=['GET', 'POST'])
@login_required
def userpooldelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删用户Pool失败")

        info=Userpoolmap.query.filter(Userpoolmap.id==id).first()

        if not info:
            return responsejson(1,"删用户Pool失败")

        select_pool=Pool.query.filter(Pool.id==info.pool_id).first()
        # select_dep=Department.query.filter(Department.id==select_group.department_id).first()
        select_user=User.query.filter(User.id==info.user_id).first()

        db.session.delete(info)
        db.session.commit()
        logmsg="删除用户Pool,Pool:id:%d"%(id)
        addlog(logmsg,1)
        return responsejson(0,"删除用户Pool成功")
    except Exception,e:
        return responsejson(1,"删除用户Pool失败")

@ldapgroup.route("/pickpool/<int:id>",methods=['GET', 'POST'])
@login_required
def pickpool(id):
    pool_user=UserSchema().dump(User.query.filter(User.id==id).first()).data
    self_pools=Userpoolmap.query.filter(Userpoolmap.user_id==id).all()

    q = request.args.get("q",'')
    pool_list_retrun=[]
    if q:
        kw = '%'+q+'%'
        poollist=Pool.query.filter(and_(Pool.search.like(kw),Pool.deleted == Pool.DELETED_NO )).order_by(Pool.id.desc()).all()
    else:
        poollist=Pool.query.filter(Pool.deleted == Pool.DELETED_NO ).order_by(Pool.id.desc()).all()
    if poollist:
        userids=find_userids(poollist)
        userlist={}
        if userids:
            userinfo=User.query.filter(User.id.in_(userids)).all()
            if userinfo:
                for item in userinfo:
                    userlist['uid_%s'%item.id]=item.cn_name


        for poolinfo in poollist:
            isexist_pool=False
            for each_pool in self_pools:
                if(each_pool.pool_id==poolinfo.id):
                    isexist_pool=True
                    break
            if isexist_pool:
                continue
            poolinfo.team_owner_name=userlist['uid_%s'%poolinfo.team_owner]
            poolinfo.ops_owner_name=userlist['uid_%s'%poolinfo.ops_owner]
            poolinfo.biz_owner_name=userlist['uid_%s'%poolinfo.biz_owner]
            pool_list_retrun.append(poolinfo)


    return render_template("ldapgroup/userpickpool.html",poollist=pool_list_retrun,pool_user=pool_user)

def find_userids(poollist):
    userids = []
    for poolinfo in poollist:
        if poolinfo.ops_owner not in userids:
            userids.append(poolinfo.ops_owner)
        if poolinfo.team_owner not in userids:
            userids.append(poolinfo.team_owner)
        if poolinfo.biz_owner not in userids:
            userids.append(poolinfo.biz_owner)
    return userids

