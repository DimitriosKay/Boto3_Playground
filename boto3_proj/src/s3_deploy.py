from s3.s3 import S3
from client_locator import S3Client
from botocore.exceptions import ClientError

s3_client = S3Client().get_client()

s3 = S3(s3_client)

# bucket name variable
bucket_name = 'fresh-bucket-but-boto3-2019'


def main():

    # s3 bucket creation
    new_bucket_response = s3.create_bucket(bucket_name)
    print (f'{bucket_name} was created !')
    print (f'\n{new_bucket_response}')

    # bucket policy creation and attachment
    bucket_policy_response = s3.create_bucket_policy(bucket_name)
    print (f'Policy for {bucket_name} has been created')
    print (bucket_policy_response)

def manage_buckets():

    # list buckets
    bucky_list = s3.list_buckets()
    for x in bucky_list['Buckets']:
        print(x)

    print ('\n')

    properties_response = s3.get_properties(bucket_name)
    print (f'Policies for "{bucket_name}" bucket:\n{properties_response["Policy"]}')

    print ('\n')

    try:
        encryption_response = s3.get_encryption(bucket_name)
    except ClientError as e:
        # check how the error syntax looks
        #print (e.response['Error']['Code'])
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            print (f'Error: Encryption protocol was not found for "{bucket_name}"')
            prompt = input('Do you want to encrypt it [Y/n]?: ')
            if prompt == 'Y':
                encrypt_response = s3.create_encryption(bucket_name)
                print (encrypt_response)
    else:
        print (f'Encryption for "{bucket_name}" bucket:\n{encryption_response}')


# destroy bucket
def destroy_bucket():

    s3.destroy_bucket(bucket_name)
    print (f'{bucket_name} was destroyed.')

if __name__ == "__main__":
    #main()
    manage_buckets()
    #destroy_bucket()
