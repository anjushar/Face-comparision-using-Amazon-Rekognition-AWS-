import os
import boto3
global a
s3_bucket = 'exit_faces' 
s3_bucket_region = 'us-east-1'

myList = ['entry','exit']

for i in range(len(myList)):
    m=myList[i]
    print (m)
    folder = m
    s3 = boto3.client('s3')
    key_name = folder + '/' 
    s3_connect = boto3.client('s3', s3_bucket_region)

    try:
        bucket = s3_connect.put_object(Bucket=s3_bucket, Key=key_name)
        print ("Bucket:", bucket)
    except Exception as e:
        print ("Bucket Error " , e)

# upload File to S3
    for filename in os.listdir(folder):
        file_key_name = folder + '/' + filename
        local_path = os.getcwd()
        local_name = local_path + '/' + key_name + filename
        upload = s3_connect.upload_file(local_name, s3_bucket, file_key_name)


# list all objects

s3 = boto3.resource('s3')
my_bucket = s3.Bucket(s3_bucket)
for file in my_bucket.objects.all():
    a = file.key
    print(a)





