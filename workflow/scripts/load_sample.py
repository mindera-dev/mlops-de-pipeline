import time
import os
import boto3
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
# 
# - Comment : Get Remain sample list from s3
#             , Repeat load sample
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

#odate = "2023-04-13"
odate=snakemake.params.ODATE
print(odate)
odate = str(odate)[0:4] + '-' + str(odate)[4:6] + '-' + str(odate)[6:8]
print(odate)

def main():    
    print('load_sample start!!')

    print('get reamin sample list!!')
    #get environment variable
    os_aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID","")
    os_aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY","")
    os_s3_region_name = os.getenv("s3_region_name","us-west-2")
    os_bucket_name = os.getenv("access_bucket_snakemake_name", "mindera-mlops-prod-bucket")

    print("aak : " + os_aws_access_key_id)
    print("asak : " + os_aws_secret_access_key)    
    print("bucket : " + os_bucket_name)

    #set file name about get remain sample list txt
    file = 'not_exist_pipeline_' + odate + '.txt'

    
    bucket_file = "output_folders/remain_sample_list/" + file
    local_file = file

    #s3 connect
    try:        
        s3 = boto3.client(
            service_name = "s3",
            region_name = os_s3_region_name,
            aws_access_key_id = os_aws_access_key_id,
            aws_secret_access_key = os_aws_secret_access_key
        )
    except Exception as e:
        print(e)

    #get s3 list
    obj_list = s3.list_objects(Bucket=os_bucket_name)
    contents_list = obj_list['Contents']

    file_list=[]
    check_exist_file = False

    #check s3 list    
    for content in contents_list:
        #print("content : %s" % content)
        key = content['Key']
        if key == bucket_file:
            check_exist_file = True
            break
        else:
            check_exist_file = False

    #download reamin sample list file from s3 bucket
    if check_exist_file == True:
        print("file exist, file download!!")
        s3.download_file(os_bucket_name, bucket_file, local_file)
        
        #check remain sample list file
        f = open(local_file, 'r')    
        line = f.readline()
        print("line",line)

        f.close()    

        #Repeat load sample
        cnt = 0
        dict_line = eval(line)
        result = ""
        config.load_kube_config()
        for i in dict_line:
            batch = i['batch']
            sample = i['sample']
            config.load_kube_config()
            try:
                c = Configuration().get_default_copy()
            except AttributeError:
                c = Configuration()
                c.assert_hostname = False
            Configuration.set_default(c)
            core_v1 = core_v1_api.CoreV1Api()
            shcommand = '/java/datatransfer.sh rnaseq ' + str(batch) + ' ' + str(sample)
            res = exec_commands('loadsample', '779792627677.dkr.ecr.us-west-2.amazonaws.com/minderadatatransfer:V1.0.2', shcommand, core_v1)
            if "" == result:
                result = res
            else:
                result = result + res
            cnt = cnt + 1

        print(result)

        #make result file
        '''
        directory = "/home/ubuntu/mlops-de-pipeline/" + odate
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")
        
        f = open(directory + '/load_sample.txt','w')
        f.write(str(res))
        f.close()
        '''
        print(snakemake.output[0])
        f = open(snakemake.output[0],'w')
        f.write(str(result))
        f.close()

    else:
        print("file not exist!!")
        print(snakemake.output[0])
        f = open(snakemake.output[0],'w')
        f.write("file not exist!!")
        f.close()
    s3.close()
    
    
    
def exec_commands(appname, image_name, commands, api_instance = None):
    namespace = 'default'
    if api_instance == None:
        config.load_incluster_config()
        api_instance = core_v1_api.CoreV1Api()
    
    name = appname + '-' + str(round(time.time() * 1000000))
    print(name)
    
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)
    
    if not resp:    
        print("Pod %s does not exist. Creating it..." % name)
        pod_manifest = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': name,
                'namespace': namespace
            },
            'spec': {
                'securityContext': {
                    'fsGroup': 1000
                },
                'serviceAccountName': 'spark',
                'ttlSecondsAfterFinished': 600,
                'containers': [{
                    'name': name,
                    'image': image_name,  #'j2lab/snakemake:v1.0.0'
                    'imagePullPolicy': 'IfNotPresent',
                    "args": [
                        "/bin/sh",
                        "-c",
                        "while true;do date;sleep 5; done"
                    ],
                    "env": [
                      {
                        "name": "dbhost",
                        "value": "mlops-postgres.cluster-c2ptheuspjk9.us-west-2.rds.amazonaws.com"
                      },
                      {
                        "name": "dbport",
                        "value": "5432"
                      },
                      {
                        "name": "database",
                        "value": "postgres"
                      },
                      {
                        "name": "dbdatabase",
                        "value": "postgres"
                      },
                      {
                        "name": "dbhost_lims",
                        "value": "minderadbprod-cluster.cluster-cotuitlujf92.us-west-1.rds.amazonaws.com"
                      },
                      {
                        "name": "dbport_lims",
                        "value": "54321"
                      },
                      {
                        "name": "dbname_lims",
                        "value": "minderadbprod"
                      },
                      {
                        "name": "dbschema",
                        "value": "public"
                      },
                      {
                        "name": "dbuser",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "dbuser",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "dbpasswd",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "dbpasswd",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "aws_access_key_id",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "aws_access_key_id",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "aws_secret_access_key",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "aws_secret_access_key",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "s3bucktname_lims",
                        "value": "mlops-lims-dump-prod"
                      },
                      {
                        "name": "s3bucktname_odm",
                        "value": "mlops-odm-dump-prod"
                      },
                      {
                        "name": "s3bucktname_rnaseq",
                        "value": "prod-dna-nexus-result"
                      },
                      {
                        "name": "s3_region_name",
                        "value": "us-west-2"
                      },
                      {
                        "name": "s3_region_name_odm",
                        "value": "us-west-1"
                      },
                      {
                        "name": "s3_region_lims_name",
                        "value": "us-west-1"
                      },
                      {
                        "name": "access_bucket_snakemake_name",
                        "value": "mindera-mlops-prod-bucket"
                      },
                      {
                        "name": "SECRET_odm",
                        "value": "prod_cc_lambda_secrets"
                      },
                      {
                        "name": "SECRET_lims",
                        "value": "lims_app_secrets"
                      }

                    ],
                }],
            }
        }
        resp = api_instance.create_namespaced_pod(body=pod_manifest,
                                                  namespace=namespace)
        while True:
            resp = api_instance.read_namespaced_pod(name=name,
                                                    namespace=namespace)
            if resp.status.phase != 'Pending':
                break
            time.sleep(1)
        print("Pod %s done created." % name)
    else:
        print("Pod %s does exist. First delete it" % name)
    
    exec_command = [
        '/bin/sh',
        '-c',
        commands]
    restm = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    # return restm
    try:
        resdel = api_instance.delete_namespaced_pod(name=name,
                                                    namespace=namespace)
        print("Pod %s does delete." % name)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    finally:
        return restm

if __name__ == '__main__':
    main()
