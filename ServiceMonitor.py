import psutil
import time
import os
from time import gmtime, strftime
import datetime 
#import sys


#print(psutil.test())
#print("please choose State: \n 1 - Monitor state \n 2 - manual state")

def writeToServiceList():
	serviceList = open("serviceList" , "a")
	serviceList.write("*******************************************************************\n")
	#serviceList.write(strftime("%a, %d %b %Y %H:%M:%S \n", gmtime()))
	serviceList.write(str(datetime.datetime.now()) + "\n")
	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict(attrs=['pid' ,'name', 'username' , 'create_time' ,'status'])
		except psutil.NoSuchProcess:
			pass
        	else:
	        	serviceList.write(str(pinfo) + "\n")
	#serviceList.write(str(psutil.test()))
	serviceList.write("*******************************************************************\n")
	serviceList.close()



def writeToStatusLog(old_process_dict , new_process_dict):
	#now = time.ctime(time.time())
	now = datetime.datetime.now()
	statuslog = open("Status_Log.txt" , "a")
	for oldproc,info in old_process_dict.items():
		if oldproc not in new_process_dict:
			statuslog.write(str(oldproc) + str(info) + " has died\n")
			statuslog.write("time of death: " + str(now) + "\n")
			print("pid: " +str(oldproc) +" "+ str(info) + " has died")
			now = time.ctime(time.time())

	for newproc,info in new_process_dict.items():
		if newproc not in old_process_dict:
			statuslog.write(str(newproc) + str(info) + " was created\n")
			statuslog.write("time of birth: " + str(now) + "\n")
			print("pid: " + str(newproc) + str(info) + " was created")
			now = time.ctime(time.time())
	statuslog.close()
			

x = input("please choose State: \n 1 - Monitor state \n 2 - manual state \n")
if x == 1:
	old_process_dict = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username' ,'status'])}
	while True:
		new_process_dict = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username' ,'status'])}
		writeToServiceList()
		writeToStatusLog(old_process_dict , new_process_dict)
		old_process_dict = new_process_dict
		time.sleep(5)
	

elif x == 2:
	#TODO: add input for dates
	serviceList = open("serviceList" , "r")
	for line in serviceList.readline():
		if line[0] != line[1] != line[2] != '*':
			pass
		else:
			line = serviceList.readline()
			date = datetime.datetime.strptime(line, '%Y-%m-%d %H:%M:%S.%f')
			#check if date is after the given time and if so take this sample

else:
	print("WORNG")

