from ec2.vpc import VPC
from client_locator import EC2Client


def main():
    # create VPC
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()
    #print ('VPC created: ' + str(vpc_response))

    # tag VPC
    vpc_name = 'FreshBotoMadeVPC'
    #we get id value of created instance from the vpc_repsonse above
    #must filter out the right dictionary value, which is under {Vpc{VpcId}}
    vpc_id = vpc_response['Vpc']['VpcId']
    #call the add_name_tag method from vpc module
    #error: make sure the sequence of the parameters is the same as in the OG method
    vpc.create_tags(vpc_id, vpc_name)

    print (f"VPC '{str(vpc_id)}' is now named '{vpc_name}'")

    # create IGW
    igw_response = vpc.create_internet_gateway()

    print (f"Internet Gateway created")

    # attach IGW
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    vpc.attach_internet_gateway(vpc_id, igw_id)

    print (f"Internet Gateway {igw_id} attached to {vpc_name}")

    # create a public Subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']
    #print ("Public subnet created " + str(public_subnet_response))
    print (f"Public Subnet {public_subnet_id} set up for {vpc_id}")

    # add name tag to public subnet
    public_subnet_name = 'FreshPublicSubnet'
    vpc.create_tags(public_subnet_id, public_subnet_name)

    print (f"Private Subnet {public_subnet_id} was named {public_subnet_name}")

    # creating public route table
    public_route_table_response = vpc.create_public_route_table(vpc_id)
    #print ("Public route table created " + str(public_route_table_response))
    print (f"Public route table set up for {vpc_id}")

    # create Internet Gateway public route
    route_table_id = public_route_table_response['RouteTable']['RouteTableId']
    vpc.create_igw_public_route(route_table_id, '0.0.0.0/0', igw_id)

    print ("Public Internet Gateway set up")
    
    # associate public subnet with route table
    vpc.associate_subnet_with_route_table(public_subnet_id, route_table_id)

    print (f"Public subnet {route_table_id} associated with {public_subnet_id}")
    
    # allow auto assigning of public IP adresses for subnets
    vpc.auto_assign_subnet_ip(public_subnet_id)

    print (f"Auto-assigning of IP's to {public_subnet_id}")

    # create private subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    print (f"Private Subnet {private_subnet_id} set up for {vpc_id}")

    # add name tag to private subnet
    private_subnet_name = 'FreshPrivateSubnet'
    vpc.create_tags(private_subnet_id, private_subnet_name)
    
    print (f"Private Subnet {private_subnet_id} was named {private_subnet_name}")


if __name__ == '__main__':
    main()
