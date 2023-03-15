import k8s_exec
# import s3_exec
import os

ODATE=snakemake.config["odate"]

def main():    
    #Run export remain sample list
    res = k8s_exec.exec_commands('remainsample', '779792627677.dkr.ecr.us-west-2.amazonaws.com/lambda-py:v2.0.0', 'python3 mlops-de-sample.py')
    print(res)

    #make result file
    f = open('/dags/mlops-pipeline-result/remain_sample.txt','w')    
    f.write(str(res))
    f.close()

    print(snakemake.output[0])
    f = open(snakemake.output[0],'w')    
    f.write(str(res))
    f.close()

if __name__ == '__main__':
    main()