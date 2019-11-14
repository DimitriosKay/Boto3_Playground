import boto3

# resource is Needed here. If we use client, we error
s3 = boto3.resource('s3')

bname = 'freshnewbucky'

# So Object requires the key because that's what the object will be looking for
# Any of the operators below are going to be refering to the swag.txt file
obj = s3.Object(bucket_name=bname, key='swag.txt')
print (obj.bucket_name)

# Action - executed to fetch the object (swag.txt) and assign to 'response'
#        - get the [Body] tag from 'response' and read it
response = obj.get()
data = response['Body'].read()
print (response)
print (data)

# Use of atributes, coded in the service on creation (might be editable)
print (str(obj.last_modified) + '\n' + obj.e_tag)
