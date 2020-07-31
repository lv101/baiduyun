import re
import bs4
import time
import main_sql
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver


def getHtmltext(find_url, headers):
    '''
    url解析器
    :param find_url: 要查找的url
    :param headers:
    :return: 若response状态码为200,返回网页原代码
    '''
    try:
        r = requests.get(find_url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        return html
    except:
        return ''

def print_resource(name, count_ch, start):
    '''
    打印输出结果
    :param name: 深度解析并核实链接有效性后的信息字典
    :param count_ch: 用于格式化输出结果
    :param start: 计时开始时间,用于计算代码运行时间
    :return: None
    '''
    global count
    global tabNum
    print(f"print-tabNum {tabNum}")
    count += 1
    # return "{0:^6} {1:{7}<23}{6:}   {2:^3}\t{3:^6} {4:>10}\t{5:<35} |用时{8:.2f}s".format(count, name['文件名'][:20]+'...', name['类别'], name['文件大小'], name['文件格式'], name['资源链接'], chr(12288)*count_ch, chr(12288), time.perf_counter() - start)
    print("{0:^6} {1:{7}<23}{6:}   {2:^3}\t{3:^6} {4:>10}\t{5:<35}".format(count, name['文件名'][:20] + '...', name['类别'],
                                                                           name['文件大小'], name['文件格式'], name['资源链接'],
                                                                           chr(12288) * count_ch, chr(12288)), end='')
    print(" |用时{:.2f}s".format(time.perf_counter() - start))
    main_sql.insert_data(tabNum, (name['文件名'][:20]+'...', name['类别'], name['文件大小'], name['文件格式'], name['资源链接']))

def check(filename, fileurl, start):
    try:
        judge = 1
        dict_name = {}
        list_1 = filename.split('，')
        for j in range(len(list_1)):
            list_2 = list_1[j].split('：')
            if len(list_2) == 2:
                dict_name[list_2[0]] = list_2[1]
        try:
            for ch in "《》【】. []：——":
                dict_name['文件名'] = dict_name['文件名'].replace(ch, '')
            for ch in ' ':
                dict_name['类别'] = dict_name['类别'].replace(ch, '')
                dict_name['文件格式'] = dict_name['文件格式'].replace(ch, '')
            count_ch = 0
            if dict_name['文件大小'].split()[1] in ['kb', 'Kb', 'KB', 'kB'] \
                    and eval(dict_name['文件大小'].split()[0]) <= 5:
                judge = 0
            if dict_name['文件格式'] in ['.txt', '.doc', '.docx', '.exe']:
                judge = 0
            for ch in dict_name['文件名'][:20]:
                if ch in "!@#$%^&*()_+-={}|01234567.89QWERTYUIOPASDFHJKLZXCVBNMqwertyuiopasdfhjklzxcvbnm<> ,?/\\“’”‘][~`":
                    count_ch += 1
            if count_ch < 6:
                count_ch = 0
            elif count_ch >= 20:
                count_ch = round(count_ch / 5) + 5
            elif count_ch >= 18:
                count_ch = round(count_ch / 5) + 4
            elif count_ch >= 16:
                count_ch = round(count_ch / 5) + 3
            elif count_ch >= 14:
                count_ch = round(count_ch / 5) + 2
            elif count_ch >= 10:
                count_ch = round(count_ch / 5) + 1
            else:
                count_ch = round(count_ch / 5)
            dict_name['资源链接'] = fileurl
            if judge:
                print_resource(dict_name, count_ch, start)
            else:
                return ''
        except:
            return ''
    except:
        return ''

def parserHtml_1(html, url, headers, start):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('div', attrs={'class': 'pss'})
        try:
            for tag in tags:
                file_url = url + tag.a.attrs['href']
                file_name = tag.div.text
                html_1 = getHtmltext(file_url, headers)
                soup_2 = BeautifulSoup(html_1, 'html.parser')
                tags = soup_2('a', attrs={'rel': 'noreferrer external nofollow'})
                try:
                    for tag in tags:
                        detail_url = tag.attrs['href']
                        html_2 = getHtmltext(detail_url, headers)
                    result = re.findall(r'<div class="platform-tips" node-id="(.*?)"', html_2, re.M)
                    if result == ['web-cancelleddoc']:
                        continue
                    else:
                        check(file_name, detail_url, start)
                except:
                    return ''
        except:
            return ''
    except:
        return ''

def parserHtml_2(html, headers, start):
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_1 = soup('span', attrs={'class': 'red'})
        for tag_1 in tags_1:
            download = {}
            mid_url = tag_1.parent.attrs['href']
            html = getHtmltext(mid_url, headers)
            soup_2 = BeautifulSoup(html, "html.parser")
            try:
                for tags_2 in soup_2.find('div', attrs={'class': 'attachlist'}).children:
                    if isinstance(tags_2, bs4.element.Tag):
                        tag_2 = tags_2('a', attrs={'class': 'ajaxdialog'})
                        for a in tag_2:
                            down_u = a.attrs['href'].replace('dialog', 'download')
                            down_n = a.text
                            download['文件名'] = down_n
                            download['类别'] = 'BT种子'
                            download['文件格式'] = '.torrent'
                            download['资源链接'] = down_u
                            tag_3 = tags_2('td', attrs={'class': 'grey'})
                            for td in tag_3:
                                if '.' in td.text:
                                    download['文件大小'] = td.text.replace(' ', '')
                            count_ch = 0
                            for ch in "《》【】. []：——":
                                download['文件名'] = download['文件名'].replace(ch, '')
                            for ch in download['文件名'][:20]:
                                if ch in "!@#$%^&*()_+-={}|01234567.89QWERTYUIOPASDFHJKLZXCVBNMqwertyuiopasdfhjklzxcvbnm<> ,?/\\“’”‘][~`":
                                    count_ch += 1
                            if count_ch < 6:
                                count_ch = 0
                            elif count_ch >= 20:
                                count_ch = round(count_ch / 5) + 5
                            elif count_ch >= 18:
                                count_ch = round(count_ch / 5) + 4
                            elif count_ch >= 16:
                                count_ch = round(count_ch / 5) + 3
                            elif count_ch >= 14:
                                count_ch = round(count_ch / 5) + 2
                            elif count_ch >= 10:
                                count_ch = round(count_ch / 5) + 1
                            else:
                                count_ch = round(count_ch / 5)
                            print_resource(download, count_ch, start)
            except:
                continue
    except:
        return ''

def fun_1(depth, url, headers, find_name, start):
    try:
        global tabNum
        for i in range(depth):
            index = i + 1
            find_url = url + '/zh/' + find_name + f'/pn{index}.html'
            html = getHtmltext(find_url, headers)
            parserHtml_1(html, url, headers, start)
        print('-' * 130)
        main_sql.del_table(tabNum)
    except:
        print("查找失败,请重试.")

def fun_2(depth, url_1, url_2, headers, find_name, page):
    global count
    global judge_
    start = time.perf_counter()
    try:
        print("正在搜索资源,请稍候...")
        try:
            driver = webdriver.Chrome()
            driver.get("http://www.3btjia.com/")
            driver.quit()
        except:
            pass
        for i in range(page):
            find_url = url_2 + find_name +f'-page-{page}.htm'
            html = getHtmltext(find_url, headers)
            parserHtml_2(html, headers, start)
        if count >= 20:
            judge_ = 0
        else:
            judge_ = 1
            fun_1(depth, url_1, headers, find_name, start)
    except:
        if judge_ == 1:
            fun_1(depth, url_1, headers, find_name, start)

def bdy(find_name, tabnum):
    url_1 = "http://www.pansoso.org"
    url_2 = "http://www.3btjia.com/search-index-keyword-"
    headers = {
        "User-Agent": UserAgent().random,
        # "Cookie": f"bbs_sid=fd0cac446f83208b; bbs_lastday={round(lastday)}; timeoffset=%2B08; cck_lasttime={round(lastday*1000)}; cck_count=2; bbs_lastonlineupdate={round(tim)}"}
    }
    depth = 2
    global count
    global judge_
    global tabNum
    tabNum = tabnum
    count = 0
    judge_ = 1
    page = 1
    fun_2(depth, url_1, url_2, headers, find_name, page)
    # for data in main_sql.search_data():
    #     print(data)

    # while True:
    #     print("\t1.加载下一页\n\t2.退出系统\n\t3.查找新的资源")
    #     user_choose = input("请输入[1-3]:")
    #     if user_choose == '1':
    #         count = 0
    #         if judge_ == 0:
    #             page += 1
    #             fun_2(depth, url_1, url_2, headers, find_name, page)
    #         elif judge_ == 1:
    #             depth *= 2
    #             page += 1
    #             fun_2(depth, url_1, url_2, headers, find_name, page)
    #     elif user_choose == '2':
    #         time.sleep(1)
    #         break
    #     elif user_choose == '3':
    #         find_name = input("请输入你要查找的资源名称：")
    #         count = 0
    #         page = 1
    #         fun_2(depth, url_1, url_2, headers, find_name, page)
    #     else:
    #         print("输入错误,请重新输入")
    #         print('-' * 130)