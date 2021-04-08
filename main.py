import re
import bs4
import time
import main_sql
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver


class bdy():
    def __init__(self, find_name, tabnum):
        self.depth = 6
        self.count = 0
        self.judge_ = 1
        self.page = 1
        self.start = time.perf_counter()
        self.find_name = find_name
        self.tabNum = find_name + '_' + tabnum

        self.url_1 = "http://www.pansoso.org"
        self.url_2 = "http://www.647.net/search-index-keyword-"
        # self.url_2 = "http://www.btbtt.me/search-index-keyword-"
        self.headers = {"User-Agent": UserAgent().random}

    def getHtmltext(self, find_url):
        '''
        url解析器
        :param find_url: 要查找的url
        :param headers:
        :return: 若response状态码为200,返回网页原代码
        '''
        try:
            r = requests.get(find_url, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text
            return html
        except:
            # print('network error')
            return ''

    def print_resource(self, name, count_ch):
        '''
        打印输出结果
        :param name: 深度解析并核实链接有效性后的信息字典
        :param count_ch: 用于格式化输出结果
        :param start: 计时开始时间,用于计算代码运行时间
        :return: None
        '''
        print(f"print-tabNum {self.tabNum}")
        self.count += 1
        # return "{0:^6} {1:{7}<23}{6:}   {2:^3}\t{3:^6} {4:>10}\t{5:<35} |用时{8:.2f}s".format(count, name['文件名'][:20]+'...', name['类别'], name['文件大小'], name['文件格式'], name['资源链接'], chr(12288)*count_ch, chr(12288), time.perf_counter() - start)
        print("{0:^6} {1:{7}<23}{6:}   {2:^3}\t{3:^6} {4:>10}\t{5:<35}".format(self.count, name['文件名'][:20] + '...', name['类别'],
                                                                               name['文件大小'], name['文件格式'], name['资源链接'],
                                                                               chr(12288) * count_ch, chr(12288)), end='')
        print(" |用时{:.2f}s".format(time.perf_counter() - self.start))
        # time.sleep(0.5)
        main_sql.insert_data(self.tabNum, (name['文件名'][:20]+'...', name['类别'], name['文件大小'], name['文件格式'], name['资源链接']))

    def check(self, filename, fileurl):
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
                if eval(dict_name['文件大小'].split()[0]) == 0:
                    judge = 0
                # if dict_name['文件格式'] in ['.txt', '.doc', '.docx', '.exe']:
                #     judge = 0
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
                    self.print_resource(dict_name, count_ch)
                else:
                    return ''
            except:
                return ''
        except:
            return ''

    def parserHtml_1(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tags = soup('div', attrs={'class': 'pss'})
            try:
                for tag in tags:
                    file_url = self.url_1 + tag.a.attrs['href']
                    file_name = tag.div.text
                    html_1 = self.getHtmltext(file_url)
                    soup_2 = BeautifulSoup(html_1, 'html.parser')
                    tags = soup_2('a', attrs={'rel': 'noreferrer external nofollow'})
                    try:
                        for tag in tags:
                            detail_url = tag.attrs['href']
                            html_2 = self.getHtmltext(detail_url)
                        result = re.findall(r'<div class="platform-tips" node-id="(.*?)"', html_2, re.M)
                        if result == ['web-cancelleddoc']:
                            continue
                        else:
                            self.check(file_name, detail_url)
                    except:
                        return ''
            except:
                return ''
        except:
            return ''

    def parserHtml_2(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            # tags_1 = soup('span', attrs={'class': 'red'})
            tags_1 = soup('a', attrs={'class': 'subject_link'})
            for tag_1 in tags_1:
                download = {}
                # mid_url = tag_1.parent.attrs['href']
                mid_url = tag_1.attrs['href']
                html = self.getHtmltext(mid_url)
                soup_2 = BeautifulSoup(html, "html.parser")
                try:
                    for tags_2 in soup_2.find('div', attrs={'class': 'attachlist'}):
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
                                self.print_resource(download, count_ch)
                except:
                    continue
        except:
            return ''

    def fun_1(self):
        try:
            for i in range(self.depth):
                index = i + 1
                find_url = self.url_1 + '/zh/' + self.find_name + f'/pn{index}.html'
                html = self.getHtmltext(find_url)
                self.parserHtml_1(html)
            print('-' * 36)
            # main_sql.del_table(self.tabNum)
        except:
            print("查找失败,请重试.")

    def fun_2(self):
        try:
            print("正在搜索资源,请稍候...")
            # if page == 1:
            # try:
            #    driver = webdriver.Chrome()
            #    driver.get("http://www.647.net/")
            #    driver.quit()
            # except:
            # print('请检查Chromedriver版本是否正确')
            #    pass
            for i in range(self.page):
                find_url = self.url_2 + self.find_name + f'-page-{self.page}.htm'
                html = self.getHtmltext(find_url)
                self.parserHtml_2(html)
            if self.count >= 20:
                self.judge_ = 0.
                print('-' * 36)
            else:
                self.judge_ = 1
                self.fun_1()
        except:
            print('error')
            if self.judge_ == 1:
                self.fun_1()

    def main(self):
        main_sql.table(self.tabNum)
        self.fun_2()


class bilibili():
    def __init__(self, url):
        self.url = url
        self.headers = {"User-Agent": UserAgent().random}
        self.result = "※输入 bilibili 视频链接错误※"

    def getHtmltext(self, find_url):
        '''
        url解析器
        :param find_url: 要查找的url
        :param headers:
        :return: 若response状态码为200,返回网页原代码
        '''
        try:
            r = requests.get(find_url, headers=self.headers)
            r.raise_for_status()
            r.encoding = 'utf-8'

            return r.text
        except:
            # print('network error')
            return ''

    def parserHtml(self):
        html = self.getHtmltext(self.url)

        tags = etree.HTML(html)
        datas = tags.xpath('//meta/@content')
        pic_name = tags.xpath('//meta[@name="keywords"]/@content')[0]

        for ch in "\\/:*?？<>|":
            pic_name = pic_name.replace(ch, ' ')[:36]
        # print(f"pic_name = {pic_name}")
        judge = 0
        for ch in ['.jpg', '.png', '.bmp', '.jpeg', '.gif']:
            for data in datas:
                pic_url = re.findall(rf'.*?{ch}', data, re.I | re.M)
                if pic_url:
                    judge = 1
                    if pic_name[-1] in [',', '，', ':', '：', '。']:
                        pic_name = pic_name[:-1]
                    filename = pic_name + ch
                    break
            if judge:
                break

        return pic_name, pic_url

    def main(self):
        try:
            if not self.url:
                return "哔哩哔哩 (゜-゜)つロ 干杯~-bilibili"
            pic_name, pic_url = self.parserHtml()
            data = []

            if pic_url:
                # self.result = f'\n  {pic_name}... の 封面地址:\n\t{pic_url[0]}'
                data.append(pic_name)
                data.append(pic_url[0])
                self.result = data
                print(self.result)
            else:
                print("\n  ※输入 bilibili 视频链接错误※")
            print('-'*36)
            return self.result
        except:
            print("\n  ※输入 bilibili 视频链接错误※")
            # print("\n  ※爬取失败※")
            print('-'*36)
            return self.result
