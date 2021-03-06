#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__="lupuxiao" 
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser
from tools.ssh_pk import ssh_pk
import ConfigParser
import time

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



#判断机器时间来重启游戏
def cront_restart(ip,port,cmd):
	nowtime = int(time.time())
	import datetime
	print "#"*20,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"#"*20
	get_nowtime = 'python -c "import time;print time.time()"'
	try:
		SSH=ssh_pk(ip,port)
		stdin,stdout,stderr = SSH.exec_command(get_nowtime)
		server_time=int(stdout.read().strip("\n").split(".")[0])
		#1小时相差
		print "当前: %s  服务器:  %s"%(nowtime,server_time)
		if server_time - nowtime > 3600:
			#back_now_time(ip,port,cmd)
			print "服务器时间大于1小时需要更改,检查游戏是否符合当前时间"
			#在判断是哪个服时间不对
			get_server_time="cd /data/server/%s && ./gamectl eval 'util:now_sec().'"%server
			stdin,stdout,stderr = SSH.exec_command(get_server_time)
			ser_time = int(stdout.read().strip("\n").split(".")[0])
			print "当前: %s  游戏服时间:  %s"%(nowtime,ser_time)
			if ser_time - nowtime > 3600:
				print "游戏需要恢复时间,正在恢复..."
				back_now_time(ip,port,cmd)
			else:
				print "游戏无需恢复时间"
		else:
			print "服务器时间小于1小时无需更改"
	except Exception,err:
		SSH.close()
		raise Exception(err)




def main(avgr):
	usage = '''%prog  -h'''

	parser = OptionParser(usage=usage)
	parser.add_option("--lang",action="store",type="str",dest="lang",help="指定平台:tl,tw,en",metavar="tl|tw|en")
	parser.add_option("--time",action="store",type="str",dest="mtime",help="时间 2015-09-06 23:57:00",metavar="2015-09-06 23:57:00")	
	parser.add_option("--online",action="store_true",dest="online",help="线上")
	parser.add_option("--new",action="store_true",dest="new",help="最新")
	parser.add_option('--nowtime',action="store_true",dest="nowtime",help="获取机器当前时间")
	parser.add_option('--backnow',action="store_true",dest="backnow",help="恢复机器当前时间")
	parser.add_option('--backnow_crond',action="store_true",dest="backnow_crond",help="计划任务中恢复机器与游戏当前时间")
	option,args = parser.parse_args()

	if not option.lang:
		parser.error("--lang 没有指定,-h查看")

	if option.online and option.new:
		parser.error("--online 与 --new 不能同时使用")
	if option.nowtime and option.backnow:
		parser.error("--nowtime 与 --backnow 不能同时使用")

	global server
	cf = ConfigParser.ConfigParser()	
	cf.read("/data/django/yunwei/mtime/servers.conf")	
	secs = cf.sections()
	if option.lang not in secs:
		print '\033[1;31m"fail",输入的平台不在配置文件中,请检查(servers.conf)...\033[0m'
		exit(1)

	ip=cf.get(option.lang,"ip")
	port=int(cf.get(option.lang,"port"))
	ntpdate=cf.get(option.lang,"ntpdate")
	
	if option.online :
		server=cf.get(option.lang,"online")
		if option.mtime:
			m_time(ip,port,server,option.mtime)
	if option.new : 
		server=cf.get(option.lang,"new")
		if option.mtime:
			m_time(ip,port,server,option.mtime)

	if option.nowtime:
		getnowtime(ip,port)

	

	#print backtime_cmd
	if option.backnow:
		stop_cmd = 'cd /data/server/%s && ./gamectl sync_stop -q'%server
		back_cmd="/usr/sbin/ntpdate -u %s > /var/log/ntpdate.log 2>&1"%ntpdate
		start_cmd='./gamectl start'
		backtime_cmd=stop_cmd+";"+back_cmd+";"+start_cmd
		back_now_time(ip,port,backtime_cmd)			

	if option.backnow_crond:
		stop_cmd = 'cd /data/server/%s && ./gamectl sync_stop -q'%server
		back_cmd="/usr/sbin/ntpdate -u %s > /var/log/ntpdate.log 2>&1"%ntpdate
		start_cmd='./gamectl start'
		backtime_cmd=stop_cmd+";"+back_cmd+";"+start_cmd
		cront_restart(ip,port,backtime_cmd)


			
if __name__ == "__main__":
	main(sys.argv)
















