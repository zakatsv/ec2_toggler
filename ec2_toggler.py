#!/usr/bin/python

'''
A script to start/stop EC2 instance depending on the value of the work_hours instance tag
Written by ArtemF
Version 1.0
'''

import subprocess
import json
import datetime
import re

status_code = ''
work_hours = ''
now = ''
start_time = ''
stop_time = ''


ins_id = 'i-0ea7e0158c98e3765'
cli_get_status = "aws ec2 describe-instance-status --include-all-instances --instance-id " + ins_id
cli_get_tag = "aws ec2 describe-tags --filters \"Name=resource-id,Values=" + ins_id + "\""
cli_start_ins = "aws ec2 start-instances --instance-ids " + ins_id
cli_stop_ins = "aws ec2 stop-instances --instance-ids " + ins_id

def get_status_code():
  global status_code
  cli_output = subprocess.check_output(['bash','-c', cli_get_status])
  data = json.loads(cli_output)
  status_code = data['InstanceStatuses'][0]['InstanceState']['Code']

def get_work_hours():
  global work_hours
  cli_output = subprocess.check_output(['bash','-c', cli_get_tag])
  data = json.loads(cli_output)
  work_hours = data['Tags'][1]['Value']

def analyze_work_hours():
  global work_hours
  global now
  global start_time
  global stop_time
  now = datetime.datetime.now()
  stamps = re.split(r'[-:]', work_hours)
  start_time = now.replace(hour=int(stamps[0]), minute=int(stamps[1]))
  stop_time = now.replace(hour=int(stamps[2]), minute=int(stamps[3]))

if __name__ == "__main__":
  get_status_code()
  get_work_hours()
  analyze_work_hours()
  print status_code
  print work_hours
  print now
  print start_time
  print stop_time
