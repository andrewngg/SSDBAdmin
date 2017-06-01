#!/usr/bin/env python
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from SSDBAdmin import app
from flask import render_template, request, make_response, redirect, url_for

from SSDBAdmin.model.ssdb_admin import SSDBObject
from SSDBAdmin.util import get_paging_tabs_info


@app.route('/ssdbadmin/queue/')
def queue_lists():
    """
    return queue list
    :return:
    """
    page_num = int(request.args.get('page_num', 1))
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    start = request.args.get('s', '')
    end = request.args.get('e', '')
    ssdb_object = SSDBObject(request)
    queue_list, has_next = ssdb_object.queue_list(start=start, end=end, page_num=page_num, page_size=int(page_size))
    select_arg = {'s': start, 'e': end, 'page_size': int(page_size)}
    resp = make_response(render_template('queue_list.html', queue_list=queue_list, has_next=has_next,
                                         page_num=page_num, select_arg=select_arg, active='queue'))
    return resp


@app.route('/ssdbadmin/queue/qpush/', methods=['GET', 'POST'])
def queue_qpush():
    """
    add item to queue
    :return:
    """
    if request.method == 'GET':
        queue_name = request.args.get('n')
        return render_template('queue_qpush.html', queue_name=queue_name, active='queue')
    else:
        queue_name = request.form.get('queue_name')
        push_type = request.form.get('type')
        item = request.form.get('item')
        ssdb_object = SSDBObject(request)
        ssdb_object.queue_qpush(queue_name, item, push_type)
        return redirect(url_for('queue_lists'))


@app.route('/ssdbadmin/queue/qpop/', methods=['GET', 'POST'])
def queue_qpop():
    """
    pop item from queue
    :return:
    """
    if request.method == 'GET':
        queue_name = request.args.get('n')
        return render_template('queue_qpop.html', queue_name=queue_name, active='queue')
    else:
        queue_name = request.form.get('n')
        pop_type = request.form.get('t')
        number = request.form.get('num')
        ssdb_object = SSDBObject(request)
        ssdb_object.queue_qpop(queue_name, number, pop_type)
        return redirect(url_for('queue_lists'))


@app.route('/ssdbadmin/queue/qrange/')
def queue_qrange():
    queue_name = request.args.get('n')
    page_num = request.args.get('page_num', 1)
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    ssdb_object = SSDBObject(request)
    item_total = ssdb_object.queue_size(queue_name)
    page_count, page_num = get_paging_tabs_info(item_total, page_num, page_size)
    offset = (page_num - 1) * int(page_size)
    item_list = ssdb_object.queue_qrange(queue_name, offset=offset, limit=page_size)
    select_arg = {'page_size': int(page_size)}
    resp = make_response(render_template('queue_qrange.html',
                                         item_list=item_list,
                                         name=queue_name,
                                         page_num=int(page_num),
                                         page_count=page_count,
                                         select_arg=select_arg,
                                         start_index=offset,
                                         data_total=item_total,
                                         active='queue'))
    resp.set_cookie('SIZE', str(page_size))
    return resp


@app.route('/ssdbadmin/queue/qget/')
def queue_qget():
    queue_name = request.args.get('n')
    index = request.args.get('i')
    ssdb_object = SSDBObject(request)
    item = ssdb_object.queue_qget(queue_name, index)
    return render_template('queue_qget.html', name=queue_name, item=item, index=index, active='queue')
