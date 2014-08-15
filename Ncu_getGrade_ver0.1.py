# -*- coding: utf-8 -*-  
#---------------------------------------
#   程序：南昌大学查询成绩
#   版本：0.1
#   作者：网工111-廖肇兴-gintama
#   日期：2014-07-20
#   语言：Python 2.7
#   功能：输入用户名和密码查询成绩
#---------------------------------------

import httplib2
from httplib2 import socks
import urllib
import re
from pyquery import PyQuery as pq


class ncu_getGrade:

	def __init__(self):
		self.username=''
		self.password=''
		self.sessionID=''

	def getLoginSession(self,userName,passWord,term):
		#conn=httplib2.Http(proxy_info=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP,'127.0.0.1',8888))
		conn=httplib2.Http()
		url='http://218.64.56.18/Logon.do?method=logon'
		resp,content=conn.request(url)
		#match=re.search(r'(.*?);',resp['set-cookie'],re.S)
		#print match
		self.sessionID=resp['set-cookie']
		#print 'sessionID=================>%s' % self.sessionID

		headers={'Cookie':self.sessionID,'Referer':'218.64.56.18','Content-Type':'application/x-www-form-urlencoded','Accept':'*/*','Connection':'Keep-Alive'}
		#data={'USERNAME':userName,'PASSWORD':passWord,'userDogCode':'','x':'0','y':'0'}
		data='USERNAME='+userName+'&PASSWORD='+passWord+'&useDogCode=&x=0&y=0'
		(resp1,content1)=conn.request(url,"POST",body=data,headers=headers)
		#print content1

		url2='http://218.64.56.18/Logon.do?method=logonBySSO'
		data2=''
		header2={'Cookie':self.sessionID,'Referer':'218.64.56.18','Content-Type':'application/x-www-form-urlencoded','Accept':'*/*','Connection':'Keep-Alive'}
		(resp2,content2)=conn.request(url2,"POST",body=data2,headers=header2)
		#print content2


		url3='http://218.64.56.18/xszqcjglAction.do?method=queryxscj'
		data3='kksj='+term+'&kcxz=&kcmc=&xsfs=&ok='
		header3={'Cookie':self.sessionID,'Content-Type':'application/x-www-form-urlencoded','Accept':'*/*','Connection': 'Keep-Alive'}
		(resp3,content3)=conn.request(url3,"POST",body=data3,headers=header3)
		self.deal_html(content3)
		#d=pq(content3.decode('utf-8'))
		#a=d('table').eq(2).find('tr').eq(1).find('td').eq(6).text()
		#b=d('table').eq(2).find('tr').size()
		#print a
		#print b
		#f=open('what.txt','w+')
		#f.writelines(a)

	def deal_html(self,content):
		d=pq(content.decode('utf-8'))
		table=d('table').eq(2)
		grade_count=table.find('tr').size()
		grade_all=table.find('tr')
		print u' 课程名              成绩      '
		print u'-------------------------------'
		for item in range(0,grade_count):
			print grade_all.eq(item).find('td').eq(6).text()+'------'+grade_all.eq(item).find('td').eq(7).text()

#-------- 程序入口处 ------------------
print u"""#---------------------------------------
#   程序：南昌大学查询成绩
#   版本：0.1
#   作者：网工111-廖肇兴-gintama
#   日期：2014-07-20
#   语言：Python 2.7
#   功能：输入用户名和密码查询成绩
#---------------------------------------
"""

print u'请输入学号:'
userN=raw_input()
print u'请输入密码:'
passW=raw_input()
print u'请输入学期，格式示范：2013-2014-2（代表2013-2014第二个学期）'
terM=raw_input()
g=ncu_getGrade()
g.getLoginSession(userN,passW,terM)
