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
