# -*- coding: utf-8 -*-  
#---------------------------------------
#   程序：南昌大学查电费
#   版本：0.1
#   作者：网工111-廖肇兴-gintama
#   日期：2014-08-15
#   语言：Python 2.7
#   功能：输入寝室号查询电费
#---------------------------------------

import httplib2
from httplib2 import socks
from pyquery import PyQuery as pq
import urllib

class ncu_getElecInfo:

	def __init__(self):
		self.roomnumber=''
		self.sessionid=''
		self.aspauth=''

	def GetElecInfo(self,roomNum):
		self.roomnumber=roomNum
		#conn=httplib2.Http(proxy_info=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP,'127.0.0.1',8888))
		conn=httplib2.Http()
		url='http://222.204.3.210/ssdf/Account/LogOn'
		(res,content)=conn.request(url)
		self.sessionid=res['set-cookie']

		headers1={'Cookie':self.sessionid,'Content-Type':'application/x-www-form-urlencoded','Accept':'*/*'}
		data={'UserName':roomNum}
		(res1,content1)=conn.request(url,"POST",body=urllib.urlencode(data),headers=headers1)
		self.aspauth=res1['set-cookie']

		#清除cookie中的莫名其妙的东西
		self.sessionid=self.sessionid.replace('HttpOnly','')
		self.aspauth=self.aspauth.replace('HttpOnly','')
		url2='http://222.204.3.210/ssdf/EEMQuery/EEMBalance'
		headers2={'Cookie':self.aspauth+self.sessionid}
		(res2,content2)=conn.request(url2,'GET',headers=headers2)

		self.deal_html(content2)

	def deal_html(self,content):
		d=pq(content.decode('utf-8'))
		table=d('table').eq(0)
		money_left=table.find('tr').eq(2).find('td').eq(1).text()
		elec_left=table.find('tr').eq(3).find('td').eq(1).text()
		print u'用户:'+self.roomnumber
		print u'-------------------------'
		print u'现金余额(元)：'+money_left
		print u'现金电量余额(度)：'+elec_left

#-------- 程序入口处 ------------------
print u"""#---------------------------------------
#   程序：南昌大学查询电费
#   版本：0.1
#   作者：网工111-廖肇兴-gintama
#   日期：2014-08-15
#   语言：Python 2.7
#   功能：输入寝室号查询电费
#---------------------------------------
"""

print u'请输入寝室号：'
roomNum=raw_input()
e=ncu_getElecInfo()
e.GetElecInfo(roomNum)

print u'press enter to exit'
quit=raw_input()

