import boto3
import logging

logging.basicConfig(filename="mylog.log", level=logging.DEBUG)

# Let's use Amazon S3
s3 = boto3.client('s3')

# create a new bucket.
s3.create_bucket(Bucket='s01bucket')

# upload json file into s00 bucket.
filename= '/Users/srikanth/Documents/timetable.xlsx'
s3.upload_file(filename, 's00bucket', 'timetable.xlsx')

response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
print("Bucket List: %s" % buckets)

s3.download_file('s00bucket', 'testfile.xlsx', '/Users/Srikanth/Desktop/newfile.xlsx')
