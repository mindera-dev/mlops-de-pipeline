import k8s_exec
import s3_exec
# 
# - Comment : Run export(sftp) odm(match-1)
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

def main():
    #Run export lims
    res = k8s_exec.exec_commands('exportlims', '779792627677.dkr.ecr.us-west-2.amazonaws.com/lambda-py:v2.0.0', 'python3 mlops-de-get-lims.py')
    print(res)
    
    #make result file
    f = open('/dags/mlops-pipeline-result/export_lims.txt','w')
    f.write(str(res))
    f.close()
    print(snakemake.output[0])
    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()
    print(res)

if __name__ == '__main__':
    main()