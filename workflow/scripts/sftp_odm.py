import k8s_exec
import s3_exec
# 
# - Comment : Run export(sftp) odm(match-1)
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#
def main():    
    #Run export(sftp) odm(match-1)
    print('sftp_odm start!!')
    '''
    res = k8s_exec.exec_commands('sftpodm', '779792627677.dkr.ecr.us-west-2.amazonaws.com/lambda-py:v2.0.0', 'python3 mlops-de-get-odm.py')
    print(res)

    #make result file
    
    f = open('/dags/mlops-pipeline-result/sftp_odm.txt','w')
    f.write(str(res))
    f.close()    

    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()
    '''

if __name__ == '__main__':
    main()
