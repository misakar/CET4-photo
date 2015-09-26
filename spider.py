# coding: utf-8

"""
    cet4.cpp
    ~~~~~~~

        爬取四级报名网站计算机同学照片
"""

import re
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup


class Cet4Spider(object):
    """
          CET$
    模拟登录CET4网站
    爬取姓名学号信息
    """
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0"
        self.headers = {
                'User-Agent':self.user_agent,
                'Referer':'http://cet.tinyin.net/login.asp',
                'Accept-encoding':'gzip'
            }
        self.postdata = urllib.urlencode({
                'stype':'#',
                'stuno':'2014214761',
                'stupwd':'#'  # 记得修改
            })


    def analog_login(self):
        """登录cet4网站，获取cookie，并将
        cookie保存至文件"""
        # 准备cookie文件, 构建opener
        filename = 'cet4_cookie.txt'
        cookie = cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

        # 利用个人用户名和密码登录cet4
        # cet4登录url
        login_url = 'http://cet.tinyin.net/reginfo.asp'
        # 构建请求
        request = urllib2.Request(login_url, self.postdata, self.headers)
        opener.open(request)
        # 保存cookie到文件 cet4_cookie.txt
        cookie.save(ignore_discard=True, ignore_expires=True)


    # 利用cookie模拟登录cet4
    def get_stu_info(self):
        file = open("stuinfo.txt", 'w+')
        """利用cookie模拟登录,爬取相关信息,并写入文件"""
        for i in range(2014210727, 2014210914, 10):
            # page 范围是727~914
            photo_url = 'http://cet.tinyin.net/accuse.asp?nxtid=%s' % str(i)

            get_cookie = cookielib.MozillaCookieJar()
            get_cookie.load('cet4_cookie.txt', ignore_discard=True, ignore_expires=True)

            # 利用cookie构建opener
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(get_cookie))
            request = urllib2.Request(photo_url)
            response = opener.open(request)
            # the html is what I want
            # html 编码转化
            html = response.read().decode('gbk').encode('utf-8’)')

            # html 的格式化打印
            # soup = BeautifulSoup(response.read(), "lxml")
            # print soup.prettify()


            # 利用正则表达式爬取html中学生姓名和学号信息，并写入文件

            # <td width="25%">
            # 学生学号: 2014210761
            # 学生姓名: 朱承浩
            #    ....
            # </td>

            # 写入文件后格式
            # 学生学号: 2014210761 学生姓名: 朱承浩
            # ......     ......     ......    ......

            parttern = re.compile('<td width=25% >(.*?)<br><br>(.*?)<br><br>', re.S)
            result = re.findall(parttern, html)
            for name in result:
                for i in range(2):
                    # name 是元组
                    file.writelines(name[i]+' ')
                file.writelines('\n')
        file.close()


if __name__ == "__main__":
    cet4 = Cet4Spider()
    cet4.analog_login()
    cet4.get_stu_info()
