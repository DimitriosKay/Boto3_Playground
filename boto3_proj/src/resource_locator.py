import boto3

# internal class making the base of the resource allocation
class ResourceLocator:
    # this init is running self._resource which has the boto3 command in
    # with specified region
    def __init__(self, resource):
        self._resource = boto3.resource(resource, region_name='eu-west-2')
    # then this one returns the resource, mapped with details from next class
    def get_resource(self):
        return self._resource

class EC2Resource(ResourceLocator):
    def __init__(self):
        super().__init__('ec2')

class S3Resource(ResourceLocator):
    def __init__(self):
        super().__init__('s3')
