from flask import Flask, request, render_template
import main
import main_sql

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
    main_sql.del_table('none')
    return render_template('index.html')


# @app.route('/del')
# def tab():
#     tabnum = request.values.get("tabnum")
#     if tabnum:
#         main_sql.del_table(tabnum)
#         # print(f"del-tabNum {tabnum}")
#     return f"tabnum={tabnum}"


@app.route('/ajax')
def ajax():
    tabnum = request.values.get("tabnum")
    data = []

    if tabnum:
        print(f"ajax-tabNum {tabnum}")
        result = main_sql.search_data(tabnum)


        if result:
            for row in result:
                data.append([row[0], row[1], row[2], row[3], row[4], row[5]])

    return str(data)


@app.route('/research')
def bdy():
    keyword = request.values.get("keyword")
    tabnum = request.values.get("tabnum")

    if tabnum:
        print(f"research-tabNum {tabnum}")
        print(f"research-keyword {keyword}")

        main_sql.table(tabnum)
        main.bdy(keyword, tabnum)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2333, threaded=True, debug=True)
