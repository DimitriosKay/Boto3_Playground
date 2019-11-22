# AWS infrastructure setup using Python and Boto3
## *Basic implementation primarily a study for now*

#                                                   
#### Started off with few dabble scripts, bringing up and deleting an S3 bucket and an EC2 instance:
##### __Run the files with a standard *python3 filename.py*__
* ec2_spawn - Create the instance and run a *.create_tags* which allows you to specify the name of the instance
* ec2_del - Run the script, paste your instance ID, Enter ... Profit
* s3_spawn - Create bucket with name specified, in the location specified, then call the *.upload_file*
* s3_del - Fetches the bucket name, checks files in bucket(iterates through objects.all), removes them(objects.delete) and deletes the bucket
* test_s3_check.py - My study file, when I was going thorugh the documentation.
  * __*Object*__ referes to a file in the bucket,
  * __*Action*__ can read the file we fetch with the previous command,
  * __*Atributes*__ can be *.last_modified* or *.e_tag*


#                                                   
#### Developed the boto3_proj while learning from a Udemy AWS course:
##### __Here we run *python3 deploy.py* or to run a specific service (eg. *_instance()* classes or the *main()* vpc infrastructure) comment out  statements at the bottom of the file__
#                                                      



[] Was (*sort of still am*) trying to make sense of when to use client or resource in the __boto3.*client/resource*__ calls

[] Would be great to set up a infrastructure tare-down script (like teraform destroy) for the whole VPC network

[] Could also 'modularize' it a bit more
