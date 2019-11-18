import boto3

s3 = boto3.resource('s3')
s3cli = boto3.client('s3')

# fetch bucket name
for bucket in s3.buckets.all():
    buck = bucket.name
    print (bucket.name)

# check all things in bucket
for file in s3.Bucket(buck).objects.all():
    print (file.key)

# this removes All items inside bucket, not bucket itself
s3.Bucket(buck).objects.delete()

# now this deletes the bucket
s3cli.delete_bucket(Bucket=buck)
