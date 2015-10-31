#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__="lupuxiao" 
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser
from tools.ssh_pk import ssh_pk


def m_time(ip,port,server,mtime):
	stop_cmd='cd /data/server/%s && ./gamectl sync_stop -q'%server
	mtime_cmd='date -s "%s" > /dev/null && echo -e "\033[1;32m-------------------\033[0m" && echo `date +"%%Y-%%m-%%d %%H:%%M:%%S"` && echo -e "\033[1;32m-------------------\033[0m"'%mtime
	start_cmd='cd /data/server/%s && ./gamectl start'%server
	try:
		SSH=ssh_pk(ip,port)
		stdin,stdout,stderr=SSH.exec_command(stop_cmd)
		stdout=stdout.read().strip("\n")
		stderr=stderr.read().strip("\n")
		print stdout		
		if stderr != "":	
			print "停服失败...%s"%(stderr)
			exit()

		stdin,stdout,stderr=SSH.exec_command(mtime_cmd)
		stdout=stdout.read().strip("\n")
		stderr=stderr.read().strip("\n")
		print stdout		
		if stderr != "":	
			print "修改时间失败...%s"%(stderr)
			exit()	


		stdin,stdout,stderr=SSH.exec_command(start_cmd)
		stdout=stdout.read().strip("\n")
		stderr=stderr.read().strip("\n")
		print stdout
		if stderr != "":	
			print "启动失败...%s"%(stderr)
			exit()	
		SSH.close()	
	except Exception,err:			
		message = '"fail",修改时间失败,信息:%s'%(err)
		SSH.close()
		raise Exception(message)

def getnowtime(ip,port):
	cmd = 'echo `date +"%Y-%m-%d %H:%M:%S"`'
	try:
		SSH=ssh_pk(ip,port)
		stdin,stdout,stderr = SSH.exec_command(cmd)
		stdout=stdout.read().strip("\n")
		stderr=stderr.read().strip("\n")
		if stderr != "":				
			print "获取机器当前时间失败!!!,请联系运维处理...%s"%(stderr)	
			SSH.close()
			exit()
		print stdout
	except Exception,err:
		SSH.close()	
		message = '"fail",sshconnect失败,信息:%s'%(err)
		raise Exception(message)



def back_now_time(ip,port,cmd):
	try:
		SSH=ssh_pk(ip,port)
		stdin,stdout,stderr = SSH.exec_command(cmd)
		stdout=stdout.read().strip("\n")
		stderr=stderr.read().strip("\n")
		if stderr != "":				
			print "恢复当前时间失败,请联系运维处理...%s"%(stderr)	
			SSH.close()
			exit()
		print stdout
		print "恢复机器当前时间成功.."
	except Exception,err:
		SSH.close()	
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
	parser.add_option('--backnow',action="store_true",dest="backnow",help="恢复机器当前时间")
	option,args = parser.parse_args()


	if option.online and option.new:
		parser.error("--online 与 --new 不能同时使用")
	if option.nowtime and option.backnow:
		parser.error("--nowtime 与 --backnow 不能同时使用")

	port = 22

	if option.lang == 'en':
		ip="52.76.92.169"
		if option.online:
			server="en_s998"
			if option.mtime:
				m_time(ip,port,server,option.mtime)
		if option.new :
			server="en_s999"
			if option.mtime:
				m_time(ip,port,server,option.mtime)

		if option.nowtime:
			getnowtime(ip,port)

		if option.backnow:
			stop_cmd = 'cd /data/server/%s && ./gamectl sync_stop -q'%server
			back_cmd="/usr/sbin/ntpdate -u sg.pool.ntp.org > /var/log/ntpdate.log 2>&1"
			start_cmd='./gamectl start'
			cmd=stop_cmd+";"+back_cmd+";"+start_cmd
			print cmd
			back_now_time(ip,port,cmd)	

	if option.lang == 'tw':
		ip="210.200.14.28"
		if option.online:
			server="tw_s3"
			if option.mtime:
				m_time(ip,port,server,option.mtime)
		if option.new :
			server="tw_s2"
			if option.mtime:				
				m_time(ip,port,server,option.mtime)
	
		if option.nowtime:
			getnowtime(ip,port)

		if option.backnow:
			stop_cmd = 'cd /data/server/%s && ./gamectl sync_stop -q'%server
			back_cmd="/usr/sbin/ntpdate -u tw.pool.ntp.org > /var/log/ntpdate.log 2>&1"
			start_cmd='./gamectl start'
			cmd=stop_cmd+";"+back_cmd+";"+start_cmd
			print cmd
			back_now_time(ip,port,cmd)	

	if option.lang == 'tl':
		ip="203.151.82.219"
		if option.online:
			server="tl_s998"
			if option.mtime:
				m_time(ip,port,server,option.mtime)
		if option.new:
			server="tl_s999"
			if option.mtime:
				m_time(ip,port,server,option.mtime)
	
		if option.nowtime:
			getnowtime(ip,port)

		if option.backnow :
			stop_cmd = 'cd /data/server/%s && ./gamectl sync_stop -q'%server			
			back_cmd = "/usr/sbin/ntpdate -u th.pool.ntp.org > /var/log/ntpdate.log 2>&1"
			start_cmd='./gamectl start'
			cmd=stop_cmd+";"+back_cmd+";"+start_cmd
			print cmd
			back_now_time(ip,port,cmd)

if __name__ == "__main__":
	main(sys.argv)
















