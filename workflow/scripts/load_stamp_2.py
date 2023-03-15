import k8s_exec
import s3_exec
# 
# - Comment : Run load odm(stamp-2)
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

def main():
    #Run load odm(stamp-2)
    res = k8s_exec.exec_commands('loadstamp2', 'j2lab/minderadatatransfer:VD_Daily_0.2.4', '/java/datatransfer.sh odm 2022-12-21 odm1.3_fullSTAMP2_ODM_Export.xml STAMP-2')
    print(res)

    #make result file
    f = open('/dags/mlops-pipeline-result/load_stamp_2.txt','w')
    f.write(str(res))    
    f.close()

    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()
    

if __name__ == '__main__':
    main()