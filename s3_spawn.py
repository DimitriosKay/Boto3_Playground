import boto3

# resource works with create, but client is required by internal things like list and upload. Not sure exactly how that relates
s3 = boto3.client('s3')

bname = 'freshnewbucky'

# Bucket is the method to name your bucket, other one is to bypass error 
s3.create_bucket(Bucket=bname, CreateBucketConfiguration={'LocationConstraint':'eu-west-2'})

# list buckets (so far it lsits all details on the ones available)
print (s3.list_buckets())

# syntac for uploading files [from which file] [which bucket] [to file]
s3.upload_file('swag.txt', bname, 'swag.txt')
