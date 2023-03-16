import boto3

region_name = 'us-west-2'

#print('s3_save(%s, %s)' % (s3path, content))
s3 = boto3.client(
    service_name = "s3",
    region_name = region_name
)
print('s3: client')


