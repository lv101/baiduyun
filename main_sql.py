# -*- coding: UTF-8 -*-
from pymysql import *


def connection():
    # 连接数据库
    db = connect(DBHOST, DBUSER, DBPASS, DBNAME)
    print("数据库连接成功！")
    cur = db.cursor()

    return db, cur


def table_head(table_name):

    return f"CREATE TABLE {table_name}(" \
            "ID INT(11) NOT NULL AUTO_INCREMENT," \
            "文件名 VARCHAR(30) NOT NULL," \
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

        sql = "DROP TABLE IF EXISTS " + f"bdy_{table_name};"
        cur.execute(sql)
        print("表格删除成功！")
    except Error:
        print("表格删除失败：" + str(Error))
        db.rollback()


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

        sql = "SELECT * FROM " + f"bdy_{table_name}"
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


DBHOST = "localhost"
DBUSER = "root"
DBPASS = "123456"
DBNAME = "dbbdy"

# 连接数据库
db, cur = connection()

cur.execute(f"DROP DATABASE IF EXISTS {DBNAME}")
cur.execute(f"CREATE DATABASE {DBNAME}")
print("数据库创建成功！")

head_name = "(文件名, 文件类型, 文件大小, 文件格式, 资源链接)"

# insert_data("bdy_1", ('name', '种子文件', '1000GB', '.torrent', 'http://panbaidu.123456.com'))
# search_data('bdy_1')
# del_data('文件名', 'name')

# table(1)
# del_table(1)
