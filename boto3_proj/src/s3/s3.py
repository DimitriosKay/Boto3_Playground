import json

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

    def destroy_bucket(self, bucket_name):
        print ('Destroying bucket ...')
        return self._client.delete_bucket(
            Bucket=bucket_name
        )
