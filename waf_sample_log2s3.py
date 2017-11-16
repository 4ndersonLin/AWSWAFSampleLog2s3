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

Environment variables most setting up for this function:
	webaclid		Get your WAF Web ACL ID by using CLI tool 'aws waf list-web-acls'
	ruleid			Get your WAF Web ACL ID by using CLI tool 'aws waf list-rules'
	first_item_num	Setting the max number record that you want forward to s3, and max of the number is 5000
	bucket_name		Bucket which you want to store the WAF sample logs

'''
import boto3
import os
from datetime import datetime
from datetime import timedelta


print('Loading function')

#create client to connect AWS service
#waf_regional = boto3.client('waf-regional')
waf = boto3.client('waf')
s3 = boto3.client('s3')


def lambda_handler(event, context):
	
	#get several variables for 'get_sampled_requests()' from environment variables
	aclid = os.environ['webaclid']
	ruleid = os.environ['ruleid']
	first_item_num = int(os.environ['first_item_num'])

	#using datetime to create the start&end time for 'get_sampled_requests()'
	#if necessary you can modify timedelta() to get time window size u want
	end_time = datetime.now()
	start_time = end_time - timedelta(minutes=5)
	
	#print start & end time for check timezone is OK
	#if timezone is wrong , modify the datetime.now() to datetime.utcnow() or datetime.now([tz])
	#print(start_time,end_time)
	
	#get sample log from aws waf
	waf_response = waf.get_sampled_requests(
	    WebAclId=aclid,
	    RuleId=ruleid,
	    TimeWindow={
	        'StartTime': start_time,
	        'EndTime': end_time
	    },
	    MaxItems= first_item_num
	)

	#print waf_response for log at cw logs and troubleshooting
	print(waf_response)

	#create s3 path
	path =  ("/".join([aclid,ruleid,str(start_time)]))

	#get s3 bucket name from environment variables
	bucket_name =  os.environ['bucket_name']

	#change waf_response type from 'dict' type to 'string' type then encode to 'bytes' type
	byte_waf_response = str(waf_response).encode()

	#put waf response to s3
	s3_response = s3.put_object(
		Body=byte_waf_response,
		Bucket=bucket_name,
		Key=path
	)
	
	#print s3_response for log at cw logs and troubleshooting
	print(s3_response)