import k8s_exec
import s3_exec
# 
# - Comment : Run load fsdata
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

def main():    
    #Run load fsdata
    res = k8s_exec.exec_commands('loadfs', '779792627677.dkr.ecr.us-west-2.amazonaws.com/minderadatatransfer:V1.0.1', '/java/datatransfer.sh fsdata 2022-12-21')
    print(res)

    #make result file
    f = open('/dags/mlops-pipeline-result/load_fs.txt','w')
    f.write(str(res))    
    f.close()

    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()

if __name__ == '__main__':
    main()