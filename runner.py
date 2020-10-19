#!/usr/bin/env python3
# -*- coding: ascii -*-

import sys, os, time, datetime, signal

"""
The configuration file for runner.py will contain one line for each program that is to be run.   Each line has the following parts: 

timespec program-path parameters

where program-path is a full path name of a program to run and the specified time(s), parameters are the parameters for the program,
timespec is the specification of the time that the program should be run.

The timespec has the following format:

[every|on day[,day...]] at HHMM[,HHMM] run

Square brackets mean the term is optional, vertical bar means alternative, three dots means repeated.

Examples:

every Tuesday at 1100 run /bin/echo hello
	every tuesday at 11am run "echo hello"
on Tuesday at 1100 run /bin/echo hello
	on the next tuesday only, at 11am run "echo hello"
every Monday,Wednesday,Friday at 0900,1200,1500 run /home/bob/myscript.sh
	every monday, wednesday and friday at 9am, noon and 3pm run myscript.sh
at 0900,1200 run /home/bob/myprog
	runs /home/bob/myprog every day at 9am and noon


"""

#
# open the configuration file and read the lines, 
#    check for errors
#    build a list of "run" records that specifies a time and program to run
#

#
# define up the function to catch the USR1 signal and print run records
#

#
# sort run records by time
# take the next record off the list and wait for the time, then run the program
# add a record to the "result" list
# if this was an "every" record", add an adjusted record to the "run" list 
#
# repeat until no more to records on the "run" list, then exit
#


#TODO: we create a file contains the pid of the process of runner in order to read it when we run the runner status.
runner_pid = os.getpid()
f_pid = open(".runner-pid","w")
f_pid.write(str(runner_pid))
f_pid.close()

#TODO: read the configuration file to get the programs and time 
lines = [line.strip('\n') for line in open("runner.conf")]
lines.remove('')
def generate_messagelist(line):
	return [x.strip(" ")for x in line.split("run",2)]
parsed_lines = []
for i in lines:
	parsed_lines.append(generate_messagelist(i))
print(parsed_lines)

start_time = time.ctime(time.time()).split(" ")
start_date = start_time[2]
start_weekday = start_time[0]
start_month = start_time[1]
start_hour = start_time[3][0]+start_time[3][1]+start_time[3][3]+start_time[3][4]

next_day_value = False



def exec_line(line):
	time_now = time.ctime(time.time()).split(" ")
	date_now = time_now[2]
	weekday_now = time_now[0]
	hour_now = time_now[3][0]+time_now[3][1]+time_now[3][3]+time_now[3][4]
	if(line[0][1] == 'a'):
		if(date_now==start_date):
			if(int(start_hour)<int(hour_now)):
				message = line[0].split(" ")
				hours = message[1].split(",")
				for x in hours:
					if(x==hour_now):
						os.execl(line[1])
			if(int(start_hour)>int(hour_now)):
				next_day_value=True
		if(next_day_value):
			message = line[0].split(" ")
			hours = message[1].split(",")
			for x in hours:
				if(x==hour_now):
					os.execl(line[1])
			next_day_value=False

	

	elif(line[0][1] == 'o'):
		message0 = line[0].split(" ")
		weekdays =message0[1].split(",")
		hours=message0[3].split(",")


	elif(line[0][1] == 'e'):
		message1 = line[0].split(" ")
		weekdays0 =message0[1].split(",")
		hours=message0[3].split(",")
		weekdays = []
		for i in weekdays0:
			weekdays.append(i[0:3])
		for x in weekdays:
			if(x==weekday_now):
				for y in hours:
					if(y==hour_now):
						os.execl(line[1])
	else:
		pass

	

		
	



while True:
	for line in parsed_lines:
		exec_line(line)
	time.sleep(60)
	
