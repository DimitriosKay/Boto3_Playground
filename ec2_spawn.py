import boto3

ec2 = boto3.resource('ec2')
ec2cli = boto3.client('ec2')

# instance creation line, gotta specify Max and Min aparently
ec2.create_instances(ImageId='ami-00a1270ce1e007c27', InstanceType= 't2.micro', MinCount=1, MaxCount=1)


# with waiters, you need to specify the exact resource to wait for
# aka in my implementation it makes no sence to use it ...
#instance = ec2.Instance('InstanceId')
#wait = instance.wait_until_running()
#print (type(wait))


# here I describe isntances, fetching all info on all instances
# then filter through the Dictionary till i get to the instances
# then fetch the InstanceId and Print
response = ec2cli.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        data = ec2.Instance(instance['InstanceId'])
        
        status = ec2cli.describe_instance_status()
        print (type(data))
        print (data)
        #print (status)

# 'slighty' more concise alternative to the above ...
for instance in ec2.instances.all():
    print (instance.id, instance.state['Name'])
    status = instance.state['Name']
# added a function for the tagging of available instances
# can be expanded endlessly
# extra: add 'sleep' https://intellipaat.com/community/8354/boto-ec2-create-an-instance-with-tags
    if status == 'running':
        ec2cli.create_tags(Resources=[instance.id], Tags=[{'Key': 'Name','Value': 'InstanceButAWS'}])
        print ('Tagged !')
    else:
        print ('Tag FAILED !')
