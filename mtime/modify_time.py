#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__="lupuxiao" 
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser
from tools.ssh import ssh

def m_time(ip,port,server,mtime):
	stop_cmd="""'cd /data/server/%s && ./gamectl sync_stop -q'"""%server
	mtime_cmd="""'date -s "%s" && echo -e "\033[1;32m-------------------\033[0m" && echo `date +"%%Y-%%m-%%d %%H:%%M:%%S"` && echo -e "\033[1;32m-------------------\033[0m"'"""%mtime
	start_cmd="""'cd /data/server/%s && ./gamectl start'"""%server
	try:
		sshconnect=ssh(host=ip,port=port)

		print "\033[1;33m开始停服: %s\033[0m"%server
		stdout,stderr,returncode = sshconnect.run(stop_cmd,drop_socket=False)
		print stdout.strip("\n")
		if returncode != 0:
			print "停服失败!!! %s,%s"%(stdout,stderr)

		print "\033[1;33m\n开始修改机器时间: %s\033[0m"%ip
		stdout,stderr,returncode = sshconnect.run(mtime_cmd,drop_socket=False)
		print stdout.strip("\n")
		if returncode != 0:
			print "修改时间失败!!! %s,%s"%(stdout,stderr)

		print "\033[1;33m\n开始开启服: %s\033[0m"%server
		stdout,stderr,returncode = sshconnect.run(start_cmd,drop_socket=False)
		print stdout.strip("\n")
		if returncode != 0:
			print "开启游戏服失败!!! %s,%s"%(stdout,stderr)

	except Exception,err:
		message = '"fail",sshconnect失败,信息:%s'%(err)
		raise Exception(message)		



def getnowtime(ip,port):
	cmd = """'echo `date +"%Y-%m-%d %H:%M:%S"`'"""
	try:
		sshconnect=ssh(host=ip,port=port)
		stdout,stderr,returncode = sshconnect.run(cmd,drop_socket=False)
		if returncode != 0:
			print "获取机器当前时间失败!!!,请联系运维处理... %s,%s"%(stdout,stderr)	
		else:
			print stdout.strip("\n")		
	except Exception,err:
		message = '"fail",sshconnect失败,信息:%s'%(err)
		raise Exception(message)

def main(avgr):
	usage = '''%prog  --lang en|tw  --online|--new'''

	parser = OptionParser(usage=usage)
	parser.add_option("--lang",action="store",type="choice",choices=("tw","en","tl"),dest="lang",help="指定语言:tl,tw,en",metavar="tl|tw|en")
	parser.add_option("--time",action="store",type="str",dest="mtime",help="时间 2015-09-06 23:57:00",metavar="2015-09-06 23:57:00")	
	parser.add_option("--online",action="store_true",dest="online",help="线上")
	parser.add_option("--new",action="store_true",dest="new",help="最新")
	parser.add_option('--nowtime',action="store_true",dest="nowtime",help="获取机器当前时间")

	option,args = parser.parse_args()


	if option.online and option.new:
		parser.error("--online 与 --new 不能同时使用")

	port = 22

	if option.lang == 'en':
		ip="52.76.92.169"
		sshconnect=ssh(host=ip,port=port)
		if option.online:
			server="en_s998"
			m_time(ip,port,server,option.mtime)
		if option.new:
			server="en_s999"
			m_time(ip,port,server,option.mtime)

		if option.nowtime:
			getnowtime(ip,port)

	if option.lang == 'tw':
		ip="210.200.14.28"
		sshconnect=ssh(host=ip,port=port)
		if option.online:
			server="tw_s3"
			m_time(ip,port,server,option.mtime)
		if option.new:
			server="tw_s2"
			m_time(ip,port,server,option.mtime)
	
		if option.nowtime:
			getnowtime(ip,port)

	if option.lang == 'tl':
		ip="203.151.82.219"
		sshconnect=ssh(host=ip,port=port)
		if option.online:
			server="tl_s998"
			m_time(ip,port,server,option.mtime)
		if option.new:
			server="tl_s999"
			m_time(ip,port,server,option.mtime)
	
		if option.nowtime:
			getnowtime(ip,port)

if __name__ == "__main__":
	main(sys.argv)













