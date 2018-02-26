# AWS WAF Sample Log to S3

Schedule and auto export AWS WAF Sample log to S3


# How to use

## AWS SAR(Serverless Application Repository) deploy

## AWS SAM(Serverless Application Model) deploy
```
#package SAM template
aws cloudformation package --template-file template.yml --s3-bucket *bucketname* --output-template-file packaged-template.yml
#Deploy the pakcaged template 
aws cloudformation deploy --template-file /*Path*/AWSwafSampleLog2s3/packaged-template.yml --stack-name waflog2s3 --capabilities CAPABILITY_IAM

```
## Manual deploy at console
# License
 
MIT License (MIT)
This software is released under the MIT License, see LICENSE.txt
