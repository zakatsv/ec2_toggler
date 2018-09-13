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

code = ''
tag = ''

ins_id = 'i-0ea7e0158c98e3765'
cli_get_status = "aws ec2 describe-instance-status --include-all-instances --instance-id " + ins_id
cli_get_tag = "aws ec2 describe-tags --filters \"Name=resource-id,Values=" + ins_id + "\""
#print cli_get_tag

def get_status_code():
  global code
  cli_output = subprocess.check_output(['bash','-c', cli_get_status])
  data = json.loads(cli_output)
  code = data['InstanceStatuses'][0]['InstanceState']['Code']

def get_work_hours():
  global tag
  cli_output = subprocess.check_output(['bash','-c', cli_get_tag])
  data = json.loads(cli_output)
  tag = data['Tags'][1]['Value']

if __name__ == "__main__":
  get_status_code()
  get_work_hours()
  print code
  print tag



#if __name__ == "__main__":
