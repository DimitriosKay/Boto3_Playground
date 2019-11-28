from s3.s3 import S3
from s3.s3 import S3_Res
from client_locator import S3Client
from resource_locator import S3Resource
from botocore.exceptions import ClientError
import os.path

s3_client = S3Client().get_client()
s3_resource = S3Resource().get_resource()

s3 = S3(s3_client)
s3_res = S3_Res(s3_resource)

# bucket name variable
bucket_name = 'fresh-bucket-but-boto3-2019'
web_bucket_name = 'fresh-boto3-webpage'

def main():

    # s3 bucket creation
    new_bucket_response = s3.create_bucket(bucket_name)
    print (f'{bucket_name} was created !')
    print (f'\n{new_bucket_response}')

    # bucket policy creation and attachment
    bucket_policy_response = s3.create_bucket_policy(bucket_name)
    print (f'Policy for {bucket_name} has been created')
    #print (bucket_policy_response)


def update_bucket_policy():
    policies_response = s3.update_bucket_policy(bucket_name)
    print (f'Policies for {bucket_name} have been updated')

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

def upload_small_file():
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/readme.txt'
    s3.single_part_file_upload(file_path, bucket_name)
    print (f'File "readme.txt" from "{file_path}" was uploaded to {bucket_name}')

def upload_big_file():
    file_name = 'automate_the_boring_stuff.pdf'
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/uploads/automate_the_boring_stuff.pdf'
    s3_res.multi_part_file_upload(file_path, bucket_name, file_name)
    print (f'\nFile "{file_name}" from "{file_path}" was uploaded to {bucket_name}/multipart_files')
   
def enable_versioning():
    versioning_response = s3.versioning_enable(bucket_name)
    print (f'Versioning for {bucket_name} has been enabled')

def enable_lifecycle_policy():
    lifecycle_response = s3.lifecycle_policy(bucket_name)
    print (f'Lifecycle policies have been added to {bucket_name}')
    #print (lifecycle_response)


def empty_bucket():
    s3_res.delete_files(bucket_name)
    print (f'Bucket "{bucket_name}" has been emptied')

# destroy bucket
def destroy_bucket():
    s3.destroy_bucket(bucket_name)
    print (f'{bucket_name} was destroyed.')


def check_available():
    return s3_res.check_available(web_bucket_name)

def deploy_webpage():
    index_file = os.path.dirname(__file__) + 'index.html'
    error_file = os.path.dirname(__file__) + 'error.html'

    #print (type(check_available))
    
    if check_available() is True:
        print ('Bucket exists, updating contents')
        s3.host_static_website(index_file, error_file, web_bucket_name) 
    elif check_available() is False:
        print ('Creating bucket')
        s3.create_bucket(web_bucket_name)
        s3.update_bucket_policy(web_bucket_name)
        s3.host_static_website(index_file, error_file, web_bucket_name)
        print (f'Go to "{web_bucket_name}.s3-website.eu-west-2.amazonaws.com" to check out your website')


if __name__ == "__main__":
    # Create S3 infrastructure
    '''
    main()
    manage_buckets()
    update_bucket_policy()
    upload_small_file()
    upload_big_file()
    enable_versioning()
    enable_lifecycle_policy()
    '''

    # Deploy bucket hosted webpage
    #check_available()
    deploy_webpage()

    # Destroy S3 infrastructure
    #empty_bucket()
    #destroy_bucket()
