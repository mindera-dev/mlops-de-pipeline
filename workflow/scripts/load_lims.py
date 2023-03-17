import time
import os
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
# 
# - Comment : Run load lims
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

def main():
    #Run load lims
    print('export_lims start!!')    
    
    config.load_kube_config()
    try:
        c = Configuration().get_default_copy()
    except AttributeError:
        c = Configuration()
        c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    
    res = k8s_exec.exec_commands('loadlims', '779792627677.dkr.ecr.us-west-2.amazonaws.com/minderadatatransfer:V1.0.2', '/java/datatransfer.sh lims 2023-03-16')
    print(res)

    #make result file
    directory = "/home/ubuntu/mlops-de-pipeline/2023-03-17"
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
    
    f = open(directory + '/load_lims.txt','w')
    f.write(str(res))    
    f.close()

    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()

if __name__ == '__main__':
    main()
