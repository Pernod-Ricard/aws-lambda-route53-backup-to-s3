# AWS Lambda Route53 Backup to S3
Simple AWS Lambda function written in Python3 to backup Route53 records in a S3 bucket.

The S3 bucket will have the following structure : S3Bucket/YYYY/<MM/DD/zoneName.export.json

# Usage
- Create a new Lambda function and specify Python 3.x
- Upload the file lambda_function.py that contains the source code of the Lambda functions
- Assign the Lambda a role that has following policies: 
  1. AmazonRoute53ReadOnlyAccess (AWS Managed policy)
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "route53:Get*",
                "route53:List*",
                "route53:TestDNSAnswer"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
  }
  ```
  2. Write permissions over the S3 bucket you want to save your Route53 records to : 
  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "VisualEditor0",
              "Effect": "Allow",
              "Action": [
                  "s3:PutObject"
              ],
              "Resource": [
                  "arn:aws:s3:::your_bucket_name_here/*",
                  "arn:aws:s3:::your_bucket_name_here"
              ]
          }
      ]
  }
  ```
- Add an Environment Variable named **S3_BUCKET_NAME** that contains the name of the S3 bucket you want to backup your files to. Do not forget it or this will trigger an error.
- Add a Cloud Watch Event to schedule the function to run every day (for example). This step is not mandatory, but normally you might want your backups to run automatically

# Warning
This script only captures basic record sets.

Shall you need to capture health checks or traffic policies, you might want to improve this script as it currently does not support it.
    
 
