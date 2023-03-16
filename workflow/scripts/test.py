import boto3

region_name = 'us-west-2'

#print('s3_save(%s, %s)' % (s3path, content))
s3 = boto3.client(
    service_name = "s3",
    region_name = region_name
)
print('s3: client')

paginator = client.get_paginator('list_objects_v2')
response_iterator = paginator.paginate(
    Bucket=mlops-lims-dump-prod, 
    Prefix="output_files/"
)

compare_file_string = "-Reads-Counts-and-logCPM.csv"
file_list=[]
try:
    for page in response_iterator:
        for content in page['Contents']:
            # print(content)
            key = content['Key']
            # print("key:", key)
            if compare_file_string in key:    
                split_file = key.split("/")
                # print("split_file:",split_file)
                if len(split_file) == 4:
                    file_list.append({'bucket': os_env_access_bucket_name, 'batch': split_file[1], 'sample': split_file[2]})
                    #return file_list

                else:
                    print(key)

    return file_list

except Exception as e:
    print(e)
    raise e
