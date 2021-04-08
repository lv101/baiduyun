# -*- coding: UTF-8 -*-
import re
import time
import schedule
from pymysql import *


def connection():
    # 连接数据库
    db = connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    print("数据库连接成功！")
    cur = db.cursor()

    return db, cur


def table_head(table_name):

    return f"CREATE TABLE {table_name}(" \
            "ID INT(11) NOT NULL AUTO_INCREMENT," \
            "文件名 VARCHAR(360) NOT NULL," \
            "文件类型 VARCHAR(10) NOT NULL," \
            "文件大小 VARCHAR(10) NOT NULL," \
            "文件格式 VARCHAR(20) NOT NULL," \
            "资源链接 VARCHAR(200) NOT NULL," \
            "PRIMARY KEY (ID)" \
            ")ENGINE=INNODB DEFAULT CHARSET=utf8mb4"


def table(tabnum):
    if not tabnum:
        return

    global table_name
    table_name = 'bdy_' + str(tabnum)

    set_table(table_name)


def set_table(table_name):
    '''
    新建表格
    :param sql: 表格头内容
    :return: None
    '''
    try:
        db, cur = connection()
        # 创建表单项
        print(table_name)
        cur.execute("DROP TABLE IF EXISTS " + table_name + ";")
        print("表格创建成功！")
        # 创建表格头内容
        cur.execute(table_head(table_name))
        print("表格头创建成功！")
    except Error:
        print("表格头创建失败：" + str(Error))
        db.rollback()


def del_table(table_name):
    '''
    删除表格
    :return: None
    '''
    try:
        db, cur = connection()

        # sql = "DROP TABLE IF EXISTS " + f"bdy_{table_name};"
        sql = "DROP TABLE IF EXISTS " + table_name
        cur.execute(sql)
        print("表格删除成功！")
    except Error:
        print("表格删除失败：" + str(Error))
        db.rollback()


def show_table(flag):
    '''
    查询所有表格并去重
    :return: None
    '''
    try:
        db, cur = connection()

        # tables = cur.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{DBNAME}' AND TABLE_TYPE='BASE TABLE';")
        cur.execute(f"SHOW TABLES;")
        tables = cur.fetchall()
        tabs = []

        for tab in tables:
            tab_ = tab[0].split('_')[1]
            # tabs.append({"oldName": tab[0], "newName": tab_, "flag": 0})
            tabs.append([tab[0], tab_, '0'])
        tabs = sorted(tabs, key=lambda x: x[1], reverse=False)

        count = len(tabs)
        index = 0
        while (count):
            try:
                for i in range(len(tabs) - 1, index, -1):
                    for j in range(i):
                        if re.findall(tabs[index][1], tabs[i][1]):
                            tabs[i][2] = '1'
                            # del datas[i]
                            break
                index += 1
                count -= 1
            except:
                count -= 1
        # print(datas)
        if not flag:
            for tab in tabs:
                if tab[2] == '1':
                    del_table(tab[0])
        # for tab in tabs:
        #     print(tab[0])
        print("表格查询&去重成功！")
    except Error:
        print("表格查询&去重失败：" + str(Error))
        db.rollback()


def del_rep_table():
    schedule.every().monday.at("08:00").do(show_table, 0)
    while True:
        schedule.run_pending()
        time.sleep(1)


def insert_data(table_name, value):
    '''
    向表格插入数据
    :param value: 插入的值
    :return: None
    '''
    try:
        if not table_name:
            return

        db, cur = connection()

        sql = "INSERT INTO " + f"bdy_{table_name}" + f"{head_name} VALUE {value}"
        cur.execute(sql)
        db.commit()
        print("数据插入成功！")
    except Error:
        print("数据插入失败：" + str(Error))
        db.rollback()


def search_data(table_name):
    '''
    查询数据
    :return: 表格中的数据
    '''
    try:
        if not table_name:
            return

        db, cur = connection()

        sql = "SELECT * FROM " + f"bdy_{table_name};"
        cur.execute(sql)
        result = cur.fetchall()
        print("数据查询成功！")
        return result
    except Error:
        print("数据查询失败：" + str(Error))
        db.rollback()


def update_data(type, value):
    '''
    更新数据
    :param type: 选中表格中的数据类型
    :param value: 要更新的数据
    :return: None
    '''
    try:
        db, cur = connection()

        global table_name
        sql = "UPDATE " + table_name + f" SET {type}=%s WHERE {type}=%s"
        cur.execute(sql, value)
        db.commit()
        print("数据更新成功！")
    except Error:
        print("数据更新失败：" + str(Error))
        db.rollback()


def del_data(type, value):
    '''
    删除表格中的数据
    :param type: 选中表格中的数据类型
    :param value: 要删除的数据
    :return: None
    '''
    try:
        db, cur = connection()

        global table_name
        sql = "DELETE FROM " + table_name + f" WHERE {type}=%s"
        cur.execute(sql, value)
        db.commit()
        print("数据删除成功！")
    except Error:
        print("数据删除失败：" + str(Error))
        db.rollback()


DBHOST = "DBHOST"
DBUSER = "DBUSER"
DBPASS = "DBPASS"
DBNAME = "DBNAME"

head_name = "(文件名, 文件类型, 文件大小, 文件格式, 资源链接)"


def sql_init(flag):
    # 连接数据库
    cur = connect(host=DBHOST, user=DBUSER, password=DBPASS, charset='utf8mb4').cursor()
    if flag:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DBNAME}")
    else:
        cur.execute(f"DROP DATABASE IF EXISTS {DBNAME}")
        cur.execute(f"CREATE DATABASE {DBNAME}")
    print("数据库创建成功！")
