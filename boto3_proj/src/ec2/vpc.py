class VPC:

    def __init__(self, client):
        self._client = client

    # VPC creation
    def create_vpc(self):
        print ('Creating...')
        # equivalent of boto3.client.create_vpc, but fetched from out ClientLocator
        return self._client.create_vpc(
            CidrBlock='10.0.0.0/16'        
        )

    def create_tags(self, resource_id, resource_name): 
        print ('Tagging...')
        # as above, as if we run boto3.client.create_tags()
        # here we need id and name parameters, which we expect from the main.py
        # then we populate fields below when method is initiated
        return self._client.create_tags(
            Resources=[
                resource_id
            ],
            Tags=[{
                'Key': 'Name',
                'Value': resource_name
            }]
        )

class VPC_Destroy:
    def __init__(self, client):
        self._client = client

    # VPC delete
    def destroy_vpc(self, vpc_id):
        print ('Destroying...')
        # keep the delete statement here
        return self._client.delete_vpc(
            VpcId=vpc_id        
        )
