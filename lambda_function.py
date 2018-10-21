#!python3
import boto3
import json
import datetime
import os

def lambda_handler(event, context):
    
    # Client intialization
    route53 = boto3.client('route53')
    s3 = boto3.client('s3')
    
    # Variable initialization
    s3_bucket_name = os.environ['S3_BUCKET_NAME']
    
    # Loop through hosted zones using a paginator
    paginator_hosted_zones = route53.get_paginator('list_hosted_zones')
    pages_hosted_zones = paginator_hosted_zones.paginate()
    for page_hosted_zones in pages_hosted_zones:
        hosted_zones = page_hosted_zones['HostedZones']
        for hosted_zone  in hosted_zones:
            print(hosted_zone['Name'] + " - " + str(hosted_zone['ResourceRecordSetCount']) + ' records')
    
            # we loop through records using a paginator
            paginator_record_sets = route53.get_paginator('list_resource_record_sets')
            pages_record_sets = paginator_record_sets.paginate(HostedZoneId=hosted_zone['Id'])
            zone_dump = [] # to store zone output
            for page_record_sets in pages_record_sets:
                # We loop through each record to generate a nice dump
                for record_set in page_record_sets['ResourceRecordSets']:
                    zone_dump.append(record_set)
    
            # We store the output files in s3 (1 file per DNS zone)
            now = datetime.datetime.now()
            key_name = str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + hosted_zone['Name'] + 'export.json'
            s3.put_object(
                Body = json.dumps(zone_dump), 
                Bucket = s3_bucket_name, 
                Key = key_name)
    
    return {
        "statusCode": 200,
        "body": json.dumps('Route53 backup to S3 completed')
    }