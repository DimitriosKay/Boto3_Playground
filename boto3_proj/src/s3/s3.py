import json
from boto3.s3.transfer import TransferConfig

# created a seperate class for the actions requiring an s3 resource call
# not sure if it is good practice, but it works and is readable
class S3_Res:
    def __init__(self, resource):
        self._resource = resource
    
    def multi_part_file_upload(self, file_path, bucket_name):
        config = TransferConfig(
            multipart_threshold=1024 * 25,
            max_concurrency=10,
            multipart_chunksize=1024 * 25,
            use_threads=True
        )
        key_path = 'multipart_files/big_doc.docx'
        
        print ('Uploading big file ...')
        return self._resource.meta.client.upload_file(
            file_path,
            bucket_name,
            key_path,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/pdf'},
            Config=config
        )

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

    
    def destroy_bucket(self, bucket_name):
        print ('Destroying bucket ...')
        return self._client.delete_bucket(
            Bucket=bucket_name
        )
