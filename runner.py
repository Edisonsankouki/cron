#!/usr/bin/env python3


import sys, os, time, datetime, signal
from datetime import timedelta
from datetime import date
import os.path



#TODO: we create a file contains the pid of the process of runner in order to read it when we run the runner status.
E = os.path.expanduser('~/.runner-pid')
runner_pid = os.getpid()
f_pid = open(E,"w+")
f_pid.write(str(runner_pid))
f_pid.close()

#TODO: we check if .runstatus exists, if not we should create one.
A = os.path.expanduser('~/.runner.status')
f_run_status = open(A,"w+")
f_run_status.close()


#TODO: read the configuration file to get the programs and time 
O = os.path.expanduser("~/.runner.conf")
try:
	lines = [line.strip('\n') for line in open(O)]
except FileNotFoundError:
	print("configuration file notfound")
	sys.exit(0)
if(len(lines)==0):
	print("configuration file empty")
	sys.exit(0)
if("" in lines):
	print("empty line detected")
	sys.exit(0)
if(len(set(lines))!=len(lines)):
	print("duplicate run time")
	sys.exit(0)
#TODO: a function to check lines of configuration file in correct format.
for i in lines:
	line_0 = i.split(" ")
	if(not("run" in line_0)):
		line_num = ""
		for x in line_0:
			line_num+=x+" "
		print(f"error in configuration file: {line_num}")
		sys.exit(0)


	

#TODO: a function to parse the lines in the format we want.
def generate_messagelist(line):
	return [x.strip(" ")for x in line.split("run",2)]
parsed_lines = []

for i in lines:
	parsed_lines.append(generate_messagelist(i))





time_start = datetime.datetime.now()#get the time when we start to run cron


#TODO:a simple function to get nextweek day for "on".
def next_weekday(d, weekday_1):
	days_ahead = weekday_1 - d.weekday()
	if days_ahead <= 0:
		days_ahead+=7
	return d + datetime.timedelta(days_ahead)

#TODO:Here we define 2 schedule class to easily store the schedule.
class schedule_var_0():#this is for "at XXX" and "on XXX at XXX"
	def  __init__(self,start,date,path,para):
		self.start = start
		self.date = date
		self.path = path
		self.para = para
		self.runned = False
		time_string_1 = time.mktime(self.date.timetuple())
		time_string = time.ctime(time_string_1)
		self.will_run_message = "will run at "+time_string+" "+self.path+"  "+para #to set the message we need to write to status first.
		self.ran_message = "ran " +time_string+" "+self.path +"  "+self.para
		self.error_message = "error "+time_string+" "+self.path +"  "+self.para
class schedule_var_1():#this is for "every XXX at XXX" 
	def __init__(self,start,weekday,hour,minute,second,path,para):
		self.start = start
		self.weekday = weekday
		self.hour = hour
		self.minute = minute
		self.second = second
		self.path = path
		self.para = para
	
	def get_ran_message(self,time_now):
		time_now_0 = datetime.datetime(time_now.year,time_now.month,time_now.day,self.hour,self.minute,0,0)
		time_now_string = time.ctime(time.mktime(time_now_0.timetuple()))
		return "ran "+time_now_string+" "+self.path+" "+self.para

	def get_will_run_message(self,time_now):
		if(time_now.weekday() == self.weekday and time_now.hour < self.hour):
			if(time_start.hour==self.hour):
				if(time_start.minute < self.minute):
					next_date_time = datetime.datetime(time_now.year,time_now.month,time_now.day,self.hour,self.minute,0,0)
					time_date_string = time.ctime(time.mktime(next_date_time.timetuple()))
					return "will run at "+time_date_string+" "+self.path+" "+self.para
				else:
					next_date_time = datetime.datetime(time_now.year,time_now.month,time_now.day,self.hour,self.minute,0,0)
					time_date_string = time.ctime(time.mktime(next_date_time.timetuple()))
					return "will run at "+time_date_string+" "+self.path+" "+self.para
					
		next_date = next_weekday(time_now,self.weekday)
		next_date_time = datetime.datetime(next_date.year,next_date.month,next_date.day,self.hour,self.minute,0,0)
		time_date_string = time.ctime(time.mktime(next_date_time.timetuple()))
		return "will run at "+time_date_string+" "+self.path+" "+self.para

    
	def get_error_message(self,time_now):
		time_now_0 = datetime.datetime(time_now.year,time_now.month,time_now.day,self.hour,self.minute,0,0)
		time_now_string = time.ctime(time.mktime(time_now_0.timetuple()))
		return "error "+time_now_string+" "+self.path+" "+self.para


#TODO： a simple function to transfor the string weekday to int weekday.
def String_to_weekday(week_string):
	if week_string=="Monday":
		return 0
	if week_string=="Tuesday":
		return 1
	if week_string=="Wednesday":
		return 2
	if week_string=="Thursday":
		return 3
	if week_string=="Friday":
		return 4
	if week_string=="Saturday":
		return 5
	if week_string=="Sunday":
		return 6

weekdayslist = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]


#TODO: main parse function to transfer a line to the schedule we want.
def parse_lines_time(line):
	if(line[1]==""):
		print("program path missing")
		sys.exit(0)
	exec_part = line[1].split(" ",1)
	path = exec_part[0]
	if(len(exec_part)==1):
		parameters = ""
	else:
		parameters = exec_part[1]
	date = time_start.day
	year = time_start.year
	month = time_start.month
	minute = time_start.minute
	second = time_start.second
	if(line[0][0]=='a'):
		final_list = []
		at_time = []
		time_string_0 = line[0].split(" ")
		time_string = time_string_0[1].split(",")
		for x in time_string:
			if(not x.isdigit()):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			if(len(x)!=4):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			if(int(x[0:2])>23 or int(x[2:4])>59):
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			today_clocks = datetime.datetime(year,month,date,int(x[0:2]),int(x[2:4]),0)
			at_time.append(today_clocks)
		for y in at_time:
			if y < time_start:
				y = y+datetime.timedelta(days=1)
				new_schedule = schedule_var_0('A',y,path,parameters)
				final_list.append(new_schedule)
			
			else:
				new_schedule = schedule_var_0('A',y,path,parameters)
				final_list.append(new_schedule)
		return final_list
	if(line[0][0]=='e'):
		final_list=[]
		every_weekday = []
		every_hour_minute = []
		time_string_0 = line[0].split(" ")
		weekday_string = time_string_0[1].split(",")
		hour_string = time_string_0[3].split(",")
		if(len(weekday_string)!=len(set(weekday_string))):
			line_num = line[0]+line[1]
			print(f"error in configuration file: {line_num}")
			sys.exit(0)
		for i in weekday_string:
			if(not(i in weekdayslist)):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			every_weekday.append(String_to_weekday(i))
		for j in hour_string:
			if(not j.isdigit()):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			if(len(j)!=4):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			if(int(j[0:2])>23 or int(j[2:4])>59):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			every_hour_minute.append([int(j[0:2]),int(j[2:4])])
		for a in every_weekday:
			for b in every_hour_minute:
				new_schedule = schedule_var_1('E',a,b[0],b[1],0,path,parameters)
				final_list.append(new_schedule)
		return final_list

	if(line[0][0]=='o'):
		final_list=[]
		time_string_0 = line[0].split(" ")
		weekday_string = time_string_0[1].split(",")
		hour_string = time_string_0[3].split(",")
		the_weekday = []
		the_hours_minute = []
		if(len(weekday_string)!=len(set(weekday_string))):
			line_num = line[0]+line[1]
			print(f"error in configuration file: {line_num}")
			sys.exit(0)
		for i in hour_string:
			if(not i.isdigit()):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			if(len(i)!=4):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			if(int(i[0:2])>23 or int(i[2:4])>59):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			the_hours_minute.append([int(i[0:2]),int(i[2:4])])
		for x in weekday_string:
			if(not(x in weekdayslist)):
				line_num = line[0]+line[1]
				print(f"error in configuration file: {line_num}")
				sys.exit(0)
			the_weekday.append(String_to_weekday(x))
		for y in the_weekday:
			temp_day = next_weekday(time_start,y)
			for k in the_hours_minute:
				if(time_start.weekday() == y and time_start.hour < k[0]):
					if(time_start.hour==k[0]):
						if(time_start.minute < k[0]):
							true_date = datetime.datetime(time_start.year,time_start.month,time_start.day,k[0],k[1],0)
							new_schedule = schedule_var_0('O',true_date,path,parameters)
							final_list.append(new_schedule)
							continue
					else:
						true_date = datetime.datetime(time_start.year,time_start.month,time_start.day,k[0],k[1],0)
						new_schedule = schedule_var_0('O',true_date,path,parameters)
						final_list.append(new_schedule)
						continue	
				true_date =datetime.datetime(temp_day.year,temp_day.month,temp_day.day,k[0],k[1],0)
				new_schedule = schedule_var_0('O',true_date,path,parameters)
				final_list.append(new_schedule)
		return final_list

#TODO:define an empty schedule.
the_schedule = []

def handler(frame,number):
	the_status_messages.extend(the_ran_message)
	the_status_messages.extend(the_error_message)
	the_thing_to_write = sorted(the_status_messages)
	f_write_status = open(A,"w")
	for i in the_thing_to_write:
		f_write_status.write(i)
		f_write_status.write("\n")
	f_write_status.close()


	

#TODO: We finally store every schedule class no matter 0/1 in schedule. now we can access to the date or message in our main loop.
for o in parsed_lines:
	the_schedule.append(parse_lines_time(o))

schedule = []

for a in the_schedule:
	for b in a:
		schedule.append(b)

check_duplicate = []
for k in schedule:
	if(k.start == 'A' or k.start == 'O'):
		check_duplicate.append([k.date.weekday(),k.date.hour,k.date.minute])
	if(k.start == 'E'):
		check_duplicate.append([k.weekday,k.hour,k.minute])
dupli_num = 0

check_duplicate_2 = check_duplicate
for m in check_duplicate_2:
	for n in check_duplicate:
		if(m==n):
			dupli_num+=1
if(dupli_num>1):
	print("double time error")
	sys.exit(0)

the_ran_message = []

the_error_message = []

#TODO:Main loop for the system to continue to run/check time, if time in the schedule, we open a subprogram to execute the program we want.
while True:
	time_now = datetime.datetime.now()
	the_status_messages=[]
	for i in schedule:
		pid = os.fork()
		if(pid == 0):
			if(i.start =='A'):
				if(time_now.day==i.date.day and time_now.hour==i.date.hour and time_now.minute==i.date.minute and time_now.second==0):#if time equals , we in the child process will do the program.
					if(i.para==""):
						try:
							os.execv(i.path,(' ',))
						except Exception:
							sys.exit(2)
					else:
						try:
							os.execv(i.path,(i.path,i.para))
						except Exception:
							sys.exit(2)
				else:#if time not equal the child will simply exit.
					sys.exit(3)
			if(i.start =='E'):
				if(time_now.weekday()==i.weekday and time_now.hour==i.hour and time_now.minute==i.minute and time_now.second==0):#weekday equals and hours and minutes equal will do, cuz it runs every week.
					if(i.para==""):
						try:
							os.execv(i.path,(' ',))
						except Exception:
							sys.exit(2)
					else:
						try:
							os.execv(i.path,(i.path,i.para))
						except Exception:
							sys.exit(2)
				else:
					sys.exit(3)
			if(i.start=='O'):
				if(time_now.day == i.date.day and time_now.hour==i.date.hour and time_now.minute==i.date.minute and time_now.month == i.date.month and time_now.year==i.date.year and time_now.second==0):
					if(i.para==""):
						try:
							os.execv(i.path,(' ',))
						except Exception:
							sys.exit(2)
					else:
						try:
							os.execv(i.path,(i.path,i.para))
						except Exception:
							sys.exit(2)
				else:
					sys.exit(3)
		else:#here we back to main process, while we are still in the loop we can still access the variable
			check_succeeded = os.waitpid(pid,0)#we use the waitpid() to see if the child process doing right.
			if(check_succeeded[1] == 512 or check_succeeded[1] == 256):#if child is having error which will return -1, we can add i's error message to the status.
				if(i.start=='E'):
					the_error_message.append(i.get_error_message(time_now))
				else:
					the_error_message.append(i.error_message)
					i.runned = True
			if(check_succeeded[1]==768):
				if(i.start=='E'):
					the_status_messages.append(i.get_will_run_message(time_now))
				else:
					if(i.runned):
						continue
					the_status_messages.append(i.will_run_message)
			if(check_succeeded[1]==0):
					if(i.start=='E'):
						the_ran_message.append(i.get_ran_message(time_now))
					else:
						the_ran_message.append(i.ran_message)
						i.runned = True
	time.sleep(1)
	signal.signal(signal.SIGUSR1,handler)#after we loop all schedule class, check if we get the signal,if so, just use handler to write the schedule_message to sttatus file.
	e_num = 0
	for x in schedule:
		if(x.start == "E"):
			e_num += 1
	Terminate_var = False
	if(e_num == 0):
		runned_num = 0
		for a in schedule:
			if(a.runned):
				runned_num+=1
			if(runned_num==len(schedule)):
				Terminate_var = True
	
	if(Terminate_var):
		print("nothing left to run")
		break






		
		











		


	
