import boto3
import os


BUCKET = "exit_faces"

s3 = boto3.resource('s3')
my_bucket = s3.Bucket(BUCKET)



entry_folder_name = "entry/"
exit_folder_name = "exit/"

q = []
############################# function for listing faces in folders of a bucket
entry_folder = "entry/"
exit_folder = "exit/"
a = []
b = []
images = []
c=0
###############################################################



def list_faces():
    c=0
   
    del images[:]
    
    for file in my_bucket.objects.all():
        g = file.key
        print (".......after:" + str(g))
        images.append(g)


    
    for x in images:
        if( x == entry_folder ):
            continue

        elif(x != exit_folder):
            a.append(x)
           
        if(x == exit_folder):
            break

   




    for y in  images:
        if(y != exit_folder):
            if(c==1):
                b.append(y)
                
            else:
                continue

        elif(y == exit_folder):
            c=1

        else:
            break
    


################################delete object

def delete_faces(bucket, key, region="us-east-1"):
                        rekognition = boto3.client("rekognition", region)
                        objs = list(my_bucket.objects.filter(Prefix=key))
                        response = my_bucket.delete_objects(
                            Delete={
                                'Objects': [
                                    {
                                        'Key': key,
                                     
                                        },
                                    ],
                                'Quiet': True|False
                                },
                            )
                        return response

############################## face comparision
def compare_faces(bucket, key, bucket_target, key_target, threshold=0, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
                }
            },
        TargetImage={
            "S3Object": {
                "Bucket": bucket_target,
                "Name": key_target,
                }
            },
        SimilarityThreshold=threshold,
        )
    return response['SourceImageFace'], response['FaceMatches']


list_faces()
print(a,b,q)
for i in a:
    for j in b:
        KEY_SOURCE = i
        KEY_TARGET = j


        print ("............face comparision started.....................")
        print (i,j)

        source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)


        print ("Source Face ({Confidence}%)".format(**source_face))


        for match in matches:
                print ("Target Face ({Confidence}%)".format(**match['Face']))
                percent = match['Similarity']
                        
                print ("  Similarity : {}%".format(match['Similarity']))
                print("......................face comparision ended ............................................")

                print(percent)
                if(percent>80):
                    if i not in q:
                        q.append(i)
print (q)

for key in q:
    delete_faces(BUCKET, key, region="us-east-1")





                        

                
