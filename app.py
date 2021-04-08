import re
import time
import main as A
import main_sql
from IP import get_ip
from threading import Thread
from multiprocessing import Process, Pool
from flask import Flask, request, render_template

# 创建Flask实例
app = Flask(__name__)


# 配置访问路由
# @app.route('/')
# def hello():
#     return "hello world"

# @app.route('/login')
# def info():
#     username = request.values.get("username")
#     password = request.values.get("password")
#
#     return f"username: {username}<br>password: {password}<br>"+测试文件.get_data(username+password)


@app.route('/')
def login():
    ip = request.remote_addr
    UA = request.headers.get("User-Agent")
    info = get_ip(ip)
    write_log(f"\n{get_time()}\n[IP] {ip}\n[IF] {' '.join(info)}\n[UA] {UA}")
    if info[0] != "中国" or not UA or re.findall(r'spider', UA, re.I) or re.findall(r'python', UA, re.I):
        return render_template('404.html'), 404
    # cookie = request.cookies
    # print(f"cookie = {cookie}")
    # main_sql.del_table('none')
    return render_template('index_BDY.html')


def get_time():
    tim = time.strftime("> %Y-%m-%d %H:%M:%S", time.localtime())
    return tim


def write_log(message):
    try:
        print(message)
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(message+'\n')
    except:
        print("[ERROR] Error_log")


@app.route('/404')
def error():
    return render_template('404.html')


@app.route('/ajax')
def ajax():
    keyword = request.values.get("keyword")
    tabnum = request.values.get("tabnum")

    if tabnum:
        if __name__ == '__main__':
            tabnum = keyword + '_' + tabnum
            print(f"ajax-tabNum {tabnum}")
            # data = get_data(tabnum)
            data = pool.apply_async(get_data, args=(tabnum,)).get()
            return data


def get_data(tabnum):
    result = main_sql.search_data(tabnum)
    data = []
    try:
        if result:
            for row in result:
                data.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    except:
        pass

    return str(data)


@app.route('/research')
def bdy():
    keyword = request.values.get("keyword")
    tabnum = request.values.get("tabnum")
    if tabnum:
        print(f"research-tabNum {tabnum}")
        print(f"research-keyword {keyword}")

        if __name__ == '__main__':
            # A.bdy(keyword, tabnum)
            t = Process(target=A.bdy(keyword, tabnum).main)
            t.start()
            t.join()

    return render_template('index_BDY.html')


if __name__ == '__main__':
    pool = Pool()
    # pool2 = Pool()
    # sql_init(1) CREATE DATABASE IF NOT EXISTS
    # sql_init(0) DROP DATABASE IF EXISTS AND CREATE DATABASE
    main_sql.sql_init(1)
    t_ = Thread(target=main_sql.del_rep_table)
    t_.start()
    app.run(host='127.0.0.1', port=2333, processes=True, debug=True)
