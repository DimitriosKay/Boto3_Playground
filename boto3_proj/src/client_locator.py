import boto3

# internal class making the base of the client allocation
class ClientLocator:
    # this init is running self._client which has the boto3 command in
    # with specified region
    def __init__(self, client):
        self._client = boto3.client(client, region_name='eu-west-2')
    # then this one returns the client, mapped with details from next class
    def get_client(self):
        return self._client

# this class allows you to specify which client setup to use
# you would call it with EC2Client, which is nesting the ClientLocator class
class EC2Client(ClientLocator):
    def __init__(self):
        super().__init__('ec2')

# if you want to expand to S£ let's say, you would add an S3Client as above
# with super().__init__('s3')
