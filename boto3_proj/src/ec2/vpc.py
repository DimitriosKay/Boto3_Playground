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

    def create_internet_gateway(self):
        print ('Creating Internet Gateway...')
        return self._client.create_internet_gateway()

    def attach_internet_gateway(self, vpc_id, igw_id):
        print ('Attaching Internet Gateway...')
        return self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )
    
    def create_subnet(self, vpc_id, cidr_block ):
        print ('Creating Subnet...')
        return self._client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block
        )

    def create_public_route_table(self, vpc_id):
        print ('Creating Route Table...')
        return self._client.create_route_table(
            VpcId=vpc_id
        )

    def create_igw_public_route(self, route_table_id, destination_cidr_block, igw_id):
        print ("Creating Internet Gateway Public route...")
        return self._client.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock=destination_cidr_block,
            GatewayId=igw_id
        )

    def associate_subnet_with_route_table(self, public_subnet_id, route_table_id):
        print ("Associating Route Table with Subnet...")
        return self._client.associate_route_table(
            SubnetId=public_subnet_id,
            RouteTableId=route_table_id
        )

    def auto_assign_subnet_ip(self, public_subnet_id):
        print ("Activate auto-assigning of public IP's...")
        return self._client.modify_subnet_attribute(
            SubnetId=public_subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )

