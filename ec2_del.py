import boto3

inst_id = input ('Paste your ID here: ')

ec2 = boto3.resource('ec2')
ec2.Instance(inst_id).terminate()
