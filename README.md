# AWS WAF Sample Log to S3

Schedule and auto export AWS WAF Sample log to S3

# How to use
Provide three way to deploy those resource.
1. AWS SAR(Serverless Application Repository)
2. AWS SAM(Serverless Application Model)
3. Manually deploy at console
## AWS SAR(Serverless Application Repository) deploy
Select "Serverless Application Repository" when you create lambda at create function step.
Key word: WAF

## AWS SAM(Serverless Application Model) deploy
```
#package SAM template
aws cloudformation package --template-file template.yml --s3-bucket your-bucketname --output-template-file packaged-template.yml
#Deploy the pakcaged template 
aws cloudformation deploy --template-file /Local-Path/AWSwafSampleLog2s3/packaged-template.yml --stack-name waflog2s3 --capabilities CAPABILITY_IAM

```
## Manually deploy at console

1. Create IAM Policy
2. Create IAM Role
3. Create Lambda by upload waflog2s3.zip
4. Create CloudWatch event trigger lambda

# License
 
MIT License (MIT)
This software is released under the MIT License, see LICENSE.txt
