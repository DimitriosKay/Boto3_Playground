from ec2.vpc import VPC
from client_locator import EC2Client


def main():
    # create VPC
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()

    print ('VPC created: ' + str(vpc_response))

    # tag VPC
    resource_name = 'FreshBotoMadeVPC'
    # we get id value of created instance from the vpc_repsonse above
    # must filter out the right dictionary value, which is under {Vpc{VpcId}}
    resource_id = vpc_response['Vpc']['VpcId']

    # call the add_name_tag method from vpc module
    # error: make sure the sequence of the parameters is the same as in the OG method
    vpc.create_tags(resource_id, resource_name)

    print (f"VPC '{str(resource_id)}' is now named '{resource_name}'")

if __name__ == '__main__':
    main()
