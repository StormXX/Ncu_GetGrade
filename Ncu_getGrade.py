# -*- coding: utf-8 -*-  
#---------------------------------------
#   程序：南昌大学查询成绩
#   版本：0.2
#   作者：网工111-廖肇兴-gintama
#   日期：2014-08-15
#   语言：Python 2.7
#   功能：输入用户名和密码查询成绩
#---------------------------------------

import httplib2
from httplib2 import socks
import urllib
import re
from pyquery import PyQuery as pq
import getpass
import datetime


class ncu_getGrade:

	def __init__(self):
		self.username=''
		self.password=''
		self.sessionID=''
		self.terms=[]

	def BindSession(self,userName,passWord):
		#发送一次get取得sessionid
		conn=httplib2.Http()
		url='http://218.64.56.18/Logon.do?method=logon'
		resp,content=conn.request(url)
		self.sessionID=resp['set-cookie']

		#用这个sessionid模拟登陆
		headers={'Cookie':self.sessionID,'Referer':'218.64.56.18','Content-Type':'application/x-www-form-urlencoded','Accept':'*/*','Connection':'Keep-Alive'}
		data='USERNAME='+userName+'&PASSWORD='+passWord+'&useDogCode=&x=0&y=0'
		(resp1,content1)=conn.request(url,"POST",body=data,headers=headers)

		#sessionid绑定账户
		url2='http://218.64.56.18/Logon.do?method=logonBySSO'
		data2=''
		header2={'Cookie':self.sessionID,'Referer':'218.64.56.18','Content-Type':'application/x-www-form-urlencoded','Accept':'*/*','Connection':'Keep-Alive'}
		(resp2,content2)=conn.request(url2,"POST",body=data2,headers=header2)

	def GetGrade(self,term):
		#进入成绩页面，获取成绩
		conn=httplib2.Http()
		url3='http://218.64.56.18/xszqcjglAction.do?method=queryxscj'
		data3='kksj='+term+'&kcxz=&kcmc=&xsfs=&ok='
		header3={'Cookie':self.sessionID,'Content-Type':'application/x-www-form-urlencoded','Accept':'*/*','Connection': 'Keep-Alive'}
		(resp3,content3)=conn.request(url3,"POST",body=data3,headers=header3)
		self.deal_html(content3)
	
	#处理html获取成绩
	def deal_html(self,content):
		d=pq(content.decode('utf-8'))
		table=d('table').eq(2)
		grade_count=table.find('tr').size()
		grade_all=table.find('tr')
		print u' 课程名              成绩      '
		print u'-------------------------------'
		for item in range(0,grade_count):
			print grade_all.eq(item).find('td').eq(6).text()+'------'+grade_all.eq(item).find('td').eq(7).text()

	def Gen_Terms(self):
		year=datetime.date.today().year
		month=datetime.date.today().month
		if(month>=6):
			yearStr=str(year-1)+'-'+str(year)
			self.terms.append(yearStr+'-2')
			self.terms.append(yearStr+'-1')
			yearStr=str(year-2)+'-'+str(year-1)
			self.terms.append(yearStr+'-2')
			self.terms.append(yearStr+'-1')
		else:
			yearStr=str(year-1)+'-'+str(year)
			self.terms.append(yearStr+'-1')
			yearStr=str(year-2)+'-'+str(year-1)
			self.terms.append(yearStr+'-2')
			self.terms.append(yearStr+'-1')
		index=1
		for term in self.terms:
			print str(index)+u'、'+term
			index+=1





#-------- 程序入口处 ------------------
print u"""#---------------------------------------
#   程序：南昌大学查询成绩
#   版本：0.2
#   作者：网工111-廖肇兴-gintama
#   日期：2014-08-15
#   语言：Python 2.7
#   功能：输入用户名和密码查询成绩
#---------------------------------------
"""

#初始化类
g=ncu_getGrade()
print u'请输入学号:'
userN=raw_input("SchoolNum:")
print u'请输入密码:(密码不会显示出来)'
passW=getpass.getpass()
print u'请选择学期：(输入序号)'
g.Gen_Terms()
term_Num=int(raw_input('Number:'))
if(term_Num>4 or term_Num<1):
	print u'输入错误,拜拜~'
	#按键退出
	print u'print Enter to exit'
	quit=raw_input()

else:

	#获得绑定的JSESSIONID
	g.BindSession(userN,passW)
	#调用获取成绩的方法
	g.GetGrade(g.terms[term_Num-1])

	#按键退出
	print u'print Enter to exit'
	quit=raw_input()
