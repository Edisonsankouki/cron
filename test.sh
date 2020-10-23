#!/bin/bash
echo "every Wednesday,Wednesday,Tuesday at 1200,1100 run /bin/date" > ~/.runner.conf
test1="$(python3 runner.py &)"
if [ "$test1" == 'error in configuration file: every Wednesday,Wednesday,Tuesday at 1200,1100/bin/date' ];
then
    echo "test1 passed"
else
    echo "test1 failed"
fi
echo "" > ~/.runner.conf
test2="$(python3 runner.py &)"
if [ "$test2" == 'empty line detected' ];
then
    echo "test2 passed"
else
    echo "test2 failed"
fi
cat /dev/null   > ~/.runner.conf
test3="$(python3 runner.py &)"
if [ "$test3" == 'configuration file empty' ];
then
    echo "test3 passed"
else
    echo "test3 failed"
fi
echo "every Friasdasd at 1100 run /bin/dat" > ~/.runner.conf
test4="$(python3 runner.py &)"
if [ "$test4" == 'error in configuration file: every Friasdasd at 1100/bin/dat' ];
then
    echo "test4 passed"
else
    echo "test4 failed"
fi
echo "every Tuesday at 1112234000 run /bin/date" > ~/.runner.conf
test5="$(python3 runner.py &)"
if [ "$test5" == 'error in configuration file: every Tuesday at 1112234000/bin/date' ];
then
    echo "test5 passed"
else
    echo "test5 failed"
fi
echo "on Tuesday at 1100 /bin/date" > ~/.runner.conf
test6="$(python3 runner.py &)"
if [ "$test6" == 'error in configuration file: on Tuesday at 1100 /bin/date' ];
then
    echo "test6 passed"
else
    echo "test6 failed"
fi
echo "on every Tuesday at 1100 run /bin/dat" > ~/.runner.conf
if [ "$test6" == 'error in configuration file: on Tuesday at 1100 /bin/date' ];
then
    echo "test6 passed"
else
    echo "test6 failed"
fi
echo "on Tuesday at 2800 run /bin/echo" > ~/.runner.conf
test7="$(python3 runner.py &)"
if [ "$test7" == 'error in configuration file: on Tuesday at 2800/bin/echo' ];
then
    echo "test7 passed"
else
    echo "test7 failed"
fi
echo "on Monday at 1700,1800 run /bin/date" > ~/.runner.conf
echo "on Monday at 1700,1800 run /bin/date" >> ~/.runner.conf
test8="$(python3 runner.py &)"
if [ "$test8" == 'duplicate run time' ];
then
    echo "test8 passed"
else
    echo "test8 failed"
fi
echo "on Tuesday at 1290 run /bin/date" > ~/.runner.conf
test9="$(python3 runner.py &)"
if [ "$test9" == 'error in configuration file: on Tuesday at 1290/bin/date' ];
then
    echo "test9 passed"
else
    echo "test9 failed"
fi
echo "on Friday at 1200 run /bin/date" > ~/.runner.conf
echo "every Friday at 1100,1200 run /bin/date">> ~/.runner.conf
test10="$(python3 runner.py &)"
if [ "$test10" == 'double time error' ];
then
    echo "test10 passed"
else
    echo "test10 failed"
fi
echo Now doing correct result test
echo Correct result 1
echo "do the test on 12:00 Friday"
echo "every Tuesday at 1100 run /bin/echo hello world" > ~/.runner.conf
echo "on Tuesday,Wednesday,Friday at 1300,1500 run /bin/date">> ~/.runner.conf
python3 runner.py &
sleep 2
var1="$(python3 runstatus.py)"
expected_output=$"will run at Fri Oct 23 13:00:00 2020 /bin/date\n\nwill run at Fri Oct 23 15:00:00 2020 /bin/date\n\nwill run at Tue Oct 27 11:00:00 2020 /bin/echo hello world\n\nwill run at Tue Oct 27 13:00:00 2020 /bin/date\n\nwill run at Tue Oct 27 15:00:00 2020 /bin/date\n\nwill run at Wed Oct 28 13:00:00 2020 /bin/date\n\nwill run at Wed Oct 28 15:00:00 2020 /bin/date"
echo the expected output is:
echo -e "$expected_output"
echo the actual output is:
echo "$var1"
echo Correct result 2
echo "do the test on 12:00 Friday"
echo "on Friday at 1201 run /bin/date" > ~/.runner.conf
python3 runner.py &
sleep 60
var2="$(python3 runstatus.py)"
echo the actual output is:
echo "$var2"
echo "check if it is ran at XXX format"
echo Correct result 3
echo "do the test on 12:10 Friday"
echo "at 12:11 run /bin/echo hello" > ~/.runner.conf
python3 runner.py &
sleep 60
var3="$(python3 runstatus.py)"
echo the actual output is:
echo "$var3"
echo "check if it is ran at XXX format"
echo Correct result 3
echo "do the test on 12:12 Friday with date result"
echo "every Friday at 12:13 run /bin/echo hello" > ~/.runner.conf
python3 runner.py &
sleep 60
var4="$(python3 runstatus.py)"
echo the actual output is:
echo "$var4"
echo "check if it is ran at XXX format with hello"
echo Correct result 4
echo "do the test on 12:14 Friday"
echo "every Friday at 12:15 run /bin/asdasdasd" > ~/.runner.conf
python3 runner.py &
sleep 60
var4="$(python3 runstatus.py)"
echo the actual output is:
echo "$var4"
echo "check if it is error at XXX format"
echo Correct result 5
echo "do the test on 12:20 Friday"
echo "at 12:21 run /bin/date" > ~/.runner.conf
echo "at 12:22 run /bin/date" > ~/.runner.conf
python3 runner.py &
echo "check if the message no process to run comes out"
sleep 180








