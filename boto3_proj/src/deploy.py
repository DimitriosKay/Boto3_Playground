from ec2.vpc import VPC
from ec2.ec2 import EC2
from client_locator import EC2Client
from resource_locator import EC2Resource

ec2_client = EC2Client().get_client()
ec2_resource = EC2Resource().get_resource()

def main():

    vpc = VPC(ec2_client)

    # create VPC
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


    '''
    ec2 instance creation segment
    '''
    
    ec2 = EC2(ec2_client)


    # creating Key Pair
    key_name = 'fresh_key_pair'
    
    # get key pair name
    key_pair = ec2_resource.KeyPair(key_name)
   
    # check if key pair is available and if it is create it, if not delete and create all over
    if key_pair.name == key_name:
        print (f'Key pair {key_pair.name} available!')
        print ('Deleting Key Pair ...')
        key_pair.delete()
        key_pair_response = ec2.create_key_pair(key_name)
    elif key_pair.name != key_name:
        print ('Nah, no key pair ...' + key_pair.name)
        key_pair_response = ec2.create_key_pair(key_name)

    print (f"Key pair {key_pair_response['KeyName']} has been created")

    # * Public EC2 instance setup block *
    # create Security Group
    public_security_group_name='BotoPubSG'
    description='Public security group with boto3'

    pub_security_group_response = ec2.create_security_group(public_security_group_name, description, vpc_id)
    print (f'Public security group created: {pub_security_group_response}')

    # adding inbound rules to public security group
    public_sg_id = pub_security_group_response['GroupId']
    ec2.add_public_inbound_rules(public_sg_id)
    print (f'Security rules added to {public_sg_id}')

    # ec2 instance launch script
    user_data = """#!/bin/bash
                yum update -y
                yum install httpd -y
                service httpd start
                chkconfig httpd on
                echo "<html><body><h1>Hello World! All the way from Boto3</h1></body></html>" > /var/www/html/index.html
                """

    # create EC2 VM into public subnet
    image_id = 'ami-00e8b55a2e841be44'
    min_count = 1
    max_count = 1
    
    public_ec2_response = ec2.create_ec2_instance(image_id, key_name, min_count, max_count, public_sg_id, public_subnet_id, user_data)
    print (f'EC2 instance created: \n{public_ec2_response}')

    # * Private EC2 instance setup block *
    # create Private Security Group
    private_security_group_name='BotoPrivSG'
    description='Private security group with boto3'

    priv_security_group_response = ec2.create_security_group(private_security_group_name, description, vpc_id)
    print (f'Private security group created: {priv_security_group_response}')

    # adding inbound rules to private security group
    private_sg_id = priv_security_group_response['GroupId']
    ec2.add_private_inbound_rules(private_sg_id)
    print (f'Security rules added to {private_sg_id}')

    # launch private ec2 instance
    private_ec2_response = ec2.create_ec2_instance(image_id, key_name, min_count, max_count, private_sg_id, private_subnet_id, """""")
    print (f'EC2 instance created: \n{private_ec2_response}')


def describe_instance():
    
    ec2 = EC2(ec2_client)

    # describe ec2 instances
    
    # add a variable for the name within the itterate method using VV
    # https://stackoverflow.com/questions/37293366/what-is-the-correct-ways-to-write-boto3-filters-to-use-customise-tag-name
    describe_ec2 = ec2.describe_ec2_instances()
   
    for i in describe_ec2:
        print ('\n')
        print (describe_ec2)


def modify_instance():
    
    ec2 = EC2(ec2_client)
    
    instance_id = 'i-097636e65a91fa964'
    ec2.modify_ec2_instance(instance_id)

def stop_instance():

    ec2 = EC2(ec2_client)

    instance_id = 'i-025c48f6f42e71f33'
    ec2.stop_ec2_instance(instance_id)

def start_instance():

    ec2 = EC2(ec2_client)

    instance_id = 'i-025c48f6f42e71f33'
    ec2.start_ec2_instance(instance_id)

def terminate_instance():

    ec2 = EC2(ec2_client)

    instance_id = 'i-025c48f6f42e71f33'
    ec2.terminate_ec2_instance(instance_id)


if __name__ == '__main__':
    main()
    #describe_instance()
    #modify_instance()
    #stop_instance()
    #start_instance()
    #terminate_instance()
