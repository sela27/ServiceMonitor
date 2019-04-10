import psutil
import time
import os
from time import gmtime, strftime
from datetime import datetime

def writeToServiceList():
        serviceList = open("serviceList" , "a")
        serviceList.write("*******************************************************************\n")
        serviceList.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
        for proc in psutil.process_iter():
                try:
                        pinfo = proc.as_dict(attrs=['pid' ,'name', 'username' ,'status'])
                except psutil.NoSuchProcess:
                        pass
                else:
                        serviceList.write(str(pinfo) + "\n")
        serviceList.write("*******************************************************************\n")
        serviceList.close()



def writeToStatusLog(old_process_dict , new_process_dict):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        statuslog = open("Status_Log.txt" , "a")
        for oldproc,info in old_process_dict.items():
                if oldproc not in new_process_dict:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        statuslog.write("time: " + str(now) + "\n")
                        statuslog.write(str(oldproc) + str(info) + " has died\n")
                        print("pid: " +str(oldproc) +" "+ str(info) + " has died")
                        

        for newproc,info in new_process_dict.items():
                if newproc not in old_process_dict:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        statuslog.write("time: " + str(now) + "\n")
                        statuslog.write(str(newproc) + str(info) + " was created\n")
                        print("pid: " + str(newproc) + str(info) + " was created")
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
	firstinput = raw_input("please insert first date in the following format : year-month-day hour:minute:second\n")
	secondinput = raw_input("please insert second date (later than the first date) in the following format : year-month-day hour:minute:second\n")
	try:
		first = datetime.strptime(firstinput , "%Y-%m-%d %H:%M:%S")
		second = datetime.strptime(secondinput , "%Y-%m-%d %H:%M:%S")
	except ValueError:
		print("ohh wrong format")
	finally:
		statuslog = open("Status_Log.txt" , "r")
		Listoflines = statuslog.readlines()
		for line ,value in enumerate(Listoflines):
			if Listoflines[line].startswith("time:"):
				time = Listoflines[line][6:-1]
				date = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
				line = line + 1
				if date > second:
					break
				if date >= first:
					print(Listoflines[line])
			else:
				pass
		print("finish all event at the given time time")
		statuslog.close()

else:
      print("WORNG")
