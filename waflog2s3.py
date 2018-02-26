'''
***Create IAM Policy and Role before build this lambda***

IAM Role for lambda.
IAM Policy for role:
Premission we need are as below:
	logs:CreateLogGroup
	logs:CreateLogStream
	logs:PutLogEvents
	waf:GetSampledRequests or waf-regional:GetSampledRequests
	s3:PutObject

Event input:
	webaclid		Get your WAF Web ACL ID from event
	ruleid			Get your WAF Web rules ID from event

Event Sample:
{
  "webaclid": "xxxxxxxx-xxxx-xxxx-xxxx-145594c6a725",
  "ruleids": [
    "xxxxxxxx-xxxx-xxxx-xxxx-b90cd6bd4671",
    "xxxxxxxx-xxxx-xxxx-xxxx-739c22c867bb"
  ]
}

Environment variables most setting up for this function:
	first_item_num	Setting the max number record that you want forward to s3, and max of the number is 5000
	bucket_name		Bucket which you want to store the WAF sample logs
	interval_time	interval time of pulling WAF API (Unit: minute)

'''
import boto3
import os
import json
from datetime import datetime
from datetime import timedelta
# extend JSONEncoder for complex datetime type
class CplxDatetimeEncode(json.JSONEncoder):
	def default(self, obj):
		# chk format and return fromated time str
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		# return error such as type error
		return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
	print('Loading function')
	# create client to connect AWS service
	# waf_regional = boto3.client('waf-regional')
	waf = boto3.client('waf')
	s3 = boto3.client('s3')
	
	# get WAF acl and rule variables for 'get_sampled_requests()' from event body
	aclid = event['webaclid']
	ruleids = event['ruleids']
	
	# get serveral variables for 'get_sampled_requests()' from os env
	item_num = int(os.environ['item_num'])
	interval_time = int(os.environ['interval_time'])
	bucket_name =  os.environ['bucket_name']
	
	# using datetime to create the start&end time for 'waf.get_sampled_requests()'
	# if necessary you can modify timedelta() to get time window size u want
	end_time = datetime.now()
	start_time = end_time - timedelta(minutes=interval_time)
	
	# print start & end time for check timezone is OK
	# if timezone is wrong , modify the datetime.now() to datetime.utcnow() or datetime.now([tz]).
	# print(start_time,end_time)
	
	# get each rule id from WebACL
	while(len(ruleids) > 0):
		ruleid = ruleids.pop()
		# get sample log from aws waf
		waf_response = waf.get_sampled_requests(
		    WebAclId=aclid,
		    RuleId=ruleid,
		    TimeWindow={
		        'StartTime': start_time,
		        'EndTime': end_time
		    },
		    MaxItems= item_num
		)
	
		# print waf_response for log at cw logs and troubleshooting
		# print(waf_response)
		# transform format from dict to json
		waf_sample_logs = json.dumps(waf_response['SampledRequests'],cls=CplxDatetimeEncode)
		print(waf_sample_logs)
		
		# create s3 path
		path =  ("/".join([aclid,ruleid,str(start_time)])) 
	
		# change waf_response type from 'dict' type to 'string' type then encode to 'bytes' type
		byte_waf_logs = str(waf_sample_logs).encode()
		
		# put waf response to s3 
		s3_response = s3.put_object(
			Body=byte_waf_logs,
			Bucket=bucket_name,
			Key=path
		)
		
		# print s3_response for log at cw logs and troubleshooting
		print(s3_response)