#!/usr/bin/env python3
# -*- coding: ascii -*-

import sys, os,signal,time

import os.path

pidfile = os.path.expanduser('~/.runner-pid')
statusfilename = os.path.expanduser('~/.runner.status')
#TODO:try open the pid file to get runner's pid. if the file not exits, exit and print error message.
try:
    f_runner_pid = open(pidfile,"r")
except(FileNotFoundError):
    print(f"file {pidfile} not found error")
    sys.exit(0)

#TODO:read the pid of the runner.
pid = f_runner_pid.readline()

f_runner_pid.close()



#TODO: send SIGUSR1 to the runner.
os.kill(int(pid),signal.SIGUSR1)

time.sleep(1)

try:
    f_runner_status = open(statusfilename,"r")
except FileNotFoundError:
    print(f"file {statusfilename} not found error")
    sys.exit(0)

if(os.stat(statusfilename)==0):
    time.sleep(5)
if(os.stat(statusfilename)==0):
    print("status timeout")
    sys.exit(0)

else:

    the_lines = f_runner_status.readlines()
    for i in the_lines:
        i.strip()
        print(i)
    f_runner_status.close()

    f_final_status = open(statusfilename,"w")

    f_final_status.write("")

    f_final_status.close()











#
# open the pidfile and read the process id
#    give an error message if file not found or bad pid
# send the USR1 signal to runner.py
# open the status file for reading and check the size
# wait until it is non zero size, then read contents and copy to output, then quit.
#
# give error messages as necessary


