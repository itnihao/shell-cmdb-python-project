# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from pypages import Paginator
from sqlalchemy import or_, and_, desc, extract
from models.user import User, Department,Group,Usergroupmap
from models.orders.orders import Orders
from models.orders.orders_task import Orders_Task
from models.orders.order_category import Order_Category
from models.orders.ordercat_type import Ordercat_Type
from models.orders.order_comments import Order_Comments
from views.functions import responsejson, addmail
from views.user import get_user_info
import datetime, json
import json as myjson
# import Tkinter
# import tkMessageBox

orders = Blueprint('orders', __name__)


@orders.route('/', )
@login_required
def index():
    return redirect(url_for('orders.my'))


@orders.route('/cat_list/<int:id>', methods=['GET', 'POST'])
@login_required
def cat_list(id):  # id=type_id
    type = Ordercat_Type.query.filter(Ordercat_Type.deleted==0).all()
    if id == 0:
        tic_cat = ''
        typeid = Ordercat_Type.query.first()
        if typeid:
            id = typeid.id
            tic_cat = Order_Category.query.filter_by(type_id=typeid.id).all()
    else:
        tic_cat = Order_Category.query.filter_by(type_id=id).all()
    if current_user.identity == 'ops':
        tic = Orders.query.filter(
            and_(Orders.approver_uid == current_user.id, Orders.status == 2)).all()  # 显示已认领，未处理的工单
    elif current_user.identity == 'leader':
        tic = Orders.query.filter(
            and_(Orders.approver_uid == current_user.id, Orders.status == 4)).all()  # 显示已认领，未处理的工单
    if tic != None:
        num = len(tic)
    else:
        num = 0
    return render_template('/orders/do_order.html', tic_cat=tic_cat, type=type, id=id, num=num)


@orders.route('/sub_order/<int:id>', methods=['GET', 'POST'])
@login_required
def sub_order(id):  # id=cat_id
    uid = current_user.id
    if request.method == 'POST':
        mod = request.form['mod']
        level = request.form['level']
        conts1 = request.form['conts']
        conts0 = json.loads(conts1)
        conts = conts0[0]
        co = json.dumps(conts, ensure_ascii=False, indent=2)

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if mod == 'sub':
            in_tic = Orders(category_id=id, uid=uid, status=5, content=co, level=level)  # , created=time, updated=time
            db.session.add(in_tic)

            # 发邮件
            leader_id = current_user.superior_id
            user_name = User.query.filter_by(id=leader_id).first()
            lemail = user_name.email  # 默认领导邮箱
            lname = user_name.cn_name
            subject = "【工单认领】%s 提交了新的工单!!" % current_user.cn_name
            go_href = '%s%s' % (app.config.get('DOMAIN'), url_for('orders.order_claim'))
            content = "Hi %s:<br/><br/>%s提交了工单任务,<a href='%s'>请前去处理(详情)</a>" % (lname, current_user.cn_name, go_href)
            addmail(lemail, subject, content)


        else:
            tid = request.form['tid']
            in_tic = Orders.query.filter_by(id=tid).first()
            in_tic.content = co
            in_tic.level = level
            in_tic.updated = time
        db.session.commit()

        msg = "提交成功"

        return app.response_class(json.dumps(msg), mimetype='application/json')
    else:
        tic_cat = Order_Category.query.filter_by(id=id).first()
        cat_dic = eval(tic_cat.cat_dec)  # json.loads
        if current_user.identity == 'ops':
            tic = Orders.query.filter(
                and_(Orders.approver_uid == current_user.id, Orders.status == 2)).all()  # 显示已认领，未处理的工单
        elif current_user.identity == 'leader':
            tic = Orders.query.filter(
                and_(Orders.approver_uid == current_user.id, Orders.status == 4)).all()  # 显示已认领，未处理的工单
        if tic != None:
            num = len(tic)
        else:
            num = 0
        return render_template('/orders/add_order.html', tic_cat=tic_cat, cat_dic=cat_dic, mod='sub', num=num)


@orders.route('/chg/<int:tid>', methods=['GET', 'POST'])
@login_required
def chg(tid):
    tic = Orders.query.filter_by(id=tid).first()
    cat_dic = eval(tic.content)  # json.loads
    cid = tic.category_id
    cat = Order_Category.query.filter_by(id=cid).first()
    cname = cat.name
    level = tic.level_desc
    tic_cat = {'id': cat.id, 'cname': cname, 'tid': tid, 'level': level}
    # tic_cat=json.loads(tic_cats)
    if current_user.identity == 'ops':
        tic = Orders.query.filter(
            and_(Orders.approver_uid == current_user.id, Orders.status == 2)).all()  # 显示已认领，未处理的工单
    elif current_user.identity == 'leader':
        tic = Orders.query.filter(
            and_(Orders.approver_uid == current_user.id, Orders.status == 4)).all()  # 显示已认领，未处理的工单
    if tic != None:
        num = len(tic)
    else:
        num = 0
    return render_template('/orders/sub_order.html', tic_cat=tic_cat, cat_dic=cat_dic, mod='chg', num=num)  #

@orders.route('/handling')
@login_required
def handling():
    p = int(request.args.get('p', 1))
    per_page = 10
    range_num = 10

    uid = current_user.id
    ident = current_user.identity

    id_name = {}
    user_ = User.query.all()
    for user in user_:
        id_name[user.id] = user.cn_name

    cat_id = {}
    cid_name = {}

    cat_ = Order_Category.query.all()
    for cat in cat_:
        cat_id[cat.id] = cat.uid
        cid_name[cat.id] = cat.name
    tic = None
    if ident == 'ops':
        tic = Orders.query.order_by(desc(Orders.id)).filter()
        tic = tic.filter(and_(Orders.approver_uid == uid, Orders.status == 3)).all()  # 显示已认领，未处理的工单
    elif ident == 'leader':
        tic= Orders.query.order_by(desc(Orders.id)).filter()
        tic = tic.filter(and_(Orders.approver_uid == uid, Orders.status == 1)).all()  # 显示已认领，未处理的工单
    if tic:
        total_num = len(tic)
        tic = tic[10 * (p - 1):10 * (p - 1) + 10]
        len_cur = len(tic)
    else:
        total_num = 0
        len_cur = 0
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    extend = {'total': total_num, 'current_page': len_cur}
    return render_template('/orders/order_handling.html', tic=tic,id_name=id_name, cat_id=cat_id,
                           cid_name=cid_name, extend=extend, p=page)


@orders.route('/order_claim')
@login_required
def order_claim():
    p = int(request.args.get('p', 1))
    per_page = 10
    range_num = 10

    uid = current_user.id
    ident = current_user.identity
    id_name = {}
    user_ = User.query.all()
    for user in user_:
        id_name[user.id] = user.cn_name

    cat_id = {}
    cid_name = {}

    cat_ = Order_Category.query.all()
    for cat in cat_:
        cat_id[cat.id] = cat.uid
        cid_name[cat.id] = cat.name
    tic=None
    if ident == 'ops' :
        tic = Orders.query.order_by(desc(Orders.id)).filter()
        tic = tic.filter(Orders.status == 2).all()  # 显示已提交，未认领的工单，所有运维人员都能看到
    elif ident == 'leader' :
        tic = Orders.query.order_by(desc(Orders.id)).filter()
        tic = tic.filter(and_(Orders.applier_uid.in_(current_user.user_list), Orders.status == 0)).all()  # 显示未认领的工单
    if tic:
       total_num = len(tic)
       tic = tic[10 * (p - 1):10 * (p - 1) + 10]
       len_cur = len(tic)
    else:
       total_num = 0
       len_cur = 0
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)

    extend = {'total': total_num, 'current_page': len_cur}
    return render_template('/orders/order_claim.html', tic=tic, id_name=id_name, cat_id=cat_id,
                           cid_name=cid_name, extend=extend, p=page)


@orders.route('/my')
@login_required
def my():
    ident = current_user.identity

    p = int(request.args.get('p', 1))
    per_page = 10
    range_num = 10

    uid = current_user.id

    id_name = {}
    # lead_id = {}
    user_ = User.query.all()
    for user in user_:
        id_name[user.id] = user.cn_name

    cat_id = {}
    cid_name = {}
    cat_ = Order_Category.query.all()
    for cat in cat_:
        cat_id[cat.id] = cat.uid
        cid_name[cat.id] = cat.name

    tic = Orders.query.order_by(desc(Orders.id)).filter()
    if ident == 'user':
        tic = tic.filter(Orders.applier_uid == uid).all()
    elif ident == 'ops':
        # tic = tic.filter(or_(Orders.approver_uid == uid, Orders.applier_uid == uid)).all()  # 显示已经认领的和自己提交的
        pag = tic.filter(or_(Orders.approver_uid == uid, Orders.applier_uid == uid)).paginate(p,per_page=per_page,error_out=False)
        plist=[]
        for pp in range(1,pag.pages+1):
            plist.append(pp)
        # pag.pages=plist
        tic= pag.items
    elif ident == 'leader':
        tic = tic.filter(or_(Orders.applier_uid.in_(current_user.user_list), Orders.applier_uid == uid)).all()  # 显示该领导下的所有员工提交的工单和自己提交的
    if tic:
        total_num = len(tic)
        # tic = tic[10 * (p - 1):10 * (p - 1) + 10]
        len_cur = len(tic)
    else:
        total_num = 0
        len_cur = 0
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    extend = {'total': total_num, 'current_page': len_cur}
    order = None

    return render_template('/orders/my_order.html', tic=tic, ident=ident, id_name=id_name, cat_id=cat_id,
                           cid_name=cid_name, extend=extend, p=pag,plist=plist)


@orders.route('/detail/<int:id>')
@login_required
def detail(id):
    uid = current_user.id

    user_sql = User.query.filter_by(id=uid).first()
    uname = user_sql.cn_name

    tic = Orders.query.filter_by(id=id).first()
    level = tic.level_desc
    approver_uid = tic.approver_uid
    cat_sql = Order_Category.query.filter_by(id=tic.category_id).first()  # id ,cname, mid
    cname = cat_sql.name

    id_name = {}
    user_ = User.query.all()
    for user in user_:
        id_name[user.id] = user.cn_name

    hander_name = id_name[approver_uid]

    info_dic = {'id': id, 'uname': uname, 'hander_name': hander_name, 'cname': cname, 'level': level,
                'status': tic.status_desc, 'title': tic.title,
                'update': str(tic.updated)}  # 'state':status_dic[tic.status],
    cont_dic = eval(tic.content)  # json.loads(tic.content)

    task = Orders_Task.query.filter_by(tickets_id=id).all()  # 工单任务
    comment = Order_Comments.query.filter_by(order_id=id).all()  # 工单评论

    return render_template('/orders/order_detail.html', cont_dic=cont_dic, info_dic=info_dic, task=task,
                           id_name=id_name, comment=comment)


@orders.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    category_info = Order_Category.query.filter(Order_Category.deleted == 0).all()
    if not current_user.is_sa:
        return redirect(url_for('orders.index'))  # "/"
    # p = request.args.get('p', 1)
    # per_page = 20
    # range_num = 10

    cat_dic = {}
    user_dic = {}
    mname = {}
    cat_sql = Order_Category.query.all()  # id ,cname, mid
    for item in cat_sql:
        cat_dic[item.id] = item.name
        mname[item.id] = item.uid

    user_sql = User.query.all()  # id, uname
    for it in user_sql:
        user_dic[it.id] = it.cn_name

    tickets = Orders.query.order_by(desc(Orders.id)).filter()
    tickets = tickets.filter(Orders.status > 2).all()  # # tickets = Orders.query.order_by(desc(Orders.id)).filter()

    # total_num = len(tickets)
    # page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    # tickets_info = tickets[20 * (p - 1):20 * (p - 1) + 20]
    # len_cur = len(tickets_info)
    # extend = {'total': total_num, 'current_page': len_cur}
    current_page = 1
    all_page = 1
    all_count = len(tickets)
    if all_count > 10:
        all_page = all_count / 10
        if (all_count % 10) > 0:
            all_page += 1
        tickets = tickets[0:10]

    return render_template('/orders/order_list.html', tickets=tickets, cat_dic=cat_dic, user_dic=user_dic,
                           mname=mname, current_page=current_page, all_page=all_page,
                           category_info=category_info)  # ,status_dic=status_dic extend=extend, p=page,


@orders.route('/search', methods=['GET', 'POST'])  # /<search>search
@login_required
def search():
    if not current_user.is_sa:
        return redirect("/")
    # if  request.method == 'POST':
    search = request.form['search']
    search = json.loads(search)

    tickets = Orders.query.order_by(desc(Orders.id)).filter()
    tickets = tickets.filter(Orders.status > 2)
    if search['catname']:
        tic_cat = Order_Category.query.filter(Order_Category.name.contains('%' + str(search['catname']) + '%')).all()
        id = []
        for tic in tic_cat:
            id.append(tic.id)
        tickets = tickets.filter(Orders.category_id.in_(id))

    if search['creater']:
        user_name = User.query.filter(User.cn_name.contains('%' + str(search['creater']) + '%')).all()
        uid = []
        for user in user_name:
            uid.append(user.id)
        tickets = tickets.filter(Orders.applier_uid.in_(uid))

    if search['handler']:
        user_hname = User.query.filter(User.cn_name.contains('%' + str(search['handler']) + '%')).all()
        hid = []
        for huser in user_hname:
            hid.append(huser.id)
        tickets = tickets.filter(Orders.approver_uid.in_(hid))

    if search['state']:
        if int(search['state']) != 100:
            tickets = tickets.filter(Orders.status == int(search['state']))

    if search['starttime']:
        starttime = datetime.datetime.strptime(search['starttime'], '%Y-%m-%d')
        tickets = tickets.filter(extract('year', Orders.created) >= starttime.year,
                                 extract('month', Orders.created) >= starttime.month,
                                 extract('day', Orders.created) >= starttime.day)

    if search['endtime']:
        starttime = datetime.datetime.strptime(search['endtime'], '%Y-%m-%d')
        tickets = tickets.filter(extract('year', Orders.updated) <= starttime.year,
                                 extract('month', Orders.updated) <= starttime.month,
                                 extract('day', Orders.updated) <= starttime.day)

    cat_dic = {}
    user_dic = {}
    mname = {}
    cat_sql = Order_Category.query.all()  # id ,cname, mid
    for item in cat_sql:
        cat_dic[item.id] = item.name
        mname[item.id] = item.uid

    user_sql = User.query.all()  # id, uname
    for it in user_sql:
        user_dic[it.id] = it.cn_name

    tickets = tickets.all()
    mod=request.form['mod']
    if mod=="search":
        current_page=1
        all_page_s=1
        all_count = len(tickets)
        if all_count > 10:
            all_page_s = all_count / 10
            if (all_count % 10) > 0:
                all_page_s += 1
            tickets = tickets[0:10]
    else:
        current_page = int(request.form.get('current_page'))
        all_page = int(request.form.get('all_page'))
        all_page_s = 1
        all_count = len(tickets)
        if all_count > 10:
            all_page_s = all_count / 10
            if (all_count % 10) > 0:
                all_page_s += 1
        if (all_page_s > current_page):
            tickets = tickets[(current_page - 1) *10:current_page * 10]
        elif (all_page == current_page):
             tickets = tickets[(current_page - 1) * 10:]

    order = []
    for item in tickets:
        order.append(serialize(item))

    return app.response_class(json.dumps(
        {'tickets': order, 'cat_dic': cat_dic, 'user_dic': user_dic, 'mname': mname, 'current_page': current_page,
         'all_page': all_page_s}), mimetype='application/json')
    # return render_template('/orders/order_list.html', tickets=tickets_info, cat_dic=cat_dic, user_dic=user_dic,'extend': extend,'p':s_page,
    #                        mname=mname, extend=extend, p=page, num=num)


def serialize(order):  # applier_uid = 0,status = 0,approver_uid=0,category_id=0,level=0,created = '',content='',title='',deleted=0
    list = {}
    list['id'] = order.id
    list['applier_uid'] = order.applier_uid
    list['status'] = order.status
    list['approver_uid'] = order.approver_uid
    list['category_id'] = order.category_id
    list['level'] = order.level
    list['created'] = str(order.created)
    list['content'] = order.content
    list['title'] = order.title
    list['deleted'] = order.deleted
    list['updated'] = str(order.updated)
    return list


def serialize_p(page):
    p = {}
    p['page_num'] = page.page_num
    p['current'] = page.current
    p['end'] = page.end
    p['has_next'] = page.has_next
    p['has_previous'] = page.has_previous
    p['next'] = page.next
    p['object_num'] = page.object_num
    p['pages'] = page.pages
    p['per_page'] = page.per_page
    p['previous'] = page.previous
    p['range_num'] = page.range_num
    p['start'] = page.start
    return p


@orders.route('/mod', methods=['GET', 'POST'])
@login_required
def mod():
    uid = current_user.id
    type = request.form['type']
    tic_id = request.form['tic_id']
    code = 0
    tic = Orders.query.filter_by(id=tic_id).first()
    if not tic:
        msg = '此任务不存在'
        code = 1
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if type == 'close':  # status={0：‘待认领’，1:'评估中',2:'已提交',3:'处理中',4:'已完成',5:'已驳回'}
        msg = '任务完成'
        tic.status = 4
        tic.approver_uid = uid
        tic.updated = time
        db.session.commit()

        task = Orders_Task(tickets_id=tic_id, uid=uid, operation='关闭工单')
        # db.session.add(task)
        # db.session.commit()

        # 发送邮件
        u_name = User.query.filter_by(id=tic.applier_uid).first()
        uname = u_name.cn_name  # 工单提交者
        email = u_name.email
        subject = "【工单关闭】"
        go_href = '%s%s' % (app.config.get('DOMAIN'), url_for('orders.detail', id=tic_id))
        content = "Hi %s:<br/><br/>您提交的工单已处理完毕,<a href='%s'>查看详情</a>" % (uname, go_href)
        addmail(email, subject, content)

    elif type == 'claim':
        msg = '任务已认领'
        if current_user.identity == 'leader':
            tic.status = 1
        else:
            tic.status = 3
        tic.approver_uid = uid
        tic.updated = time
        db.session.commit()

        task = Orders_Task(tickets_id=tic_id, uid=uid, operation='认领工单')
        # db.session.add(task)
        # db.session.commit()
    elif type == 'del':
        msg = '任务已删除'
        tic.approver_uid = uid
        tic.status = 4
        tic.deleted = 1
        tic.updated = time
        db.session.commit()

        task = Orders_Task(tickets_id=tic_id, uid=uid, operation='删除工单')
        # db.session.add(task)
        # db.session.commit()

    elif type == 'sub':
        msg = '任务已提交，ops待认领'
        tic.approver_uid = uid
        tic.status = 2
        tic.updated = time
        db.session.commit()

        task = Orders_Task(tickets_id=tic_id, uid=uid, operation='提交工单')
        # db.session.add(task)
        # db.session.commit()

        # 发送群邮件
        order_cat = Order_Category.query.filter_by(id=tic.category_id).first()
        mid = order_cat.uid
        user_name = User.query.filter_by(id=mid).first()
        mname = user_name.cn_name  # 默认处理人
        u_name = User.query.filter_by(id=tic.applier_uid).first()
        uname = u_name.cn_name  # 工单提交者
        subject = "【工单认领】%s 有工单任务啦!!" % mname
        go_href = '%s%s' % (app.config.get('DOMAIN'), url_for('orders.order_claim'))
        content = "Hi :<br/><br/>%s提交了工单任务,<a href='%s'>请前去认领(详情)</a>" % (uname, go_href)
        addmail(app.config.get("MAIL_TO")['ops_email'], subject, content)

    elif type == 'reject':
        msg = '任务已驳回'
        tic.approver_uid = uid
        tic.status = 5
        tic.updated = time
        db.session.commit()

        task = Orders_Task(tickets_id=tic_id, uid=uid, operation='驳回工单')
        # db.session.add(task)
        # db.session.commit()

        # 发送邮件
        u_name = User.query.filter_by(id=tic.applier_uid).first()
        uname = u_name.cn_name  # 工单提交者
        email = u_name.email
        subject = "【工单驳回】"
        go_href = '%s%s' % (app.config.get('DOMAIN'), url_for('orders.detail', id=tic_id))
        content = "Hi %s:<br/><br/>您提交的工单已被驳回,<a href='%s'>可查看详情</a>" % (uname, go_href)
        addmail(email, subject, content)

    else:  # type='comment'
        content = request.form['content']
        msg = '评论成功'
        task = Order_Comments(order_id=tic_id, uid=uid, content=content)

    db.session.add(task)
    db.session.commit()
    return app.response_class(json.dumps(msg), mimetype='application/json')


@orders.route('/add')
@login_required
def add():
    order_type = Ordercat_Type.query.filter(Ordercat_Type.deleted==0).all()
    order_category = Order_Category.query.filter(Order_Category.deleted == 0).all()
    return render_template('/orders/do_order.html', type_name=order_type, order_category=order_category)


@orders.route('/deleted/<int:id>', methods=['POST', 'GET'])
@login_required
def deleted(id):
    category_info = Order_Category.query.filter(Order_Category.id == id).first()
    category_info.deleted = 1
    db.session.commit()
    return redirect(url_for('orders.add'))

@orders.route('/type_deleted/<int:id>', methods=['POST', 'GET'])
@login_required
def type_deleted(id):
    type_info = Ordercat_Type.query.filter(Ordercat_Type.id == id).first()
    category_info = Order_Category.query.filter(and_(Order_Category.type_id == id,Order_Category.deleted==0)).all()
    if category_info:
        return app.response_class(json.dumps({'code': 1, 'msg': '该工单类型下有工单分类请首先移除后删除!'}), mimetype='application/json')
    type_info.deleted = 1
    db.session.commit()
    return app.response_class(json.dumps({'code': 0, 'msg': '删除成功'}), mimetype='application/json')

@orders.route('/get_detailtype/<int:id>',methods=['POST','GET'])
@login_required
def get_detailtype(id):
    type_info = Ordercat_Type.query.filter(and_(Ordercat_Type.deleted==0,Ordercat_Type.id==id)).first()
    type_name = type_info.name
    return app.response_class(json.dumps({'code': 0,'data':type_name }), mimetype='application/json')

@orders.route('/edit_type/<int:id>',methods=['POST','GET'])
@login_required
def edit_type(id):
    msg="修改成功"
    category_info = Order_Category.query.filter(and_(Order_Category.deleted==0,Order_Category.type_id==id)).all()
    type_info = Ordercat_Type.query.filter(and_(Ordercat_Type.deleted==0,Ordercat_Type.id==id)).first()
    move_typename = request.form['type_name']
    move_typeid=int(request.form['move_typeid'])
    # type_info.name = move_typename
    for item in category_info:
        item.type_id = move_typeid
        # db.session.commit()
    db.session.commit()
    return app.response_class(json.dumps({'code': 0,'msg':msg }), mimetype='application/json')

@orders.route('/edit_category/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_category(id):
    category_info = Order_Category.query.filter(Order_Category.id == id).first()
    target_info = Ordercat_Type.query.filter(Ordercat_Type.deleted==0).all()
    category_name = category_info.name
    uid = category_info.uid
    approver = User.query.filter(User.id == uid).first().cn_name
    type_id = category_info.type_id
    category_dec = eval(category_info.dec)
    dec = eval(category_info.dec)
    if request.method == "POST":
        category_name = request.form['category_name']
        type_id = request.form['select_type']
        user_id = request.form['user_id']
        data_label = request.form.getlist('data_label')
        data_content = request.form.getlist('data_content')
        input_type = request.form.getlist('input_type[]')
        for i in data_label:
            a = i.split(',')
        for j in data_content:
            b = j.split(',')
        # dec = dict(zip(a,b))

        dec = []
        for i in range(0, len(a)):
            c = {'label': a[i], 'content': b[i], 'input_type': input_type[i]}
            dec.append(c)
        category_info.name = category_name
        category_info.type_id = type_id
        category_info.uid = user_id
        category_info.dec = '%s'%dec
        db.session.commit()
        return app.response_class(json.dumps({'code': 0, 'msg': '修改成功'}), mimetype='application/json')
    return render_template('/orders/add_category.html',category_dec=category_dec,target_info = target_info,target=2,category_id=id,category_name=category_name,dec=dec,approver=approver,uid=uid,type_id=type_id)


@orders.route('/add_type', methods=["GET", "POST"])
@login_required
def add_type():
    type_info = Ordercat_Type.query.filter(Ordercat_Type.deleted ==0).all()
    if request.method == "POST":
        type_name = request.form['type_name']
        type = Ordercat_Type.query.filter(and_(Ordercat_Type.deleted ==0,Ordercat_Type.name==type_name)).all()
        if type:
            return app.response_class(json.dumps({'code': 1, 'msg': '工单类型已存在'}),mimetype='application/json')
        ticket_target = Ordercat_Type(name=type_name)
        db.session.add(ticket_target)
        db.session.commit()
        return app.response_class(json.dumps({'code': 0, 'msg': '提交成功'}), mimetype='application/json')
    return render_template('/orders/add_type.html',type_info=type_info,tatget=1)


@orders.route('/add_category', methods=["GET", "POST"])
@login_required
def add_category():
    target_info = Ordercat_Type.query.filter(Ordercat_Type.deleted==0).all()
    if request.method == "POST":
        category_name = request.form['category_name']
        type_id = request.form['select_type']
        user_id = request.form['user_id']
        data_label = request.form.getlist('data_label')
        data_content = request.form.getlist('data_content')
        input_type = request.form.getlist('input_type[]')
        category_info = Order_Category.query.filter(and_(Order_Category.deleted==0,Order_Category.name==category_name,Order_Category.type_id==type_id)).all()
        if category_info:
            return app.response_class(json.dumps({'code': 1, 'msg': '工单分类已存在'}), mimetype='application/json')
        for i in data_label:
            a = i.split(',')
        for j in data_content:
            b = j.split(',')
        # dec = dict(zip(a,b))

        dec = []
        for i in range(0, len(a)):
            c = {'label': a[i], 'content': b[i], 'input_type': input_type[i]}
            dec.append(c)
        target = Order_Category(name=category_name, type_id=type_id, uid=user_id, dec='%s' % dec)
        db.session.add(target)
        db.session.commit()
        return app.response_class(json.dumps({'code': 0, 'msg': '提交成功'}), mimetype='application/json')
    return render_template('/orders/add_category.html', target_info=target_info,target=1)


@orders.route('/do_order/<int:id>', methods=["GET", "POST"])
@login_required
def do_order(id):
    category_info = Order_Category.query.filter(Order_Category.id == id).first()
    category_name = category_info.name
    category_uid = category_info.uid
    category_typid = category_info.type_id
    category_dec = eval(category_info.dec)
    for item in category_dec:
        if int(item['input_type'])==3:
            item['content']=item['content'].split(";")
    return render_template('/orders/sub_order.html', category_name=category_name, category_uid=category_uid,
                           category_typid=category_typid, category_dec=category_dec, category_id=id)


@orders.route('/order_detail', methods=["GET", "POST"])
@login_required
def order_detail():
    if request.method == "POST":
        status = 0
        deleted = 0
        applier_uid = current_user.id
        category_id = request.form['category_id']
        category_uid = request.form['category_uid']
        order_title = request.form['order_title']
        order_level = request.form['order_level']
        mail_list = request.form.getlist('mail_list[]')
        label_list = request.form.getlist('label_list[]')
        content_list = request.form.getlist('content_list[]')
        content = str(dict(zip(label_list, content_list)))

        usergroup_info=Usergroupmap.query.filter_by(user_id=applier_uid).first()
        if usergroup_info:
            group_id=usergroup_info.group_id
            group_info=Group.query.filter_by(id=group_id).first()
            if group_info:
                department_id=group_info.department_id
                department_info=Department.query.filter_by(id=department_id).first()
        approver_email=""       # 默认领导邮箱
        if department_info:
            approver_uid=department_info.leader_uid  #默认领导
            leader_info1=User.query.filter_by(id=department_info.leader_uid).first()
            approver_email+=leader_info1.email + ";"
            leader_info2=User.query.filter_by(id=department_info.bleader_uid).first()
            approver_email+=leader_info2.email + ";"

        target = Orders(category_id=category_id, title=order_title, applier_uid=applier_uid, approver_uid=approver_uid,
                        content=content, level=order_level, status=status, deleted=deleted)
        db.session.add(target)
        db.session.commit()
        # user_info = User.query.filter(User.id == category_uid).first()
        subject = "【工单认领】%s 提交了新的工单!!" % current_user.cn_name
        go_href = '%s%s' % (app.config.get('DOMAIN'), url_for('orders.order_claim'))
        content = "Hi:<br/><br/>%s提交了工单任务,<a href='%s'>请前去处理(详情)</a>" % (current_user.cn_name, go_href)
        addmail(approver_email, subject, content)
        return app.response_class(json.dumps({'code': 0, 'msg': '提交成功'}), mimetype='application/json')


@orders.route('/user/autocomplete', methods=["GET", "POST"])
@login_required
def user_search():
    q = request.form['q'] + '%'
    print "============="
    print q
    result = []
    user_list = User.query.filter(or_(User.name.like(q),User.cn_name.like(q))).limit(12).all()
    for item in user_list:
        result.append({"id": item.id, "name": item.name, "cn_name": item.cn_name})
    return app.response_class(json.dumps(result), mimetype='application/json')


@orders.route('/user/tokeninput', methods=["GET", "POST"])
@login_required
def tokeninput():
    q = '%' + request.args.get('q') + '%'
    result = []
    user_list = User.query.filter(User.name.like(q)).limit(12).all()
    for item in user_list:
        result.append({"id": item.id, "name": item.name, "mail": item.email})
    return app.response_class(json.dumps(result), mimetype='application/json')


@orders.route('/numbers', methods=["GET", "POST"])
@login_required
def numbers():
    if current_user.identity == 'leader':
        tmp_claim = 0
        tmp_handling = 1
    elif current_user.identity == 'ops':
        tmp_claim = 2
        tmp_handling = 3
    else:
        tmp_claim = 100
        tmp_handling = 100
    wait_claim_number = Orders.query.filter(Orders.status == tmp_claim).count()
    wait_do_number = Orders.query.filter(and_(Orders.status == tmp_handling,Orders.approver_uid == current_user.id)).count()
    result = {"wait_claim_number": wait_claim_number, "wait_do_number": wait_do_number}
    return app.response_class(json.dumps(result), mimetype='application/json')

@orders.route("/getuser",methods=['GET', 'POST'])
@login_required
def getuser():
     all_dep=Department.query.all()
     # all_dep=DepartmentSchema(many=True).dump(all_dep).data

     jsonval=[]
     for d in all_dep:
         d_add={'id':d.id,'text': d.name,'href': '#'+d.name,'tags': ['0'],'nodes':[],'level':1}
         for w in d.group:
             g_add=({'id':w.id,'text': w.name,'href': '#'+w.name,'tags': ['0'],'nodes':[],'level':2})
             for u in w.Usergroupmaps:
                 u_add={'id':u.user.id,'text': u.user.cn_name+'@'+u.user.name,'href': '#'+u.user.name,'tags': ['0'],'nodes':[],'level':3}
                 g_add['nodes'].append(u_add)
             g_add['tags'][0]=str(len(g_add['nodes']))
             d_add['nodes'].append(g_add)


         d_add['tags'][0]=str(len(d_add['nodes']))
         jsonval.append(d_add)

     return app.response_class(json.dumps(jsonval), mimetype='application/json')
