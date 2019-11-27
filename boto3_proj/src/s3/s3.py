import json
import threading
import os
import sys
from boto3.s3.transfer import TransferConfig


# created a seperate class for the actions requiring an s3 resource call
# not sure if it is good practice, but it works and is readable
class S3_Res:
    def __init__(self, resource):
        self._resource = resource
    
    def multi_part_file_upload(self, file_path, bucket_name, file_name):
        config = TransferConfig(
            multipart_threshold=1024 * 25,
            max_concurrency=10,
            multipart_chunksize=1024 * 25,
            use_threads=True
        )
        key_path = 'multipart_files/automating_the_boring_stuff.pdf'
        
        print ('Uploading big file ...')
        return self._resource.meta.client.upload_file(
            file_path,
            bucket_name,
            key_path,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/pdf'},
            Config=config,
            Callback=UploadProgress(file_path, file_name)
        )


class UploadProgress(object):
    # properties of the object, populated in the init method
    def __init__(self, filepath, filename):
        self._filepath = filepath
        self._filename = filename
        # get the actual file size
        self._size = float(os.path.getsize(filepath))
        # progress so far
        self._upload_so_far = 0
        # lock the threading process from python so only this uses the function
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._upload_so_far += bytes_amount
            # calculate percentage
            percentage = (self._upload_so_far / self._size) * 100
            # output for the above setup in a system tag
            sys.stdout.write(
                f'\r%s %s / %s (%.2f%%)' % (
                        self._filename, self._upload_so_far, self._size, percentage
                    )
            )
            sys.stdout.flush()


class S3:
    def __init__(self, client):
        self._client = client
       
    def create_bucket(self, bucket_name):
        print ('Creating S3 bucket ...')
        return self._client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-2'
            }
        )

    def create_bucket_policy(self, bucket_name):
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:*"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        policy_string = json.dumps(bucket_policy)

        print ('Creating bucket policy ...')
        return self._client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_string
        )

    def list_buckets(self):
        return self._client.list_buckets()

    def get_properties(self, bucket_name):
        return self._client.get_bucket_policy(
            Bucket=bucket_name
        )
    
    def get_encryption(self, bucket_name):
        return self._client.get_bucket_encryption(
            Bucket=bucket_name
        )

    def update_bucket_policy(self, bucket_name):
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:DeleteObject",
                        "s3:GetObject",
                        "s3:PutObject"
                    ],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        policy_string = json.dumps(bucket_policy)

        print ('Creating bucket policy ...')
        return self._client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_string
        )


    def create_encryption(self, bucket_name):
        return self._client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        )

    def single_part_file_upload(self, file_path, bucket_name):
        print ('Uploading tiny file ...')
        return self._client.upload_file(file_path, bucket_name, 'readme.txt')

    def versioning_enable(self, bucket_name):
        print ('Enabling file versioning ...')
        return self._client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
    
    def lifecycle_policy(self, bucket_name):
        # rules for moving specified files to Glacier (the one with the readme prefix)
        # and a rule for backing up everything that has been versioned and not the latest file
        lifecycle_policy = {
            "Rules": [
                {
                    "ID": "Move file to Glacier",
                    "Prefix": "readme",
                    "Status": "Enabled",
                    "Transition": {
                        "Date": "2020-01-05T00:00:00.000Z",
                        "StorageClass": "GLACIER"
                        }
                },
                {
                    "ID": "Move old versions to Glacier",
                    "Status": "Enabled",
                    "Prefix": "",
                    "NoncurrentVersionTransition": {
                            "NoncurrentDays": 2,
                            "StorageClass": "GLACIER"
                        }
                }
            ]
        }
        print ('Assigning Lifecycle policy ...')
        return self._client.put_bucket_lifecycle(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )

    def destroy_bucket(self, bucket_name):
        print ('Destroying bucket ...')
        return self._client.delete_bucket(
            Bucket=bucket_name
        )
