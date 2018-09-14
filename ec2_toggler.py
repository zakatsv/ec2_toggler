#!/usr/bin/python

'''
A script to start/stop EC2 instance depending on the value of the work_hours instance tag
Written by ArtemF
Version 1.0
'''

'''
Status code reminder:
0 : pending
16 : running
32 : shutting-down
48 : terminated
64 : stopping
80 : stopped
'''

import os
import sys
import subprocess
import json
import datetime
import re
import time

#status_code = ''
#work_hours = ''
#now = ''
#start_time = ''
#stop_time = ''

# DEFINE A VALID INSTANCE ID HERE
ins_id = 'i-0ea7e0158c98e3765'

cli_get_status = "aws ec2 describe-instance-status --include-all-instances --instance-id " + ins_id
cli_get_tag = "aws ec2 describe-tags --filters \"Name=resource-id,Values=" + ins_id + ",Name=key,Values=work_hours\""
cli_start_ins = "aws ec2 start-instances --instance-ids " + ins_id
cli_stop_ins = "aws ec2 stop-instances --instance-ids " + ins_id

def toggle_instance(cmd):
  cli_output = subprocess.check_output(['bash','-c', cmd])
  #sleep for 5 secs and re-run the script to confirm the status
  time.sleep(5)
  os.execv(sys.executable, ['python'] + sys.argv)

def get_status_code():
  global status_code
  cli_output = subprocess.check_output(['bash','-c', cli_get_status])
  data = json.loads(cli_output)
  try:  
    status_code = data['InstanceStatuses'][0]['InstanceState']['Code']
  except:
    print "Failed to get the status code"
    exit(1)

def get_work_hours():
  global work_hours
  cli_output = subprocess.check_output(['bash','-c', cli_get_tag])
  data = json.loads(cli_output)
  try:
    work_hours = data['Tags'][0]['Value']
  except:
    print "Failed to get the 'work_hours' tag. Check if tag is specified"
    exit(1)

#def generate_timestamps():
#  global now
#  global start_time
#  global stop_time
#  now = datetime.datetime.now()
#  stamps = re.split(r'[-:]', work_hours)
#  start_time = now.replace(hour=int(stamps[0]), minute=int(stamps[1]), second=0, microsecond=0)
#  stop_time = now.replace(hour=int(stamps[2]), minute=int(stamps[3]), second=0, microsecond=0)

def analyze_status_code():
  try:
    if re.match('48', str(status_code)):
      print "The EC2 instance " + ins_id + " is terminated. Changing state is not possible"
      exit(1)
    elif re.match('16', str(status_code)):
      print "instance is running"
      return True
    elif re.match('80', str(status_code)):
      print "instance is stopped"
      return False
    elif re.match('0|32|64', str(status_code)):
      print "instance is pending/shutting-down/stopping. Sleep and retry"
      time.sleep(5)
      get_status_code()
      analyze_status_code()
  except:
    print "Something went wrong. Failed to get a valid status code"
    exit(1)

def analyze_work_hours():
  global now
  global start_time
  global stop_time
  now = datetime.datetime.now()
  stamps = re.split(r'[-:]', work_hours)
  start_time = now.replace(hour=int(stamps[0]), minute=int(stamps[1]), second=0, microsecond=0)
  stop_time = now.replace(hour=int(stamps[2]), minute=int(stamps[3]), second=0, microsecond=0)
  
  if start_time < now < stop_time:
    return True
  else:
    return False

def toggler():
  if analyze_status_code() and analyze_work_hours():
    print "The instance is running as it should"
  elif not analyze_status_code() and not analyze_work_hours():
    print "The instance is stopped as it should be"
  elif (analyze_status_code(), analyze_work_hours()) == (1, 0):
    print "It shold not be running. Stopping..."
    toggle_instance(cli_stop_ins)
  elif (analyze_status_code(), analyze_work_hours()) == (0, 1):
    print "It shold be running. Starting..."
    toggle_instance(cli_start_ins)

if __name__ == "__main__":
  get_status_code()
  get_work_hours()
#  generate_timestamps()
  analyze_status_code()
  analyze_work_hours()
  print status_code, type(status_code)
  print work_hours
  print now
  print start_time
  print stop_time
  toggler()
