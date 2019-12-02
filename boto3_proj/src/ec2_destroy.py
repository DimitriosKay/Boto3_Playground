from ec2.destroy_vpc import destroy_VPC
from resource_locator import EC2Resource
from client_locator import EC2Client

ec2_resource = EC2Resource().get_resource()
ec2_client = EC2Client().get_client()

def main():

    ec2 = destroy_VPC(ec2_resource)
    ec2_cli = destroy_VPC(ec2_client)

    # mdular filter of what vpc instance you are searching up
    # if your tags change change it below
    # tags being the best way to fetch our instance)
    filters = [{
        'Name': 'tag:Name',
        'Values': [
            'FreshBotoMadeVPC'
        ]
    }]

    # list your instances, with the applied filter (will list only the ones tagged with the name)
    list_vpc_response = ec2.vpc_id(filters)

    for dhcp in list_vpc_response['Vpcs']:
        dhcp_id = dhcp['DhcpOptionsId']
        print (dhcp_id)

    # itterate through the dict that is 'Vpcs', find the 'VpcId' and do Below
    for id in list_vpc_response['Vpcs']:
        vpc_id = id['VpcId']
        print (vpc_id)

    # method to execute vpc actions, without defining it every line
    # (equivalent of 'boto3.resource.Vpc')
    vpc = ec2_resource.Vpc(vpc_id)


    for rt in vpc.route_tables.all():
        print (rt)
        for rta in rt.associations:
            print (rta)
            print (rta.main)
            if not rta.main:
                rta.delete()
                ec2_client.delete_route_table(RouteTableId=rt.id)

    for subnet in vpc.subnets.all():
        ec2_client.modify_subnet_attribute(
            SubnetId= subnet.id,
            MapPublicIpOnLaunch={'Value': False}
        )

    # detach and delete igw
    for gateway in vpc.internet_gateways.all():
        # '.id' goes in the list and get's only the id number
        print (gateway.id) 
        print ('Detaching ...')
        vpc.detach_internet_gateway(InternetGatewayId=gateway.id)
        print ('Detached')
        gateway.delete()
        # delete gateway
        #ec2_client.delete_internet_gateway(InternetGatewayId=gateway.id)

    for sg in vpc.security_groups.all():
        print (sg)
        if sg.group_name != 'default':
            sg.delete()
 
    for nacl in vpc.network_acls.all():
        print (nacl)
        if not nacl.is_default:
            nacl.delete()
            ec2_client.delete_network_acl(NetworkAclId=nacl.id)

    for subnet in vpc.subnets.all():
        print (subnet)
        ec2_client.delete_subnet(SubnetId=subnet.id)

    ec2_client.delete_vpc(VpcId=vpc_id)

    ec2_client.delete_dhcp_options(DhcpOptionsId=dhcp_id)

if __name__ == '__main__':
    main() 
