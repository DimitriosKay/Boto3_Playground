class EC2:
    def __init__(self, client):
        self._client = client

    def check_if_key_pair(self):
        print ('Checking if key pair is available ...')
        return self._client.describe_key_pairs()

    def create_key_pair(self, key_name):
        print ('Creating Key Pair...')
        return self._client.create_key_pair(
            KeyName=key_name
        )

    def delete_key_pair(self, key_name):
        print ('Deleting Key Pair ...')
        return self._client.delete_key_pair(
            KeyName=key_name
        )

    def create_security_group(self, group_name, description, vpc_id):
        print ('Creating Security Group...')
        return self._client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        
        )

    '''
    Public EC2 instance creation
    '''
    def add_public_inbound_rules(self, public_sg_id):
        print ('Adding Ingress Rules...')
        return self._client.authorize_security_group_ingress(
            GroupId=public_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        
        )
 
    '''
    Private EC2 instance creation
    '''
    def add_private_inbound_rules(self, private_sg_id):
        print ('Adding Ingress Rules...')
        return self._client.authorize_security_group_ingress(
            GroupId=private_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        
        )
   
    def create_ec2_instance(self, image_id, key_name, min_count, max_count, security_group_id, subnet_id, user_data):
        print ('Launching EC2 Instance...')
        return self._client.run_instances(
            ImageId=image_id,
            InstanceType='t2.micro',
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            UserData=user_data
        )
    
    def describe_ec2_instances(self):
        print ('Describing EC2 Instances...')
        return self._client.describe_instances()

    def modify_ec2_instance(self, instance_id):
        print (f'Disabling termination for EC2 instance {instance_id}')
        return self._client.modify_instance_attribute(
            InstanceId=instance_id,
            DisableApiTermination={'Value': True}
        )
    
    def stop_ec2_instance(self, instance_id):
        print (f'Stoping EC2 instance {instance_id} ...')
        return self._client.stop_instances(
            InstanceIds=[instance_id]
        )

    def start_ec2_instance(self, instance_id):
        print (f'Starting EC2 instance {instance_id} ...')
        return self._client.start_instances(
            InstanceIds=[instance_id]
        )

    def terminate_ec2_instance(self, instance_id):
        print (f'Terminating EC2 instance {instance_id} ...')
        return self._client.terminate_instances(
            InstanceIds=[instance_id]
        )

