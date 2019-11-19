from ec2.vpc import VPC_Destroy
from client_locator import EC2Client

def main():
    ec2_client = EC2Client().get_client()
    vpc = VPC_Destroy(ec2_client)

    vpc_pick = input('Paste VPC ID to delete: ')

    vpc.destroy_vpc(vpc_pick)

if __name__ == '__main__':
    main()
