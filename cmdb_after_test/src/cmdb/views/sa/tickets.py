# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from pypages import Paginator
from sqlalchemy import or_,and_,desc
from models.sa.tickets import Tickets
from models.sa.tickets_task import Tickets_Task
from models.sa.tickets_category import Tickets_Category
from models.sa.tickets_comments import Tickets_Comments
from views.functions import responsejson, addmail
from views.user import get_user_info
import json

tickets = Blueprint('tickets', __name__)

@tickets.route("/")
@login_required
def index():
    if not current_user.is_sa:
        return redirect("/")
    p = request.args.get('p',1)
    per_page = 50
    range_num = 10
    uid = current_user.id
    cat_dic = {}
    uids = []
    tickets_id = []
    tickets_tasks_dic = {}
    idx = 1
    cat_list = Tickets_Category.query.all()
    if cat_list:
        for cat_item in cat_list:
            cat_dic[cat_item.id] = cat_item
    target = Tickets.query
    total_num = target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    tickets_info = target.order_by(Tickets.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    for tickets_item in tickets_info:
        tickets_id.append(tickets_item.id)
        uids.append(tickets_item.uid)
    tickets_tasks_info = Tickets_Task.query.filter(Tickets_Task.tickets_id.in_(tickets_id)).all()

    for tickets_tasks_item in tickets_tasks_info:
        tmp_tickets_id = tickets_tasks_item.tickets_id
        if tmp_tickets_id not in tickets_tasks_dic:
            tickets_tasks_dic[tmp_tickets_id] = []

        tickets_tasks_dic[tmp_tickets_id].append({
            'tickets_cat_id':tickets_tasks_item.tickets_cat_id,
            'manage_uid':tickets_tasks_item.manage_uid,
            'content':tickets_tasks_item.content
        })
        uids.append(tickets_tasks_item.manage_uid)


    user_mapping = get_user_info(uids = uids)
    for tickets_item in tickets_info:
        tickets_item.idx = idx
        tickets_item.uid_cname = user_mapping[tickets_item.uid].cn_name
        tickets_item.cat_name = ''
        tickets_item.content = ''
        tickets_item.manage_name = ''
        idx += 1
        if tickets_item.id in tickets_tasks_dic:
            for tmp_tickets_tasks_item in tickets_tasks_dic[tickets_item.id]:
                tmp_cat_dic = cat_dic[tmp_tickets_tasks_item['tickets_cat_id']]
                tmp_user_info = user_mapping[tmp_tickets_tasks_item['manage_uid']]
                tmp_cat_name = tmp_cat_dic.name if  tmp_cat_dic.name == tmp_cat_dic.label else '%s-%s'%(tmp_cat_dic.label,tmp_cat_dic.name)
                tickets_item.cat_name += tmp_cat_name + ","
                tickets_item.manage_name += tmp_user_info.cn_name + ","
                tickets_item.content += '<br/>分类:'+ tmp_cat_name  + '&nbsp;&nbsp;简述:' +tmp_tickets_tasks_item['content'] + "<br/>"
            tickets_item.cat_name = tickets_item.cat_name[:-1]
            tickets_item.manage_name = tickets_item.manage_name[:-1]

    extend = {
        'total':total_num,
        'cur_total':len(tickets_info)
    }
    return render_template('/sa/tickets/list.html',tickets = tickets_info , extend = extend, p = page)


@tickets.route("/<int:id>")
@login_required
def detail(id):
    uid = current_user.id
    cat_dic = {}
    uids = []
    extend = {}
    tmp_idx = 1
    task_closed_counter = 0
    ticket_info = Tickets.query.filter(Tickets.id == id).first()
    if not ticket_info:
        return redirect(url_for('user.tickets'))
    tasks = Tickets_Task.query.filter(Tickets_Task.tickets_id == id).all()
    cat_list = Tickets_Category.query.all()
    history_info = Tickets_Comments.query.filter(Tickets_Comments.tickets_id == id).order_by(Tickets_Comments.id.desc()).limit(5).all()

    if cat_list:
        for cat_item in cat_list:
            cat_dic[cat_item.id] = cat_item

    for task_item in tasks:
        uids.append(task_item.manage_uid)

    for history_item in history_info:
        uids.append(history_item.uid)

    uids.append(ticket_info.uid)

    user_mapping = get_user_info(uids = uids)
    for task_item in tasks:
        task_item.idx = tmp_idx
        task_item.manage_cname = user_mapping[task_item.manage_uid].cn_name
        tmp_tickets_cat_info = cat_dic[task_item.tickets_cat_id]
        task_item.tickets_cat_name = tmp_tickets_cat_info.name if \
            tmp_tickets_cat_info.name == tmp_tickets_cat_info.label else\
            '%s-%s'%(tmp_tickets_cat_info.label,tmp_tickets_cat_info.name)
        task_item.can_closed = True if task_item.status == Tickets_Task.STATUS_OPEN and task_item.manage_uid == uid else False
        task_item.can_deleted = True if task_item.status == Tickets_Task.STATUS_OPEN and task_item.uid == uid else False
        tmp_idx += 1
        if task_item.status == Tickets_Task.STATUS_CLOSED:
            task_closed_counter += 1
    ticket_info.cname = user_mapping[ticket_info.uid].cn_name

    for history_item in history_info:
        history_item.uid_cname = user_mapping[history_item.uid].cn_name

    if task_closed_counter>0:
        tmp_idx = tmp_idx - 1
        tmp_percent = '%.0f%%'%(float(task_closed_counter)/float(tmp_idx) * 100)
        if task_closed_counter == tmp_idx:
            extend['ticket_tips'] = '已关闭'
        else:
            extend['ticket_tips'] = '%s%s'%('处理中&nbsp;',tmp_percent)
    else:
        extend['ticket_tips'] = '处理中'

    if uid == ticket_info.uid:
        extend['is_owner'] = True
    else:
        extend['is_owner'] = False

    ticket_info.opened = True if ticket_info.status == Tickets.STATUS_OPEN else False

    return render_template('/sa/tickets/detail.html',tasks = tasks, ticket = ticket_info ,extend = extend, history = history_info)


@tickets.route("/add",methods = ['GET','POST'])
@login_required
def add():
    if request.method == 'GET':
        tickets_cat_list = Tickets_Category.query.all()
        tickets_cat_dic = {}
        for cat_item in tickets_cat_list:
            tmp_name = cat_item.name if cat_item.name == cat_item.label else '%s-%s'%(cat_item.label,cat_item.name)
            tickets_cat_dic[cat_item.id] = {'name':tmp_name,'template':cat_item.template}
        return render_template('/sa/tickets/add.html',cats = json.dumps(tickets_cat_dic))
    code = 0
    msg = '添加成功'
    counter = 0
    catids = []
    contents = []
    email_uids = []
    if request.form.getlist('cat[]'):
        catids = request.form.getlist('cat[]')
        contents = request.form.getlist('content[]')
    for cat_item in catids:
        if int(cat_item)<1:
            code = 1
            msg = '请选择工单分类'
            break
        if len(contents[counter]) < 5:
            code = 1
            msg = '工单内容不能为空'
            break
        counter += 1
    if code > 0:
        return redirect(url_for('tickets.add',code = code, msg = msg))
    uid = current_user.id
    ticket_target = Tickets(uid = uid)
    db.session.add(ticket_target)
    db.session.commit()
    ticket_id = ticket_target.id
    counter = 0
    for cat_id in catids:
        tmp_ticket_cat_info = Tickets_Category.query.filter(Tickets_Category.id == cat_id).first()
        if tmp_ticket_cat_info:
            email_uids.append(tmp_ticket_cat_info.manage_uid)
            tmp_target = Tickets_Task(uid = uid , manage_uid = tmp_ticket_cat_info.manage_uid, tickets_id = ticket_id, tickets_cat_id = cat_id , content = contents[counter])
            db.session.add(tmp_target)
            db.session.commit()
        counter += 1
    #发送邮件
    tmp_email_name = ""
    user_info_mapping = get_user_info(uids = email_uids)
    for tmp_email_uid,tmp_user_info in user_info_mapping.items():
        tmp_email_name += '%s,'%tmp_user_info.cn_name
    tmp_email_name = tmp_email_name[:-1]
    subject = "【工单处理】%s 有工单任务啦!!"%tmp_email_name
    go_href = '%s%s'%(app.config.get('DOMAIN'),url_for('tickets.detail',id = ticket_id))
    content = "Hi %s:<br/><br/>%s提交了工单任务,<a href='%s'>请前去处理(详情)</a>"%(tmp_email_name,current_user.cn_name,go_href)
    addmail(app.config.get("MAIL_TO")['ops_email'], subject, content)
    return redirect(url_for('tickets.detail',id = ticket_id))

@tickets.route("/mod/<int:id>",methods = ['GET','POST'])
@login_required
def tickets_mod(id):
    uid = current_user.id
    if request.method == 'GET':
        cat_dic = {}
        uids = []
        tmp_idx = 1
        tickets_cat = []
        ticket_info = Tickets.query.filter(Tickets.id == id).first()
        if not ticket_info:
            return redirect(url_for('user.tickets'))
        if uid != ticket_info.uid:
            return redirect(url_for('user.tickets'))
        if ticket_info.status == Tickets.STATUS_CLOSED:
            return redirect(url_for('user.tickets'))

        tasks = Tickets_Task.query.filter(Tickets_Task.tickets_id == id).all()
        cat_list = Tickets_Category.query.all()
        if cat_list:
            for cat_item in cat_list:
                cat_dic[cat_item.id] = cat_item
                tmp_name = cat_item.name if cat_item.name == cat_item.label else '%s-%s'%(cat_item.label,cat_item.name)
                tickets_cat.append({'id':cat_item.id,'name':tmp_name})

        for task_item in tasks:
            uids.append(task_item.manage_uid)

        user_mapping = get_user_info(uids = uids)
        opened_task = []
        closed_task = []
        for task_item in tasks:
            task_item.idx = tmp_idx
            task_item.manage_cname = user_mapping[task_item.manage_uid].cn_name
            task_item.tickets_cat_name = cat_dic[task_item.tickets_cat_id].name
            if task_item.status == Tickets_Task.STATUS_CLOSED:
                closed_task.append(task_item)
            else:
                opened_task.append(task_item)
            tmp_idx += 1
        return render_template('/sa/tickets/mod.html',tasks = {'opened':opened_task,'closed':closed_task}, ticket = ticket_info , cats = tickets_cat)
    code = 0
    msg = '添加成功'
    counter = 0
    catids = []
    contents = []
    task_ids = []
    ticket_id = id
    if request.form.getlist('cat[]'):
        catids = request.form.getlist('cat[]')
        contents = request.form.getlist('content[]')
        task_ids = request.form.getlist('task_ids[]')

    for cat_item in catids:
        if int(cat_item)<1:
            code = 1
            msg = '请选择工单分类'
            break
        if len(contents[counter]) < 5:
            code = 1
            msg = '工单内容不能为空'
            break
        if task_ids[counter] < 1:
            code = 1
            msg = '任务ID没有,非法请求'
            break
        counter += 1
    ticket_info = Tickets.query.filter(and_(Tickets.uid == uid , Tickets.id == ticket_id)).first()
    if not ticket_info:
        code = 1
        msg = "此功能不存在"
    if code > 0:
        return redirect(url_for('tickets.mod',code = code, msg = msg))
    counter = 0
    for tmp_task_id in task_ids:
        tmp_cat_id = catids[counter]
        tmp_content = contents[counter]
        tmp_ticket_cat_info = Tickets_Category.query.filter(Tickets_Category.id == tmp_cat_id).first()
        if tmp_ticket_cat_info:
            tmp_tickets_task_info = Tickets_Task.query.filter(Tickets_Task.id == tmp_task_id).first()
            if tmp_tickets_task_info:
                tmp_tickets_task_info.tickets_cat_id = tmp_cat_id
                tmp_tickets_task_info.content = tmp_content
                db.session.commit()
        counter += 1
    return redirect(url_for('tickets.detail',id = ticket_id))

@tickets.route("/task/my/")
@login_required
def task_my():
    if not current_user.is_sa:
        return redirect("/")
    p = request.args.get('p',1)
    per_page = 50
    range_num = 10
    uid = current_user.id
    idx = 1
    cat_dic = {}
    uids = []
    cat_list = Tickets_Category.query.all()
    if cat_list:
        for cat_item in cat_list:
            cat_dic[cat_item.id] = cat_item
    ticket_tasks_target = Tickets_Task.query.filter(Tickets_Task.manage_uid == uid)
    total_num = ticket_tasks_target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    ticket_tasks = ticket_tasks_target.order_by(Tickets_Task.status).offset((int(p) - 1) * per_page).limit(per_page).all()
    for item in ticket_tasks:
        uids.append(item.uid)
    user_mapping = get_user_info(uids = uids)
    for item in ticket_tasks:
        item.idx = idx
        item.tickets_cat_name = cat_dic[item.tickets_cat_id].name if \
            cat_dic[item.tickets_cat_id].name == cat_dic[item.tickets_cat_id].label else \
            '%s-%s'%(cat_dic[item.tickets_cat_id].label,cat_dic[item.tickets_cat_id].name)
        item.uid_cname = user_mapping[item.uid].cn_name
        idx += 1
    extend = {
        'total':total_num,
        'cur_total':len(ticket_tasks)
    }
    return render_template('/sa/tickets/my.html',tasks = ticket_tasks , extend = extend, p = page)

@tickets.route("/task/mod",methods = ['POST'])
@login_required
def mod():
    code = 0
    msg = '关闭任务成功'
    uid = current_user.id
    type = request.form['type'].strip()
    task_id = request.form['task_id'].strip()
    if type == "close":
        task_info = Tickets_Task.query.filter(Tickets_Task.id == task_id).first()
        if not task_info:
            code = 1
            msg ='此任务不存在'
            return responsejson(code, msg)
        if task_info.manage_uid != uid:
            code = 1
            msg ='您没有关闭此任务的权限'
            return responsejson(code, msg)
        task_info.status = Tickets_Task.STATUS_CLOSED
        db.session.commit()
        __add_comments(uid = uid, tickets_id = task_info.tickets_id , content = '完成任务(Task ID:%s)'%task_id)
        tickets_opend_tasks_count = Tickets_Task.query.filter(and_(Tickets_Task.tickets_id == task_info.tickets_id,Tickets_Task.status == Tickets_Task.STATUS_OPEN )).count()
        if tickets_opend_tasks_count == 0:
            tickets_info = Tickets.query.filter(Tickets.id == task_info.tickets_id).first()
            tickets_info.status = Tickets.STATUS_CLOSED
            db.session.commit()
    elif type == "deleted":
        msg = '删除任务成功'
        task_info = Tickets_Task.query.filter(Tickets_Task.id == task_id).first()
        if not task_info:
            code = 1
            msg ='此任务不存在'
            return responsejson(code, msg)
        if task_info.uid != uid:
            code = 1
            msg ='您没有删除此任务的权限'
            return responsejson(code, msg)
        task_info.deleted = Tickets_Task.DELETED_YES
        task_info.status = Tickets_Task.STATUS_CLOSED
        db.session.commit()
        __add_comments(uid = uid, tickets_id = task_info.tickets_id , content = '删除并关闭任务(Task ID:%s)'%task_id)
        tickets_opend_tasks_count = Tickets_Task.query.filter(and_(Tickets_Task.tickets_id == task_info.tickets_id,Tickets_Task.status == Tickets_Task.STATUS_OPEN )).count()
        if tickets_opend_tasks_count == 0:
            tickets_info = Tickets.query.filter(Tickets.id == task_info.tickets_id).first()
            tickets_info.status = Tickets.STATUS_CLOSED
            db.session.commit()
    return responsejson(code, msg)




@tickets.route("/add/comments/<int:id>",methods = ['POST'])
@login_required
def add_comments(id):
    code = 0
    msg = '评论成功'
    uid = current_user.id
    tickets_id = id
    content = request.form['content'].strip()
    if len(content)<5:
        code = 1
        msg = "请输入评论,不少于5字节"
    else:
        __add_comments(uid = uid ,tickets_id = tickets_id, content = content)
    return responsejson(code, msg)

def __add_comments(uid = 0,tickets_id = 0, content = ''):
    target = Tickets_Comments(uid = uid,tickets_id = tickets_id ,content =content)
    db.session.add(target)
    db.session.commit()