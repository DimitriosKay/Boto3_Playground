from ec2.destroy_vpc import destroy_VPC
from ec2.ec2 import EC2
from resource_locator import EC2Resource
from client_locator import EC2Client

# import time

ec2_resource = EC2Resource().get_resource()
ec2_client = EC2Client().get_client()

def main():

    ec2 = destroy_VPC(ec2_resource)
    ec2_cli = destroy_VPC(ec2_client)
    inst_cli = EC2(ec2_client)

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
   

    # iterate through all your instances
    for instance in ec2.instance_id():
        instance_id = instance.id
        
        # fetch your waiter from destroy_VPC
        complete_waiter = ec2.waiter(instance_id)
        
        # terminate instance - method fetched from ec2/ec2.py
        inst_cli.terminate_ec2_instance(instance_id)

        # make the thing wait till it's done doing it's thing
        try:
            complete_waiter.wait(InstanceIds = [instance_id])
            print (f'Instance ({instance_id}) has been terminated')
        except:
            print ('Failed ?!')


        '''
        while ec2.describe_instance_status(instance_id) != 'stopped':
            time.sleep(2)
            print (ec2.describe_instance_status(instance_id) + ' ' + instance_id)
            #print (' ' + instance_id)
            #print (f'Instance {instance_id} has been {instance_state}')
        '''

        '''
        if instance_state != 'terminated':
            status = 'running'
            # waiter goes here
            while status != 'terminated':
                time.sleep(2)
                for instance in ec2.instance_id():
                    instance_state = instance.state['Name']
                    print ('Still terminating ...')
                    print (f'{instance_state} -- {instance_id}')
                    if instance_state == 'terminated':
                        status = 'terminated'
                        return status
        '''
                                

    # itterate through the dict 'Vpcs', find the 'DhcpOptionsId' and do Below
    for dhcp in list_vpc_response['Vpcs']:
        dhcp_id = dhcp['DhcpOptionsId']
        #print (dhcp_id)

    # itterate through the dict 'Vpcs', find the 'VpcId' and do Below
    for id in list_vpc_response['Vpcs']:
        vpc_id = id['VpcId']
        print (f'Working with VPC {vpc_id} ...')

    # method to execute vpc actions, without defining it every line
    # (equivalent of 'boto3.resource.Vpc')
    vpc = ec2_resource.Vpc(vpc_id)

# why not run these in a for loop where you would fetch vpc id and run all the code below for the vpc
# will give you the option to delete multiple vpcs ?

    # iterate through route tables, disassociate and delete everything
    # that is not the main association table
    for rt in vpc.route_tables.all():
        print (rt)
        for rta in rt.associations:
            print (rta)
            print (rta.main)
            if not rta.main:
                rta.delete()
                ec2_client.delete_route_table(RouteTableId=rt.id)
                print (f'Deleted route table {rt.id}')

    # unmap Public IP on subnets
    for subnet in vpc.subnets.all():
        ec2_client.modify_subnet_attribute(
            SubnetId= subnet.id,
            MapPublicIpOnLaunch={'Value': False}
        )
        print (f'Deleted subnet {subnet.id}')

    # detach and delete igw
    for gateway in vpc.internet_gateways.all():
        # '.id' goes in the list and get's only the id number
        print (gateway.id)
        print ('Detaching ...')
        vpc.detach_internet_gateway(InternetGatewayId=gateway.id)
        print ('Detached')
        gateway.delete()
        print (f'Deleted gateway {gateway.id}')
        # delete gateway (this line is not necesary ?)
        #ec2_client.delete_internet_gateway(InternetGatewayId=gateway.id)

    # just fetch and delete the SGs that are not default
    for sg in vpc.security_groups.all():
        print (sg)
        if sg.group_name != 'default':
            sg.delete()
            print (f'Deleted security group {sg}')
    
    # again fetch and delete NACLs that are not default
    for nacl in vpc.network_acls.all():
        print (nacl)
        if not nacl.is_default:
            nacl.delete()
            ec2_client.delete_network_acl(NetworkAclId=nacl.id)
            print (f'Deleted Network ACL {nacl.id}')

    # after we have dissasociated all things from the subnets
    # delete them
    for subnet in vpc.subnets.all():
        print (subnet)
        ec2_client.delete_subnet(SubnetId=subnet.id)
        print (f'Deleted subnet {subnet}')

    # then delete the VPC
    ec2_client.delete_vpc(VpcId=vpc_id)
    print (f'VPC {vpc_id} deleted')

    # and the residual dhcp options
    ec2_client.delete_dhcp_options(DhcpOptionsId=dhcp_id)
    print ('DHCP options deleted')

    key_name = 'fresh_key_pair'
    # delete the leftover key pair
    inst_cli.delete_key_pair(key_name)
    print (f'Key pair ({key_name}) deleted')

# and Done, sparkling clean


if __name__ == '__main__':
    main() 
